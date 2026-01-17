---
title: Project Structure
description: Overview of the DigitalEngn monorepo layout and purpose of each directory.
---

The DigitalEngn monorepo is organized into several key areas, each serving a specific role in the ecosystem.

## Directories

### `digitalengn/`
The primary TypeScript web application built with SvelteKit. It handles workspace and project management.

### `docsengn/`
A specialized TypeScript web application for document and slide editing.

### `engn/`
A Python CLI application designed for AI agent integration and support.

### `infrastructure/`
Contains Kubernetes configuration and scripts for managing the deployment environment locally using Minikube.

### `mbse/`
Stores Systems Modeling Language (SysML v2) architecture details, providing a formal model of the system.

### `docs/`
The project documentation site, built with Astro Starlight and hosted on GitHub Pages.

### `features/`
Top-level Behavior Driven Development (BDD) tests using the Behave library.

## Configuration Files

- `package.json`: Root npm workspace configuration.
- `pyproject.toml`: Root Python project configuration for BDD and dev tools.
- `activate.sh`: Shell script to set up the development environment path.
- `AGENTS.md`: Guidelines and instructions for AI agents operating in this repo.
