import os
import subprocess
import time
import sys
import signal


def run_command(command, env=None):
    print(f"Executing: {' '.join(command)}")
    subprocess.run(command, check=True, env=env)


def main():
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

        # Ensure ingress addon is enabled
        print("Enabling ingress addon...")
        run_command(["minikube", "addons", "enable", "ingress"], env=env)

        # Apply kustomization
        print("Applying infrastructure configuration...")
        run_command(["kubectl", "apply", "-k", "infrastructure/k8s/base"], env=env)

        # Wait for ingress controller to be ready
        print("Waiting for ingress controller to be ready...")
        run_command(
            [
                "kubectl",
                "wait",
                "--namespace",
                "ingress-nginx",
                "--for=condition=ready",
                "pod",
                "--selector=app.kubernetes.io/component=controller",
                "--timeout=90s",
            ],
            env=env,
        )

        print("Infrastructure deployed successfully.")

        # Start port-forward for ingress controller
        print("Starting port-forward on 0.0.0.0:8080...")
        port_forward_proc = subprocess.Popen(
            [
                "kubectl",
                "port-forward",
                "--address",
                "0.0.0.0",
                "-n",
                "ingress-nginx",
                "service/ingress-nginx-controller",
                "8080:80",
            ],
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        # Wait for port-forward to be ready
        time.sleep(5)
        if port_forward_proc.poll() is not None:
            print(
                "Error: Port-forward failed to start. Port 8080 might be in use.",
                file=sys.stderr,
            )
            sys.exit(1)

        print("\nDeployment complete and port-forwarding active.")
        print("Core infrastructure is accessible on the network at port 8080.")
        print("Examples:")
        print("  - http://localhost:8080/       (digitalengn)")
        print("  - http://localhost:8080/plan   (openproject)")
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
