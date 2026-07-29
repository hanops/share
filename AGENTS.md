# Agent Instructions

These instructions apply to the entire repository.

## Project model

- This is a zero-build GitHub Pages site.
- Each published page lives in its own directory as `index.html`.
- The root `index.html` is the registry for all top-level pages.
- Do not introduce a framework, package manager, bundler, or generated asset pipeline unless the user explicitly requests that architectural change.

## Change scope

- Keep edits narrowly scoped to the requested page or repository support file.
- Preserve the single-file page model unless a change clearly requires shared assets.
- When adding a top-level page, add its directory link to the root index.
- Do not edit unrelated copy, visual styling, or interactions while fixing a focused issue.
- Do not add analytics, tracking, credentials, or third-party services without explicit authorization.

## Implementation rules

- Use semantic HTML where practical and keep `lang`, UTF-8 charset, viewport metadata, and a descriptive title on every page.
- Keep local links relative so the site works both locally and under the `/share/` GitHub Pages base path.
- Respect existing responsive breakpoints and `prefers-reduced-motion`.
- External runtime dependencies must use HTTPS and an explicit version.
- Treat factual product, scientific, biographical, award, and certification claims as source-sensitive content. Verify them before changing them; do not invent missing citations or data.
- Maintain compatibility with current evergreen browsers. The repository tooling must remain compatible with Python 3.9+.

## Verification

Run:

```bash
make check
```

For visual or interaction changes, also serve the site locally with `make serve` and inspect:

- the affected page at a desktop viewport;
- the affected page at a 390 × 844 mobile viewport;
- browser console errors;
- horizontal overflow and loading states.

Report only checks that actually ran. Do not claim factual accuracy from structural or visual verification alone.

## Delivery

- Do not commit, push, publish, tag, or change GitHub Pages settings unless the user explicitly requests that action.
- Keep generated screenshots, temporary captures, caches, and local environments out of version control.
- Never include AI attribution in commits, pull requests, issues, or public page content.
