#!/usr/bin/env python3
"""Build a Sites-compatible worker from the existing static HTML pages."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
SERVER_DIR = DIST / "server"
HOSTING_SOURCE = ROOT / ".openai" / "hosting.json"

PAGES = {
    "/": ROOT / "index.html",
    "/index.html": ROOT / "index.html",
    "/ergonomic-chair/": ROOT / "ergonomic-chair" / "index.html",
    "/ergonomic-chair/index.html": ROOT / "ergonomic-chair" / "index.html",
    "/kakeya/": ROOT / "kakeya" / "index.html",
    "/kakeya/index.html": ROOT / "kakeya" / "index.html",
}


def read_html_pages() -> Dict[str, str]:
    pages: Dict[str, str] = {}
    for route, path in PAGES.items():
        pages[route] = path.read_text(encoding="utf-8")
    return pages


def build_worker_source(pages: Dict[str, str]) -> str:
    page_map = json.dumps(pages, ensure_ascii=False, indent=2)
    return f"""/* eslint-disable */
const pages = {page_map};

function htmlResponse(html, status = 200) {{
  return new Response(html, {{
    status,
    headers: {{
      "content-type": "text/html; charset=utf-8",
      "cache-control": "no-store",
    }},
  }});
}}

export default {{
  async fetch(request) {{
    const url = new URL(request.url);
    const pathname = url.pathname;

    if (pathname in pages) {{
      return htmlResponse(pages[pathname]);
    }}

    if (pathname === "/ergonomic-chair" || pathname === "/kakeya") {{
      return htmlResponse(pages[`${{pathname}}/`]);
    }}

    if (pathname === "/") {{
      return htmlResponse(pages["/"]);
    }}

    return htmlResponse(pages["/"], 404);
  }},
}};
"""


def main() -> int:
    pages = read_html_pages()
    SERVER_DIR.mkdir(parents=True, exist_ok=True)
    (DIST / ".openai").mkdir(parents=True, exist_ok=True)

    (SERVER_DIR / "index.js").write_text(
        build_worker_source(pages), encoding="utf-8"
    )
    (DIST / ".openai" / "hosting.json").write_text(
        HOSTING_SOURCE.read_text(encoding="utf-8"), encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
