"""Query and validate the wiki with SPARQL and SHACL."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from .frontmatter import convert_all, normalize_all
from .shacl import validate_all, validate_file, validate_summary
from .sparql import graph_stats, load_graph, run_query, validate_query


def _add_sparql(subparsers: argparse._SubParsersAction) -> None:
    p = subparsers.add_parser("sparql", help="run a SPARQL SELECT or CONSTRUCT query")
    p.add_argument("query", nargs="+", help="SPARQL query string")
    p.add_argument(
        "-f", "--format",
        choices=["table", "json", "csv", "tsv", "turtle", "nt"],
        default="table",
    )
    p.add_argument("-o", "--output", help="write output to file")
    p.add_argument("--construct", action="store_true", help="shorthand for -f turtle")
    p.add_argument(
        "--dry-run", action="store_true",
        help="load graph and print stats, skip query",
    )
    p.add_argument(
        "-v", "--verbose",
        action="store_true", help="print graph stats before results",
    )
    p.add_argument(
        "--no-inference", action="store_true",
        help="skip OWL-RL inference (faster, raw data only)",
    )


def _add_shacl(subparsers: argparse._SubParsersAction) -> None:
    p = subparsers.add_parser("shacl", help="validate frontmatter against SHACL shapes")
    sub = p.add_subparsers(dest="subcmd", required=True)
    validate = sub.add_parser("validate", help="validate wiki pages against SHACL shapes")
    validate.add_argument(
        "--summary", action="store_true",
        help="print per-file conformance summary",
    )
    validate.add_argument(
        "-v", "--verbose",
        action="store_true", help="print full validation report",
    )
    validate.add_argument(
        "file", nargs="?",
        help="validate a single file (by name or path)",
    )


def _add_frontmatter(subparsers: argparse._SubParsersAction) -> None:
    p = subparsers.add_parser("frontmatter", help="frontmatter conversion and normalization")
    sub = p.add_subparsers(dest="subcmd", required=True)
    norm = sub.add_parser("normalize", help="normalize frontmatter property names")
    norm.add_argument(
        "--dry-run", action="store_true",
        help="print what would change without changing it",
    )
    sub.add_parser("convert", help="convert frontmatter to canonical JSON-LD")


def _add_init(subparsers: argparse._SubParsersAction) -> None:
    p = subparsers.add_parser("init", help="initialize a new wiki from a template")
    p.add_argument("-t", "--template", default="default", help="template to use (default: default)")
    p.add_argument("-d", "--dir", default=".", help="target directory (default: current directory)")
    p.add_argument(
        "--list-templates", action="store_true",
        help="list available templates",
    )


def _run_sparql(args: argparse.Namespace, book_root: Path) -> int:
    wiki_dir = book_root / "wiki"
    raw_dir = book_root / "raw"

    if args.dry_run:
        g = load_graph(
            wiki_dir=wiki_dir,
            raw_dir=raw_dir if raw_dir.exists() else None,
            infer=not args.no_inference,
        )
        stats = graph_stats(g)
        print(f"Graph stats: {stats['triples']} triples, {stats['subjects']} subjects")
        return 0

    query = " ".join(args.query)
    if not validate_query(query):
        print(f"Error: '{query}' does not look like a valid SPARQL query", file=sys.stderr)
        return 1

    g = load_graph(
        wiki_dir=wiki_dir,
        raw_dir=raw_dir if raw_dir.exists() else None,
        infer=not args.no_inference,
    )

    if args.verbose:
        stats = graph_stats(g)
        msg = f"Graph: {stats['subjects']} subjects, "
        msg += f"{stats['predicates']} predicates, "
        msg += f"{stats['triples']} triples\n"
        print(msg)

    output_format = "turtle" if args.construct else (args.format or "table")
    result = run_query(g, query, format=output_format)

    if args.output:
        Path(args.output).write_text(result, encoding="utf-8")
        print(f"Written to {args.output}")
    else:
        print(result)

    return 0


def _run_shacl(args: argparse.Namespace, book_root: Path) -> int:
    wiki_dir = book_root / "wiki"
    shapes_dir = book_root / "shapes"

    if args.file:
        path = Path(args.file)
        if not path.is_absolute():
            path = wiki_dir / path

        result = validate_file(path, shapes_dir=shapes_dir, verbose=args.verbose)
        if result is None:
            print("No frontmatter found in file")
            return 1
        print(f"[{'PASS' if result else 'FAIL'}] {path.name}")
        return 0 if result else 1

    if args.summary:
        summary = validate_summary(wiki_dir=wiki_dir, shapes_dir=shapes_dir)
        print(f"Conforms: {len(summary['conforms'])}")
        print(f"Fails:    {len(summary['fails'])}")
        print(f"Errors:   {len(summary['errors'])}")
        if summary["fails"]:
            print("\nFailing files:")
            for name in summary["fails"]:
                print(f"  - {name}")
        if summary["errors"]:
            print("\nError files:")
            for e in summary["errors"]:
                print(f"  - {e['file']}: {e['reason']}")
        return 0

    conforms = validate_all(wiki_dir=wiki_dir, shapes_dir=shapes_dir, verbose=args.verbose)
    print(f"\n[{'PASS' if conforms else 'FAIL'}] SHACL validation")
    return 0 if conforms else 1


def _run_frontmatter(args: argparse.Namespace, book_root: Path) -> int:
    wiki_dir = book_root / "wiki"

    if args.subcmd == "normalize":
        results = normalize_all(wiki_dir=wiki_dir, dry_run=args.dry_run)
        if args.dry_run:
            print(f"[DRY-RUN] Would fix {results['fixed']} files")
        else:
            print(f"Fixed {results['fixed']} files")
        return 0

    if args.subcmd == "convert":
        results = convert_all(wiki_dir=wiki_dir)
        print(f"Converted:     {len(results['converted'])}")
        print(f"No frontmatter: {len(results['no_frontmatter'])}")
        if results["errors"]:
            for e in results["errors"]:
                print(f"  Error: {e['file']}: {e['error']}")
        return 0

    return 0


def _run_init(args: argparse.Namespace) -> int:
    """Initialize a new wiki from a template."""
    # Handle --list-templates
    if args.list_templates:
        template_root = Path(__file__).resolve().parent / "templates"
        if not template_root.is_dir():
            print("No templates directory found.", file=sys.stderr)
            return 1
        
        templates = [d.name for d in template_root.iterdir() if d.is_dir()]
        if not templates:
            print("No templates available.", file=sys.stderr)
            return 1
        
        print("Available templates:")
        for t in sorted(templates):
            print(f"  - {t}")
        return 0
    
    target_dir = Path(args.dir).resolve()
    
    # Check if target directory is not empty
    if target_dir.exists() and any(target_dir.iterdir()):
        print(f"Error: Target directory '{target_dir}' is not empty", file=sys.stderr)
        return 1
    
    template_id = args.template
    template_path = Path(__file__).resolve().parent / "templates" / template_id
    
    if not template_path.is_dir():
        print(f"Error: Template '{template_id}' not found in {Path(__file__).resolve().parent / 'templates'}", file=sys.stderr)
        return 1
    
    # Copy template to target directory
    target_dir.mkdir(parents=True, exist_ok=True)
    
    for item in template_path.iterdir():
        dest = target_dir / item.name
        if item.is_dir():
            shutil.copytree(item, dest)
        else:
            shutil.copy2(item, dest)
    
    print(f"Initialized wiki in {target_dir} using '{template_id}' template")
    
    # Initialize git repository
    try:
        subprocess.run(["git", "init"], cwd=target_dir, check=True, capture_output=True)
        subprocess.run(["git", "add", "."], cwd=target_dir, check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit from wiki-framework template"],
            cwd=target_dir, check=True, capture_output=True
        )
        print(f"Initialized git repository with initial commit")
    except subprocess.CalledProcessError as e:
        print(f"Warning: Failed to initialize git repo: {e}", file=sys.stderr)
        return 0  # Not a fatal error
    
    return 0


def _find_wiki_root() -> Path:
    """Walk up from __file__ until we find a directory containing pyproject.toml."""
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / "pyproject.toml").exists() or (current / "wiki").exists():
            return current
        current = current.parent
    raise RuntimeError(f"Could not locate wiki root from {__file__}")


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="wiki-tool",
        description="Query and validate the wiki with SPARQL and SHACL",
    )
    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    _add_sparql(subparsers)
    _add_shacl(subparsers)
    _add_frontmatter(subparsers)
    _add_init(subparsers)

    args = parser.parse_args()

    if args.subcommand == "init":
        return _run_init(args)

    book_root = _find_wiki_root()

    if args.subcommand == "sparql":
        return _run_sparql(args, book_root)
    if args.subcommand == "shacl":
        return _run_shacl(args, book_root)
    if args.subcommand == "frontmatter":
        return _run_frontmatter(args, book_root)

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())

