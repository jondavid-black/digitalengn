import os
import subprocess
import sys


def run_command(command, env=None):
    print(f"Executing: {' '.join(command)}")
    subprocess.run(command, check=True, env=env)


def main():
    # Add ~/bin to PATH for subprocess calls
    env = os.environ.copy()
    home_bin = os.path.expanduser("~/bin")
    if home_bin not in env["PATH"]:
        env["PATH"] = f"{home_bin}:{env['PATH']}"

    services = {
        "digitalengn": "digitalengn/Dockerfile",
        "docsengn": "docsengn/Dockerfile",
    }

    try:
        # Check if minikube is running
        result = subprocess.run(
            ["minikube", "status"], capture_output=True, text=True, env=env
        )
        if "Running" not in result.stdout:
            print(
                "Error: Minikube is not running. Please run 'uv run launch' first or start Minikube.",
                file=sys.stderr,
            )
            sys.exit(1)

        for service, dockerfile in services.items():
            print(f"\n--- Building {service} ---")
            # Build using podman (since that's what minikube is using)
            # We use the root as context as indicated by the Dockerfiles
            run_command(
                ["podman", "build", "-t", f"{service}:latest", "-f", dockerfile, "."],
                env=env,
            )

            print(f"\n--- Loading {service} into Minikube ---")
            run_command(["minikube", "image", "load", f"{service}:latest"], env=env)

        print("\nAll images built and loaded successfully.")

    except subprocess.CalledProcessError as e:
        print(f"\nError during build/load: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
