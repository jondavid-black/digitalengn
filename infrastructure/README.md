# Local Infrastructure Environment

This directory manages the Kubernetes configuration for the DigitalEngn monorepo.
Local testing is performed using **Minikube** with **Podman** as the container runtime.

## Design Goals

The infrastructure is designed to support both persistent team services and dynamic, on-demand developer environments.

### Persistent Applications
These applications are maintained as core services within the cluster:
- **DigitalEngn**: The top-level landing page, dashboard, and navigation assistant.
- **OpenProject**: Project management and collaboration.
- **GitLab**: Source code management and CI/CD registry. Includes configured GitLab Runners for pipeline support.

### Dynamic Applications
These are user and project-specific applications that launch on-demand and scale to zero when not in use:
- **VS Code**: Web-based IDE.
- **PenPot**: Design and prototyping.
- **DocsEngn**: Document and slide editing.

**Architecture for Dynamic Apps:**
- **Encapsulation**: Each user/project environment is contained within a single Pod.
- **Shared Storage**: Applications within the same Pod share an underlying file system (EmptyDir or PV) containing a local clone of the project's repository from GitLab.
- **Scaling**: Managed via Kubernetes-native scaling (e.g., KEDA or custom controller) to optimize resource usage by scaling to zero.

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
