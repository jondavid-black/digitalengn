# Local Infrastructure Environment

This directory manages the Kubernetes configuration for the DigitalEngn monorepo.
Local testing is performed using **Minikube** with **Podman** as the container runtime.

## Prerequisites

- **Podman**: Used for building and managing containers.
- **Minikube**: Local Kubernetes cluster.
- **kubectl**: Kubernetes command-line tool.

## Setup Instructions

If you haven't already, you can start the local environment with:

```bash
minikube start --driver=podman --rootless
```

## Tools Installed

The following tools have been installed in `~/bin`:
- `minikube`
- `kubectl`

Ensure `~/bin` is in your `PATH`.

## Building Images

To build images directly into the Minikube registry using Podman:

```bash
eval $(minikube -p minikube docker-env --shell bash)
# Note: Since we use podman, you might need to use minikube's podman-env
eval $(minikube podman-env)
podman build -t my-image .
```

## Managing Cluster

- `minikube status`: Check cluster status.
- `minikube dashboard`: Open the Kubernetes dashboard.
- `kubectl get pods -A`: List all pods.
