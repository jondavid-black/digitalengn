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

    try:
        print("Cleaning Minikube environment...")

        # We'll use 'minikube delete' to completely remove the cluster.
        # This ensures the next 'launch' reloads everything from baseline,
        # including re-creating disks/volumes.
        run_command(["minikube", "delete"], env=env)

        print("Minikube environment cleaned successfully.")
        print("The next 'uv run launch' will start from a fresh baseline.")

    except subprocess.CalledProcessError as e:
        print(f"Error during cleaning: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
