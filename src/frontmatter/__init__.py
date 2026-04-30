"""Reusable frontmatter normalization and conversion logic."""

from __future__ import annotations

import json
from pathlib import Path

import yaml

from ..sparql import (
    parse_frontmatter,
    ensure_context,
)

def frontmatter_to_jsonld(file_path: Path) -> dict | None:
    """Parse and add context to frontmatter."""
    data = parse_frontmatter(file_path.read_text(encoding="utf-8"))
    if not data:
        return None
    return ensure_context(data)


def convert_all(
    wiki_dir: Path,
    dry_run: bool = False,
) -> dict:
    """Convert all .md files to JSON-LD and return a summary."""
    results = {
        "converted": [],
        "no_frontmatter": [],
        "errors": [],
    }

    for md_file in sorted(wiki_dir.glob("*.md")):
        try:
            jsonld = frontmatter_to_jsonld(md_file)
            if jsonld:
                results["converted"].append({
                    "file": md_file.name,
                    "@type": jsonld.get("@type"),
                })
            else:
                results["no_frontmatter"].append(md_file.name)
        except Exception as e:
            results["errors"].append({"file": md_file.name, "error": str(e)})

    return results


def normalize_frontmatter_str(content: str) -> str:
    """Normalize frontmatter keys in a markdown string.

    Returns the content unchanged if nothing was fixed.
    """
    if not content.startswith("---"):
        return content

    parts = content.split("---", 2)
    if len(parts) < 2:
        return content

    frontmatter_text = parts[1].strip()
    is_json = frontmatter_text.strip().startswith("{")

    try:
        data = json.loads(frontmatter_text) if is_json else yaml.safe_load(frontmatter_text)
    except Exception:
        return content

    if not isinstance(data, dict):
        return content

    fixed = False
    if "@context" not in data:
        data["@context"] = {
            "@vocab": "https://schema.org/",
            "wiki": "https://{{owner}}.github.io/{{repo}}/wiki/",
        }
        fixed = True
    elif isinstance(data["@context"], dict):
        for k, v in {"@vocab": "https://schema.org/", "wiki": "https://{{owner}}.github.io/{{repo}}/wiki/"}.items():
            if k not in data["@context"]:
                data["@context"][k] = v
                fixed = True

    if not fixed:
        return content

    new_fm = json.dumps(data, indent=2) if is_json else yaml.dump(data, default_flow_style=False)
    return f"---\n{new_fm}\n---" + (parts[2] if len(parts) > 2 else "")


def normalize_all(wiki_dir: Path, dry_run: bool = False) -> dict:
    """Normalize frontmatter across all wiki files."""
    results = {"fixed": 0, "skipped": 0, "errors": []}

    for md_file in sorted(wiki_dir.glob("*.md")):
        try:
            original = md_file.read_text(encoding="utf-8")
            normalized = normalize_frontmatter_str(original)
            if normalized != original:
                results["fixed"] += 1
                if not dry_run:
                    md_file.write_text(normalized, encoding="utf-8")
            else:
                results["skipped"] += 1
        except Exception as e:
            results["errors"].append({"file": md_file.name, "error": str(e)})

    return results
