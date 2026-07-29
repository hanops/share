# Agent Instructions

These instructions apply to the entire repository. When working inside a subproject, also follow the nearest nested `AGENTS.md`.

## Repository model

- This is a zero-build GitHub Pages repository containing independent subprojects.
- Each published subproject lives in its own top-level directory with an `index.html`, `README.md`, and `AGENTS.md`.
- The root `index.html` is the registry for published subprojects.
- Root tooling and configuration must stay generic. Project-specific instructions belong in that project's directory.
- Do not introduce a framework, package manager, bundler, or generated site pipeline unless the user explicitly requests an architectural change.

## Shared implementation rules

- Keep changes narrowly scoped and preserve unrelated worktree changes.
- When adding a top-level page, add it to the root index and give it local project documentation.
- Keep local page links compatible with both local serving and the `/share/` GitHub Pages base path.
- External runtime dependencies must use HTTPS and explicit versions.
- Do not add analytics, tracking, credentials, or third-party services without explicit authorization.
- Shared Python tooling must remain compatible with Python 3.9 or newer.

## Shared verification

Run `make check` for every repository change. For page changes, follow the additional visual and interaction checks in the subproject's `AGENTS.md`.

Only report checks that actually ran. Structural or visual checks do not establish the factual accuracy of page content.

## Delivery

- Do not commit, push, publish, tag, or change GitHub Pages settings unless the user explicitly requests that action.
- Keep generated screenshots, exports, caches, and local environments out of version control.
- Never include AI attribution in commits, pull requests, issues, or public page content.
