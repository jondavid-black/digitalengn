import os
import subprocess
import sys
import json
import time


def run_command(command, env=None):
    print(f"Executing: {' '.join(command)}")
    subprocess.run(command, check=True, env=env)


def get_version(package_json_path):
    try:
        with open(package_json_path, "r") as f:
            data = json.load(f)
            return data.get("version", "0.1.0")
    except Exception as e:
        print(f"Warning: Could not read version from {package_json_path}: {e}")
        return "0.1.0"


def main():
    # Add ~/bin to PATH for subprocess calls
    env = os.environ.copy()
    home_bin = os.path.expanduser("~/bin")
    if home_bin not in env["PATH"]:
        env["PATH"] = f"{home_bin}:{env['PATH']}"

    services = {
        "digitalengn": {
            "dockerfile": "digitalengn/Dockerfile",
            "package_json": "digitalengn/package.json",
        },
        "docsengn": {
            "dockerfile": "docsengn/Dockerfile",
            "package_json": "docsengn/package.json",
        },
    }

    try:
        # Check if minikube is running with retry logic
        minikube_ready = False
        for attempt in range(5):
            result = subprocess.run(
                ["minikube", "status"], capture_output=True, text=True, env=env
            )
            if "Running" in result.stdout:
                print("Minikube is running.")
                minikube_ready = True
                break

            print(
                f"Error: Minikube is not running. Please run 'uv run launch' first or start Minikube. (Attempt {attempt + 1}/5)"
            )
            if attempt < 4:
                print("Retrying in 5 seconds...")
                time.sleep(5)

        if not minikube_ready:
            print(
                "\nFailed to connect to Minikube after 5 attempts. Terminating.",
                file=sys.stderr,
            )
            sys.exit(1)

        for service, paths in services.items():
            version = get_version(paths["package_json"])
            print(f"\n--- Building {service} (version: {version}) ---")

            # Use minikube image build to build directly inside the cluster.
            # This is more robust than podman build + load when using rootless drivers.
            run_command(
                [
                    "minikube",
                    "image",
                    "build",
                    "-t",
                    f"{service}:{version}",
                    "-f",
                    paths["dockerfile"],
                    ".",
                ],
                env=env,
            )

            # Also tag as latest
            print(f"--- Tagging {service} as latest ---")
            run_command(
                [
                    "minikube",
                    "image",
                    "build",
                    "-t",
                    f"{service}:latest",
                    "-f",
                    paths["dockerfile"],
                    ".",
                ],
                env=env,
            )

        print("\nAll images built successfully within Minikube with version tracking.")

    except subprocess.CalledProcessError as e:
        print(f"\nError during build: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
