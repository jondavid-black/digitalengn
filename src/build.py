import os
import subprocess
import sys
import json


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

        for service, paths in services.items():
            version = get_version(paths["package_json"])
            print(f"\n--- Building {service} (version: {version}) ---")

            image_name = service
            version_tag = f"{image_name}:{version}"
            latest_tag = f"{image_name}:latest"

            # Build using podman
            run_command(
                [
                    "podman",
                    "build",
                    "-t",
                    version_tag,
                    "-t",
                    latest_tag,
                    "-f",
                    paths["dockerfile"],
                    ".",
                ],
                env=env,
            )

            print(f"\n--- Loading {service} into Minikube ---")
            # Load both tags to ensure consistency
            run_command(["minikube", "image", "load", version_tag], env=env)
            run_command(["minikube", "image", "load", latest_tag], env=env)

        print("\nAll images built and loaded successfully with version tracking.")

    except subprocess.CalledProcessError as e:
        print(f"\nError during build/load: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
