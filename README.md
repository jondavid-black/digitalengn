# DigitalEngn Monorepo

A collection of tools and integrating infrastructure.

## Structure

- `digitalengn/`: TypeScript web application for workspace and project management.
- `docsengn/`: TypeScript web application for document and slide editing.
- `engn/`: Python CLI application for AI agent integration and support.
- `infrastructure/`: Kubernetes configuration and management.

## Development

### TypeScript

This repo uses npm workspaces for TypeScript projects. Run `npm install` at the root.

### Python

The `engn` project uses `pyproject.toml`.

### Environment Setup

To add tools like `minikube` and `kubectl` to your path for this session:

```bash
source activate.sh
```

Alternatively, if you have [direnv](https://direnv.net/) installed, the `.envrc` file will handle this automatically when you enter the directory.

Install direnv:

```bash
sudo apt-get install direnv
```

Add a shell hook to your .bashrc configuration:

```bash
echo 'eval "$(direnv hook bash)"' >> ~/.bashrc
```

Authorize the `digitalengn` directory within direnv:

```bash
# Inside the 'digitalengn' directory
direnv allow
```

## Issue Tracking

The DigitalEngn project uses Beads (bd) for AI-native issue tracking.
Run `bdui start` for a simple, human-centric [web UI](http://127.0.0.1:3000) of the Beads backlog.
