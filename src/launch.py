import os
import subprocess
import time
import sys
import signal
import argparse


def run_command(command, env=None):
    print(f"Executing: {' '.join(command)}")
    subprocess.run(command, check=True, env=env)


def main():
    parser = argparse.ArgumentParser(
        description="Launch the DigitalEngn infrastructure."
    )
    parser.add_argument(
        "--build", action="store_true", help="Build container images before launching."
    )
    args = parser.parse_args()

    # Add ~/bin to PATH for subprocess calls (as seen in smoke_test_steps.py)
    env = os.environ.copy()
    home_bin = os.path.expanduser("~/bin")
    if home_bin not in env["PATH"]:
        env["PATH"] = f"{home_bin}:{env['PATH']}"

    port_forward_proc = None

    def signal_handler(sig, frame):
        print("\nShutting down...")
        if port_forward_proc:
            print("Stopping port-forward...")
            port_forward_proc.terminate()
            port_forward_proc.wait()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        # Check if minikube is running
        result = subprocess.run(
            ["minikube", "status"], capture_output=True, text=True, env=env
        )
        if "Running" not in result.stdout:
            print("Minikube is not running. Starting Minikube...")
            run_command(["minikube", "start"], env=env)
        else:
            print("Minikube is already running.")

        # Ensure namespaces exist before creating secrets
        print("Ensuring namespaces exist...")
        run_command(
            ["kubectl", "apply", "-f", "infrastructure/k8s/base/namespaces.yaml"],
            env=env,
        )

        # Ensure TLS secret exists
        print("Checking for TLS secret...")
        result = subprocess.run(
            ["kubectl", "get", "secret", "-n", "digitalengn", "digitalengn-tls"],
            capture_output=True,
            env=env,
        )
        if result.returncode != 0:
            print("TLS secret not found. Generating self-signed certificate...")
            cert_dir = "/tmp/digitalengn-certs"
            os.makedirs(cert_dir, exist_ok=True)
            run_command(
                [
                    "openssl",
                    "req",
                    "-x509",
                    "-nodes",
                    "-days",
                    "365",
                    "-newkey",
                    "rsa:2048",
                    "-keyout",
                    f"{cert_dir}/tls.key",
                    "-out",
                    f"{cert_dir}/tls.crt",
                    "-subj",
                    "/CN=localhost",
                    "-addext",
                    "subjectAltName = DNS:localhost",
                ],
                env=env,
            )
            run_command(
                [
                    "kubectl",
                    "create",
                    "secret",
                    "tls",
                    "digitalengn-tls",
                    f"--cert={cert_dir}/tls.crt",
                    f"--key={cert_dir}/tls.key",
                    "-n",
                    "digitalengn",
                ],
                env=env,
            )

        # Build images if requested
        if args.build:
            print("\n--- Performing requested container builds ---")
            run_command(["uv", "run", "build"], env=env)

        # Ensure ingress addon is enabled
        print("Enabling ingress addon...")
        run_command(["minikube", "addons", "enable", "ingress"], env=env)

        # Wait for ingress controller to be ready BEFORE applying configuration
        # This prevents the "failed calling webhook" error for Ingress resources
        print("Waiting for ingress controller to be ready...")

        # First wait for the deployment to exist (minikube addon might take a second to create it)
        max_retries = 10
        for i in range(max_retries):
            result = subprocess.run(
                [
                    "kubectl",
                    "get",
                    "deployment",
                    "-n",
                    "ingress-nginx",
                    "ingress-nginx-controller",
                ],
                capture_output=True,
                env=env,
            )
            if result.returncode == 0:
                break
            if i == max_retries - 1:
                print(
                    "Error: ingress-nginx-controller deployment not found after enabling addon.",
                    file=sys.stderr,
                )
                sys.exit(1)
            time.sleep(2)

        run_command(
            [
                "kubectl",
                "wait",
                "--namespace",
                "ingress-nginx",
                "--for=condition=ready",
                "pod",
                "--selector=app.kubernetes.io/component=controller",
                "--timeout=120s",
            ],
            env=env,
        )
        # Extra buffer for the webhook service to start listening
        print("Waiting an extra 10 seconds for the webhook service to stabilize...")
        time.sleep(10)

        # Apply kustomization
        print("Applying infrastructure configuration...")
        run_command(["kubectl", "apply", "-k", "infrastructure/k8s/base"], env=env)

        # Wait for all pods to be ready
        print("\nWaiting for all pods to be ready (Running or Completed)...")
        while True:
            result = subprocess.run(
                ["kubectl", "get", "pods", "-A"],
                capture_output=True,
                text=True,
                env=env,
            )

            lines = result.stdout.strip().split("\n")
            if len(lines) > 1:
                print("\n--- Current Pod Status ---")
                print(result.stdout)

                all_ready = True
                # Skip header line
                for line in lines[1:]:
                    parts = line.split()
                    if len(parts) < 4:
                        continue

                    ready_status = parts[2]
                    status = parts[3]

                    # Jobs that have finished successfully
                    if status in ["Completed", "Succeeded"]:
                        continue

                    # Pods must be Running
                    if status != "Running":
                        all_ready = False
                        break

                    # If Running, check if all containers are ready (e.g., 1/1)
                    if "/" in ready_status:
                        try:
                            ready_count, total_count = ready_status.split("/")
                            if ready_count != total_count:
                                all_ready = False
                                break
                        except ValueError:
                            all_ready = False
                            break

                if all_ready:
                    print("\nAll pods are ready.")
                    break
            else:
                print("No pods found yet, waiting...")

            print("Still waiting for pods to initialize (checking again in 5s)...")
            time.sleep(5)

        print("Infrastructure deployed successfully.")

        # Start port-forward for ingress controller
        print("Starting port-forward on localhost:8080 (HTTPS)...")
        port_forward_proc = subprocess.Popen(
            [
                "kubectl",
                "port-forward",
                "--address",
                "localhost",
                "-n",
                "ingress-nginx",
                "service/ingress-nginx-controller",
                "8080:443",
            ],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Wait for port-forward to be ready
        time.sleep(5)
        if port_forward_proc.poll() is not None:
            stdout, stderr = port_forward_proc.communicate()
            print(
                f"Error: Port-forward failed to start.\nSTDOUT: {stdout}\nSTDERR: {stderr}",
                file=sys.stderr,
            )
            sys.exit(1)

        print("\nDeployment complete and port-forwarding active.")
        print("Core infrastructure is accessible on the network at port 8080 (HTTPS).")
        print("Examples:")
        print("  - https://localhost:8080/       (digitalengn)")
        print("  - https://localhost:8080/plan   (openproject)")
        print("  - http://localhost:8080/git    (gitlab)")

        # Also show Ingress hosts if any are specifically defined
        result = subprocess.run(
            [
                "kubectl",
                "get",
                "ingress",
                "-A",
                "-o",
                "jsonpath={range .items[*].spec.rules[*]}{.host}{'\\n'}{end}",
            ],
            capture_output=True,
            text=True,
            env=env,
        )
        hosts = sorted(list(set(result.stdout.strip().split("\n"))))
        defined_hosts = [h for h in hosts if h]
        if defined_hosts:
            print("\nDefined Ingress Hosts (Internal):")
            for host in defined_hosts:
                print(f"  - http://{host}")

            ip_result = subprocess.run(
                ["minikube", "ip"], capture_output=True, text=True, env=env
            )
            minikube_ip = ip_result.stdout.strip()
            print(
                f"\nNote: To use defined hosts, map them to Minikube IP {minikube_ip} in /etc/hosts."
            )

        print("\nPress Ctrl+C to stop the port-forward and exit.")

        # Keep the script running
        while True:
            time.sleep(1)

    except subprocess.CalledProcessError as e:
        print(f"Error during deployment: {e}", file=sys.stderr)
        if port_forward_proc:
            port_forward_proc.terminate()
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        if port_forward_proc:
            port_forward_proc.terminate()
        sys.exit(1)


if __name__ == "__main__":
    main()
