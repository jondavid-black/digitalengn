#!/bin/bash

# Ensure ~/bin is in PATH
export PATH=$PATH:$HOME/bin

echo "Checking prerequisites..."

if ! command -v podman &> /dev/null; then
    echo "Error: podman is not installed."
    exit 1
fi

if ! command -v minikube &> /dev/null; then
    echo "Minikube not found. Installing..."
    mkdir -p ~/bin
    curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
    chmod +x minikube-linux-amd64
    mv minikube-linux-amd64 ~/bin/minikube
fi

if ! command -v kubectl &> /dev/null; then
    echo "kubectl not found. Installing..."
    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
    chmod +x kubectl
    mv kubectl ~/bin/
fi

echo "Starting Minikube with Podman driver..."
minikube start --driver=podman --rootless

echo "Local environment is ready!"
kubectl cluster-info
