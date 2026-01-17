# Agent Guidelines for DigitalEngn

This document provides comprehensive instructions for AI agents operating within the DigitalEngn monorepo. Follow these guidelines strictly to ensure code quality, consistency, and stability across our TypeScript and Python services.

## Project Overview

DigitalEngn is a monorepo containing:
- `digitalengn/`: TypeScript web application for workspace and project management.
- `docsengn/`: TypeScript web application for document and slide editing.
- `engn/`: Python CLI application for AI agent integration and support.
- `infrastructure/`: Kubernetes configuration and management (Minikube/kubectl).

## Development Environment & Toolchain

This project expects the host system to provide certain tools. If these aren't present inform the user and provide instructions for them to properly install the required tools in their environment.

### Core Environment Tools
| Tool | Check Command | Initialization Command | Description |
| :--- | :--- | :--- | :--- |
| **UV** | `uv --version` | `uv init` | Modern python package manager. |
| **Beads** | `bd --version` | `bd init` | AI native issue tracker. |
| **OpenCode** | `opencode --version` | `/init` (in OpenCode TUI) | Open source AI Agent. |

### Core Project Tools (Python)
If these tools aren't present in the Python environment, add them to the project's dev dependencies.

| Tool | Install Command | Description |
| :--- | :--- | :--- |
| **Python** | `uv python install 3.12` | Python 3.12 or above. |
| **Pytest** | `uv add pytest --dev` | Unit test runner. |
| **Behave** | `uv add behave --dev` | BDD acceptance testing. |
| **Ruff** | `uv add ruff --dev` | Linting and formatting. |
| **Pyright** | `uv add pyright --dev` | Type checking. |
| **MkDocs** | `uv add mkdocs --dev` | Documentation site generator. |

## Build, Lint, and Test Commands

### Python Projects (`engn`)
Uses **uv** for dependency management. All commands should be executed via `uv run`.

| Action | Command | Description |
| :--- | :--- | :--- |
| **Unit Tests** | `uv run pytest` | Run all unit tests with coverage |
| **BDD Tests** | `uv run behave` | Run acceptance tests (features) |
| **Linting** | `uv run ruff check .` | Check for linting errors |
| **Formatting** | `uv run ruff format .` | Auto-format code |
| **Type Check** | `uv run pyright` | Run static type checking |
| **Specific Test** | `uv run pytest <file>::<func>` | Run specific test function |
| **BDD Feature** | `uv run behave features/<pkg>/<use_case>.feature` | Run specific feature |

### TypeScript Projects (`digitalengn`, `docsengn`)
Uses **npm** workspaces and **SvelteKit**. Run from root or with `-w`.

| Action | Command | Description |
| :--- | :--- | :--- |
| **Install** | `npm install` | Install all dependencies |
| **Build** | `npm run build -w <pkg>` | Build specific service |
| **Test** | `npm test -w <pkg>` | Run tests for a service |
| **Lint** | `npm run lint -w <pkg>` | Lint specific service |
| **Dev** | `npm run dev -w <pkg>` | Start development server |
| **Check** | `npm run check -w <pkg>` | Run svelte-check |

## Issue Tracking (beads)

This project uses **bd (beads)** for issue tracking to ensure work is visible.
- `bd ready` - Find unblocked work.
- `bd create "Title" --type task --priority 2` - Create issue.
- `bd close <id>` - Complete work.
- `bd sync` - Sync with git (run at session end).
- Run `bd prime` for full workflow details.

## Standard Process

1. **Plan**: Write a feature or bug in **bd** defining the work. Decompose into tasks.
2. **Implement**: Execute work. New code MUST have unit tests. New features should have BDD acceptance tests.
3. **Verify**: Run `ruff check`, `ruff format`, `pytest`, `pyright`, and `behave`. For TS, run `npm run lint` and `npm test`.
4. **Track**: Update status in **bd** as you work. Commit and push when complete.

## Code Style & Conventions

### Python Standards
- **Style**: Adhere strictly to **PEP 8**. We use `ruff` for formatting and linting.
- **Type Safety**: Mandatory type hints for all new code. Use modern generics (e.g., `list[str]`). Verify with `pyright`.
- **Naming**: `snake_case` for vars/funcs, `PascalCase` for classes, `UPPER_CASE` for constants. Prefix private members with `_`.
- **Imports**: Absolute imports for internal modules. Sort using `ruff`. Group standard library, third-party, and local separately.
- **Error Handling**: Use specific, custom exception classes. Catch narrowly and provide context when re-raising. Fail fast.

### TypeScript Standards
- **Strictness**: `strict: true` is enabled. Provide explicit types for exported members.
- **Framework**: **SvelteKit** is the preferred framework for web applications.
- **Structure**: Source in `src/`, UI in `src/components/`, hooks in `src/hooks/`.
- **Naming**: `camelCase` for vars/funcs, `PascalCase` for Components/Classes.
- **Formatting**: 2-space indentation.

### Project Structure (Python)
- `docs/`: Application/library documentation.
- `src/` or `<pkg>/`: Source code and modules.
- `tests/`: Unit tests mirroring the source structure.
- `features/`: Gherkin feature files for BDD.

## Landing the Plane (Session Completion)

**MANDATORY WORKFLOW** - Work is NOT complete until `git push` succeeds:
1. **File follow-up issues** for remaining work in **bd**.
2. **Run quality gates**: Tests, linters, builds.
3. **Update issue status**: Close finished work in **bd**.
4. **PUSH TO REMOTE**:
   ```bash
   git pull --rebase
   bd sync
   git push
   git status  # MUST show "up to date with origin"
   ```
5. **Clean up**: Clear stashes, prune remote branches.
6. **Hand off**: Provide context for the next session.

**CRITICAL RULES**: Work is NOT complete until `git push` succeeds. NEVER stop before pushing.

## AI Agent Specifics
- **Context**: Consider surrounding code and monorepo structure.
- **Safety**: Explain impact before modifying filesystem or running shell commands.
- **Dependencies**: Do not introduce new dependencies without explicit instruction.
- **Hallucinations**: Verify library APIs before generating code.
