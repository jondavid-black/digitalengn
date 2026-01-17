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
        # Check if minikube is running
        result = subprocess.run(
            ["minikube", "status"], capture_output=True, text=True, env=env
        )

        if "Running" in result.stdout or "Stopped" in result.stdout:
            print("Stopping Minikube cluster...")
            run_command(["minikube", "stop"], env=env)
            print("Minikube stopped successfully.")
        else:
            print("Minikube is not running or already stopped.")

    except subprocess.CalledProcessError as e:
        print(f"Error during shutdown: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
