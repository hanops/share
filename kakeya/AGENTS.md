# Kakeya Agent Instructions

These instructions apply to files under `kakeya/` in addition to the repository-level `AGENTS.md`.

## Page model

- Keep `index.html` independently publishable and preserve its single-file HTML/CSS/JavaScript structure.
- Keep Three.js and OrbitControls versions explicit and mutually compatible.
- Preserve the loading/error layer, `window.__errs`, scene groups, scene switcher, animation loop, and resize handling when changing rendering code.
- Reuse existing Canvas and Three.js helpers before adding another rendering dependency.
- Respect the 960 px, 640 px, and 380 px responsive breakpoints and the mobile HUD drawer behavior.

## Content and export rules

- Treat theorem statements, dimensions, proof attribution, biographies, dates, prizes, and open-problem status as source-sensitive facts.
- Do not infer mathematical correctness from a visually plausible animation.
- Keep generated GIFs under ignored output paths; do not commit exports unless the user explicitly requests them.
- Changes to the optional MoWen exporter must preserve its declared output dimensions, loop behavior, and deterministic rendering unless the user requests a format change.

## Verification

After changes, run `make check` from the repository root and inspect:

- all four navigation tabs;
- the play/pause and range controls in Scenes 01–03;
- the Three.js loading failure state;
- the timeline scroll and reveal behavior;
- desktop and 390 × 844 mobile layouts;
- the mobile drawer, console errors, and horizontal overflow.

If the export script changes, run it only when Pillow and the referenced local fonts are available, then inspect at least one generated animation rather than relying only on process exit status.
