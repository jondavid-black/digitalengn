import os
import subprocess
import time
import sys


def run_command(command, env=None):
    print(f"Executing: {' '.join(command)}")
    subprocess.run(command, check=True, env=env)


def main():
    # Add ~/bin to PATH for subprocess calls (as seen in smoke_test_steps.py)
    env = os.environ.copy()
    home_bin = os.path.expanduser("~/bin")
    if home_bin not in env["PATH"]:
        env["PATH"] = f"{home_bin}:{env['PATH']}"

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
        print("Waiting 60 seconds for applications to start (as per smoke tests)...")
        time.sleep(60)

        print("\nDeployment complete. Core infrastructure should be accessible.")
        print("You can run 'kubectl get pods -A' to check status.")

    except subprocess.CalledProcessError as e:
        print(f"Error during deployment: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
        sys.exit(0)


if __name__ == "__main__":
    main()
