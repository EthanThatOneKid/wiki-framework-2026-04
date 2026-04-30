"""Validate wiki frontmatter against SHACL shapes."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from rdflib import Graph

from ..sparql import frontmatter_from_path, frontmatter_to_graph

try:
    from pyshacl import validate
except ImportError:
    # We will raise RuntimeError inside functions if called and pyshacl is missing
    validate = None

WIKI_DIR = Path("wiki")
SHAPES_DIR = Path("shapes")


def load_shapes(shapes_dir: Path = SHAPES_DIR) -> Graph:
    """Load all SHACL shapes (.ttl files) into a Graph."""
    shapes_graph = Graph()
    shapes_graph.bind("sh", "http://www.w3.org/ns/shacl#")
    shapes_graph.bind("schema", "https://schema.org/")

    for shape_file in sorted(shapes_dir.glob("*.ttl")):
        try:
            shapes_graph.parse(shape_file, format="turtle")
        except Exception as e:
            print(f"Warning: failed to parse {shape_file.name}: {e}")

    return shapes_graph




def validate_all(
    wiki_dir: Path = WIKI_DIR,
    shapes_dir: Path = SHAPES_DIR,
    verbose: bool = False,
) -> bool:
    """Validate all wiki pages against SHACL shapes."""
    # pyshacl import moved to module level
    if validate is None:
        raise RuntimeError("pyshacl not installed — run: uv add pyshacl")

    shapes_graph = load_shapes(shapes_dir)
    if not shapes_graph:
        raise RuntimeError(f"No shapes loaded from {shapes_dir}")

    data_graph = Graph()
    errors = []

    for md_file in sorted(wiki_dir.glob("*.md")):
        try:
            data = frontmatter_from_path(md_file)
            if data:
                data_graph += frontmatter_to_graph(data, file_id=md_file.stem)
        except Exception as e:
            errors.append((md_file.name, str(e)))

    conforms, results_graph, results_text = validate(
        data_graph,
        shapes_graph,
        inference="rdfs",
        abort_on_first_error=False,
    )

    if verbose:
        print(results_text)

    if errors:
        print(f"\nParse errors ({len(errors)}):")
        for name, err in errors:
            print(f"  {name}: {err}")

    return conforms


def validate_file(
    file_path: Path,
    shapes_dir: Path = SHAPES_DIR,
    verbose: bool = False,
) -> Optional[bool]:
    """Validate a single markdown file. Returns None if no frontmatter."""
    data = frontmatter_from_path(file_path)
    if not data:
        return None

    shapes_graph = load_shapes(shapes_dir)
    data_graph = frontmatter_to_graph(data)

    conforms, results_graph, results_text = validate(
        data_graph,
        shapes_graph,
        inference="rdfs",
    )

    if verbose:
        print(results_text)

    return conforms


def validate_summary(
    wiki_dir: Path = WIKI_DIR,
    shapes_dir: Path = SHAPES_DIR,
) -> dict:
    """Return a summary dict of validation results per file."""
    # pyshacl import moved to module level

    shapes_graph = load_shapes(shapes_dir)
    results = {"conforms": [], "fails": [], "errors": []}

    for md_file in sorted(wiki_dir.glob("*.md")):
        try:
            data = frontmatter_from_path(md_file)
            if not data:
                results["errors"].append({"file": md_file.name, "reason": "no frontmatter"})
                continue

            data_graph = frontmatter_to_graph(data)
            conforms, _, _ = validate(data_graph, shapes_graph, inference="rdfs")

            if conforms:
                results["conforms"].append(md_file.name)
            else:
                results["fails"].append(md_file.name)
        except Exception as e:
            results["errors"].append({"file": md_file.name, "reason": str(e)})

    return results

