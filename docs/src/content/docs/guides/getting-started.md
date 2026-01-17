---
title: Getting Started
description: How to set up and start developing in the DigitalEngn monorepo.
---

## Prerequisites

Before you begin, ensure you have the following tools installed:

- **Node.js & npm**: For TypeScript projects.
- **Python 3.12+**: For the `engn` CLI and BDD tests.
- **uv**: Python package manager.
- **Docker**: Required for Kubernetes infrastructure.
- **Minikube & kubectl**: For local Kubernetes development.

## Initial Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/jondavid-black/digitalengn.git
   cd digitalengn
   ```

2. **Install TypeScript dependencies**:
   ```bash
   npm install
   ```

3. **Set up Python environment**:
   ```bash
   uv sync
   ```

4. **Activate environment**:
   ```bash
   source activate.sh
   ```

## Running Tests

### Automated Acceptance Tests (BDD)
Run the top-level features using Behave:
```bash
uv run behave
```

### TypeScript Tests
Run tests for specific workspaces:
```bash
npm test -w digitalengn
npm test -w docsengn
```
