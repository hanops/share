#!/usr/bin/env python3
"""Validate the repository's zero-build HTML page structure."""

from html.parser import HTMLParser
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_META_NAMES = {"viewport"}
SKIPPED_DIRECTORIES = {".git", ".venv", "__pycache__"}


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.declarations: List[str] = []
        self.html_lang: Optional[str] = None
        self.charset: Optional[str] = None
        self.meta_names: Set[str] = set()
        self.title_depth = 0
        self.title_parts: List[str] = []
        self.ids: Dict[str, int] = {}
        self.references: List[Tuple[str, str]] = []

    def handle_decl(self, decl: str) -> None:
        self.declarations.append(decl.lower())

    def handle_starttag(
        self, tag: str, attrs: List[Tuple[str, Optional[str]]]
    ) -> None:
        values = {name.lower(): value for name, value in attrs}

        if tag == "html":
            self.html_lang = values.get("lang")
        elif tag == "meta":
            if values.get("charset"):
                self.charset = values["charset"]
            if values.get("name"):
                self.meta_names.add(values["name"].lower())
        elif tag == "title":
            self.title_depth += 1

        element_id = values.get("id")
        if element_id:
            self.ids[element_id] = self.ids.get(element_id, 0) + 1

        for attribute in ("href", "src"):
            reference = values.get(attribute)
            if reference:
                self.references.append((attribute, reference))

    def handle_endtag(self, tag: str) -> None:
        if tag == "title" and self.title_depth:
            self.title_depth -= 1

    def handle_data(self, data: str) -> None:
        if self.title_depth:
            self.title_parts.append(data)


def html_files() -> List[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*.html")
        if not any(part in SKIPPED_DIRECTORIES for part in path.parts)
    )


def local_target(page: Path, reference: str) -> Optional[Path]:
    if reference.startswith(("#", "//")):
        return None

    parsed = urlparse(reference)
    if parsed.scheme or parsed.netloc or not parsed.path:
        return None

    path_text = unquote(parsed.path)
    if path_text.startswith("/"):
        target = ROOT / path_text.lstrip("/")
    else:
        target = page.parent / path_text

    if path_text.endswith("/"):
        target = target / "index.html"

    return target.resolve()


def validate_page(page: Path) -> List[str]:
    relative = page.relative_to(ROOT)
    errors: List[str] = []
    parser = PageParser()

    try:
        parser.feed(page.read_text(encoding="utf-8"))
        parser.close()
    except (OSError, UnicodeError) as exc:
        return [f"{relative}: cannot read as UTF-8: {exc}"]

    if "doctype html" not in parser.declarations:
        errors.append(f"{relative}: missing <!DOCTYPE html>")
    if not parser.html_lang:
        errors.append(f"{relative}: missing html[lang]")
    if (parser.charset or "").lower().replace("-", "") != "utf8":
        errors.append(f"{relative}: missing UTF-8 charset metadata")
    if not REQUIRED_META_NAMES.issubset(parser.meta_names):
        errors.append(f"{relative}: missing viewport metadata")
    if not "".join(parser.title_parts).strip():
        errors.append(f"{relative}: missing non-empty <title>")

    for element_id, count in sorted(parser.ids.items()):
        if count > 1:
            errors.append(f"{relative}: duplicate id {element_id!r} ({count} uses)")

    root_resolved = ROOT.resolve()
    for attribute, reference in parser.references:
        target = local_target(page, reference)
        if target is None:
            continue
        try:
            target.relative_to(root_resolved)
        except ValueError:
            errors.append(
                f"{relative}: {attribute} escapes repository root: {reference!r}"
            )
            continue
        if not target.exists():
            errors.append(
                f"{relative}: broken local {attribute} {reference!r}"
            )

    return errors


def validate_root_registry() -> List[str]:
    errors: List[str] = []
    root_page = ROOT / "index.html"
    parser = PageParser()
    parser.feed(root_page.read_text(encoding="utf-8"))
    parser.close()

    root_hrefs = {reference for attribute, reference in parser.references if attribute == "href"}
    for child_index in sorted(ROOT.glob("*/index.html")):
        directory = child_index.parent.name
        accepted = {f"./{directory}/", f"{directory}/"}
        if root_hrefs.isdisjoint(accepted):
            errors.append(
                f"index.html: missing registry link for {directory}/index.html"
            )

    return errors


def main() -> int:
    pages = html_files()
    errors: List[str] = []

    if not pages:
        errors.append("no HTML pages found")
    else:
        for page in pages:
            errors.extend(validate_page(page))

    if (ROOT / "index.html").exists():
        errors.extend(validate_root_registry())
    else:
        errors.append("missing root index.html")

    if errors:
        print(f"check failed with {len(errors)} error(s):")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"check passed: {len(pages)} HTML page(s) validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
