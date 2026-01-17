# Shared Assets Strategy

To maintain core shared assets like favicons and branding images across multiple projects (`digitalengn`, `docsengn`, `docs`), we will use a central repository at the root of the monorepo.

## Implementation Details

1.  **Central Directory**: A `shared-assets/` directory at the root will store all common assets.
2.  **Linking Mechanism**: Assets will be linked into each project's static asset directory:
    - `digitalengn/static/shared` -> `shared-assets/`
    - `docsengn/static/shared` -> `shared-assets/`
    - `docs/public/shared` -> `shared-assets/`
3.  **Automation**: A script `scripts/sync-assets.sh` will be provided to set up these links. This script can be run manually or as part of a post-install hook.

## Pros and Cons

| Approach | Pros | Cons |
| :--- | :--- | :--- |
| **Symlinks (Selected)** | Single source of truth, transparent to build tools. | Can be tricky on Windows. |
| **Copy Script** | Robust across platforms. | File duplication, needs sync on changes. |
| **NPM Package** | Idiomatic for monorepo. | Complex build tool configuration required. |

## Usage

To sync assets:
```bash
./scripts/sync-assets.sh
```
