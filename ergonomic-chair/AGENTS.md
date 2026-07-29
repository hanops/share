# Ergonomic Chair Agent Instructions

These instructions apply to files under `ergonomic-chair/` in addition to the repository-level `AGENTS.md`.

## Page model

- Keep `index.html` independently publishable and preserve the single-file implementation.
- Preserve the 790 px long-page composition and the existing 12-section content sequence unless the user requests a structural redesign.
- Reuse the existing design tokens, inline SVG language, reveal classes, and interaction patterns before adding new ones.
- Do not add product image files or a JavaScript framework for a focused page edit.

## Content rules

- Treat prices, specifications, ergonomic percentages, certifications, warranties, review counts, ratings, and customer quotes as source-sensitive claims.
- Do not invent supporting data or silently turn demonstration copy into verified product facts.
- Keep the distinction between visual concept work and a production commerce page explicit.

## Verification

After changes, run `make check` from the repository root and inspect:

- the full page at a desktop viewport;
- the full page at 390 × 844;
- initial and scrolled reveal states;
- the sticky purchase bar threshold;
- `prefers-reduced-motion`;
- console errors and horizontal overflow.
