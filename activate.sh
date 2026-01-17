#!/bin/bash

# This script mimics a virtual environment activation for the DigitalEngn monorepo.
# Usage: source activate.sh

if [[ "$0" == "$BASH_SOURCE" ]]; then
    echo "Error: This script must be sourced."
    echo "Usage: source activate.sh"
    exit 1
fi

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOCAL_BIN="$HOME/bin"

# Add local bin to PATH if not already there
if [[ ":$PATH:" != *":$LOCAL_BIN:"* ]]; then
    export PATH="$LOCAL_BIN:$PATH"
    echo "Added $LOCAL_BIN to PATH"
fi

# Set project-specific environment variables
export DIGITALENGN_ROOT="$REPO_ROOT"
export KUBECONFIG="$HOME/.kube/config"

echo "DigitalEngn environment activated."
echo "Commands available: minikube, kubectl"

# Optional: deactivate function
deactivate_engn() {
    # This is a basic PATH restoration. A more robust one would store the old PATH.
    export PATH="${PATH//"$LOCAL_BIN:"/}"
    unset DIGITALENGN_ROOT
    unset -f deactivate_engn
    echo "DigitalEngn environment deactivated."
}
