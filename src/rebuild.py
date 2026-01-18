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
        print("--- Starting Full Rebuild ---")

        # 1. Run clean
        run_command(["uv", "run", "clean"], env=env)

        # 2. Run launch --build
        run_command(["uv", "run", "launch", "--build"], env=env)

        print("\n--- Rebuild Complete ---")

    except subprocess.CalledProcessError as e:
        print(f"Error during rebuild: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
