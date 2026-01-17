# Dynamic Application Scaling Strategy

Dynamic applications (VS Code, PenPot, DocsEngn) are designed to be user and project-specific.

## Shared File System
To allow multiple applications (IDE, Design, Docs) to access the same underlying git repository, they must be co-located within the same Kubernetes Pod. This allows them to share an `emptyDir` or a `PersistentVolume` via `volumeMounts`.

## Scale to Zero
We utilize **KEDA (Kubernetes Event-driven Autoscaling)** with the **HTTP Add-on** to manage scaling.
- Each dynamic environment is represented by a Deployment/Service pair.
- A KEDA `HTTPScaledObject` tracks incoming requests.
- If no requests are received for a specific period (e.g., 30 minutes), KEDA scales the Deployment to zero.
- Incoming requests trigger KEDA to scale the Deployment back to 1.

## Dynamic Provisioning
A custom controller or a simple automation script (triggered by DigitalEngn dashboard) will:
1. Create a new namespace or label for the user/project.
2. Apply the `dynamic-app-pod.yaml` manifest.
3. Initialize the shared volume by cloning the repository from GitLab.
