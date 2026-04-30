"""SPARQL utilities for the book graph."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Optional

import yaml
from rdflib import Graph, Literal, Namespace, RDF, RDFS, URIRef, OWL
from rdflib.namespace import XSD

# Namespaces
SCHEMA = Namespace("https://schema.org/")
WIKI = Namespace("https://{{owner}}.github.io/{{repo}}/wiki/")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")
DC = Namespace("http://purl.org/dc/elements/1.1/")
DCTERMS = Namespace("http://purl.org/dc/terms/")

NAMESPACES = {
    "schema": SCHEMA,
    "wiki": WIKI,
    "foaf": FOAF,
    "rdf": RDF,
    "rdfs": RDFS,
    "xsd": XSD,
    "dc": DC,
    "dcterms": DCTERMS,
}

WIKI_DIR = Path("wiki")
RAW_DIR = Path("raw")
WIKI_BASE = "https://{{owner}}.github.io/{{repo}}/wiki/"



# --- Utility Functions ---


def _kebab(s: str) -> str:
    """Convert string to kebab-case for URI segments."""
    s = str(s).lower().strip()
    s = re.sub(r"[\s\-]+", "-", s)
    s = re.sub(r"[^a-z0-9\-]", "", s)
    return s


# --- Frontmatter Logic ---


def parse_frontmatter(content: str) -> Optional[dict]:
    """Parse YAML or JSON frontmatter from markdown content."""
    if not content.startswith("---"):
        return None

    parts = content.split("---", 2)
    if len(parts) < 2:
        return None

    frontmatter_text = parts[1].strip()

    if frontmatter_text.startswith("{"):
        try:
            return json.loads(frontmatter_text)
        except json.JSONDecodeError:
            return None

    try:
        return yaml.safe_load(frontmatter_text)
    except yaml.YAMLError:
        return None





def ensure_context(data: dict) -> dict:
    """Ensure @context is present with required namespaces."""
    if "@context" not in data:
        data["@context"] = {
            "@vocab": "https://schema.org/",
            "wiki": "https://{{owner}}.github.io/{{repo}}/wiki/",
            "foaf": "http://xmlns.com/foaf/0.1/",
        }
    return data


def frontmatter_to_dict(content: str) -> Optional[dict]:
    """Parse and add context to frontmatter in one call."""
    data = parse_frontmatter(content)
    if not data:
        return None
    data = ensure_context(data)
    return data


def frontmatter_from_path(path: Path) -> Optional[dict]:
    """Read a .md file and return its parsed, normalized frontmatter."""
    try:
        content = path.read_text(encoding="utf-8")
        return frontmatter_to_dict(content)
    except Exception:
        return None


# --- RDF Conversion ---


def _resolve_predicate(key: str) -> URIRef:
    """Map a frontmatter key to an RDF predicate URI."""
    if ":" in key:
        prefix, name = key.split(":", 1)
        if prefix in NAMESPACES:
            return NAMESPACES[prefix][name]
    if key.startswith("wiki."):
        return WIKI[key[5:]]
    return SCHEMA[key]


def _resolve_object(key: str, value: Any, graph: Graph, subject: URIRef) -> None:
    """Add a predicate-object pair to the graph, handling nested structures."""
    pred = _resolve_predicate(key)

    if isinstance(value, dict):
        if "@id" in value:
            uri = value["@id"]
            if ":" in uri:
                prefix, name = uri.split(":", 1)
                if prefix in NAMESPACES:
                    uri = str(NAMESPACES[prefix][name])
            graph.add((subject, pred, URIRef(uri)))
        elif "@type" in value:
            blank = URIRef(f"_:blank-{_kebab(key)}-{id(value)}")
            graph.add((subject, pred, blank))
            graph.add((blank, RDF.type, URIRef(f"{SCHEMA}{value['@type']}")))
            for k, v in value.items():
                if not k.startswith("@"):
                    _resolve_object(k, v, graph, blank)
        else:
            graph.add((subject, pred, Literal(str(value))))
    elif isinstance(value, str) and value.startswith("http"):
        graph.add((subject, pred, URIRef(value)))
    elif isinstance(value, bool):
        graph.add((subject, pred, Literal(value, datatype=XSD.boolean)))
    elif isinstance(value, (int, float)):
        graph.add((subject, pred, Literal(value)))
    elif value is not None:
        graph.add((subject, pred, Literal(str(value))))


def frontmatter_to_graph(
    data: dict, base_uri: str = WIKI_BASE, file_id: Optional[str] = None
) -> Graph:
    """Convert frontmatter dictionary to an RDF graph."""
    g = Graph()
    for prefix, ns in NAMESPACES.items():
        g.bind(prefix, ns)
 
    if not data or "@type" not in data:
        return g
 
    doc_id = data.get("@id")
    if not doc_id:
        if file_id:
            doc_id = f"{base_uri}{file_id}.md"
        else:
            name = data.get("name", data.get("givenName", ""))
            if data.get("@type") == "Person":
                given = data.get("givenName", "")
                family = data.get("familyName", "")
                if given and family:
                    doc_id = f"{base_uri}{_kebab(given)}-{_kebab(family)}.md"
                else:
                    doc_id = f"{base_uri}{_kebab(name)}.md"
            else:
                doc_id = f"{base_uri}{_kebab(name)}.md"

    subject = URIRef(doc_id)

    rdf_type = data.get("@type")
    if isinstance(rdf_type, list):
        for t in rdf_type:
            g.add((subject, RDF.type, URIRef(f"{SCHEMA}{t}")))
    elif rdf_type:
        g.add((subject, RDF.type, URIRef(f"{SCHEMA}{rdf_type}")))

    for key, value in data.items():
        if key.startswith("@"):
            continue
        if isinstance(value, list):
            for item in value:
                _resolve_object(key, item, g, subject)
        elif value:
            _resolve_object(key, value, g, subject)

    return g





# --- Resolution Logic ---


def _build_name_to_id_map(wiki_dir: Path = WIKI_DIR) -> dict[str, str]:
    """Build a map from person names to their wiki @id URIs."""
    name_map: dict[str, str] = {}

    for md_file in wiki_dir.glob("*.md"):
        try:
            data = frontmatter_from_path(md_file)
            if not data or data.get("@type") != "Person":
                continue

            doc_id = data.get("@id", "")
            if not doc_id:
                name = data.get("name", data.get("givenName", ""))
                if data.get("givenName") and data.get("familyName"):
                    doc_id = f"{WIKI_BASE}{_kebab(data['givenName'])}-{_kebab(data['familyName'])}.md"
                else:
                    doc_id = f"{WIKI_BASE}{_kebab(name)}.md"

            name = data.get("name", "")
            if name:
                name_map[name.lower()] = doc_id

            given = data.get("givenName", "")
            family = data.get("familyName", "")
            if given and family:
                full_name = f"{given} {family}"
                name_map[full_name.lower()] = doc_id
                name_map[given.lower()] = doc_id
        except Exception:
            continue

    return name_map


def resolve_blank_nodes(g: Graph, wiki_dir: Path = WIKI_DIR) -> Graph:
    """Resolve blank nodes to @id references where possible."""
    name_map = _build_name_to_id_map(wiki_dir)

    blank_nodes = list(g.subjects())
    blank_nodes = [s for s in blank_nodes if str(s).startswith("_:")]

    for blank in blank_nodes:
        name = g.value(blank, SCHEMA.name)
        if not name or str(name).lower() not in name_map:
            continue

        target_id = name_map[str(name).lower()]

        for pred, obj in list(g.predicate_objects(blank)):
            g.remove((blank, pred, obj))
            g.add((URIRef(target_id), pred, obj))

        for subj, pred in list(g.subject_predicates(blank)):
            g.remove((subj, pred, blank))
            g.add((subj, pred, URIRef(target_id)))

    return g


# --- Inference Logic ---


def add_inference_axioms(g: Graph) -> None:
    """Load OWL/RDFS inference axioms from reasoning/*.ttl."""
    reasoning_dir = Path("reasoning")
    if reasoning_dir.exists():
        for ttl_file in reasoning_dir.glob("*.ttl"):
            g.parse(ttl_file, format="turtle")


def expand_with_owlrl(g: Graph) -> Graph:
    """Apply OWL-RL deductive closure to the graph."""
    import owlrl
    owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(g)
    return g


# --- Graph Loading ---


def load_graph(
    wiki_dir: Path = WIKI_DIR,
    raw_dir: Optional[Path] = RAW_DIR,
    infer: bool = True,
) -> Graph:
    """Load all wiki (and optionally raw) markdown files into a single Graph."""
    g = Graph()
    for prefix, ns in NAMESPACES.items():
        g.bind(prefix, ns)

    for md_file in wiki_dir.glob("*.md"):
        data = frontmatter_from_path(md_file)
        if data:
            g += frontmatter_to_graph(data, file_id=md_file.stem)

    if raw_dir and raw_dir.exists():
        for md_file in raw_dir.glob("*.md"):
            data = frontmatter_from_path(md_file)
            if data:
                g += frontmatter_to_graph(data, file_id=md_file.stem)

    resolve_blank_nodes(g, wiki_dir)

    if infer:
        add_inference_axioms(g)
        expand_with_owlrl(g)

    return g


def graph_stats(g: Graph) -> dict:
    """Return basic stats about a graph."""
    return {
        "triples": len(g),
        "subjects": len(set(g.subjects())),
        "predicates": len(set(g.predicates())),
        "objects": len(set(g.objects())),
    }


# --- Query Logic ---


def run_query(
    graph: Graph,
    query: str,
    format: str = "table",
) -> str:
    """Run a SPARQL SELECT or CONSTRUCT query against the graph."""
    q = query.strip().upper()
    is_construct = q.startswith("CONSTRUCT")

    if is_construct:
        result = graph.query(query)
        if format in ("turtle", "nt"):
            return result.serialize(format=format)
        return result.serialize(format="turtle")

    result = graph.query(query)

    if format == "json":
        return result.serialize(format="json")
    elif format == "csv":
        return result.serialize(format="csv")
    elif format == "tsv":
        return result.serialize(format="tsv")
    else:
        return _table_format(result)


def _table_format(result) -> str:
    """Format SELECT results as a simple ASCII table."""
    rows = list(result)
    if not rows:
        return "(no results)"

    try:
        keys = [str(v) for v in result.vars]
    except Exception:
        keys = []

    if not keys and rows:
        first = rows[0]
        if isinstance(first, tuple):
            keys = [f"?v{i}" for i in range(len(first))]
        elif hasattr(first, "keys"):
            keys = list(first.keys())
        else:
            return str(rows)

    if not keys:
        return "(empty query)"

    col_widths = [len(str(k)) for k in keys]
    for row in rows:
        if isinstance(row, tuple):
            vals = [str(v) for v in row]
        else:
            vals = [str(row.get(k, "")) for k in keys]
        for i, val in enumerate(vals):
            if i < len(col_widths):
                col_widths[i] = max(col_widths[i], len(val))

    header = " | ".join(str(k).ljust(col_widths[i]) for i, k in enumerate(keys))
    sep = "-+-".join("-" * w for w in col_widths)
    lines = [header, sep]
    for row in rows:
        if isinstance(row, tuple):
            vals = [str(v) for v in row]
        else:
            vals = [str(row.get(k, "")) for k in keys]
        line = " | ".join(
            vals[i].ljust(col_widths[i]) if i < len(vals) else "" for i in range(len(keys))
        )
        lines.append(line)

    return "\n".join(lines)


def validate_query(query: str) -> bool:
    """Check if a query string looks like valid SPARQL."""
    text = query.strip()
    valid_keywords = ("SELECT", "CONSTRUCT", "DESCRIBE", "ASK")
    cleaned = ""
    for line in text.split("\n"):
        ul = line.strip().upper()
        if ul.startswith("PREFIX"):
            rest = line.strip()[len("PREFIX"):].strip()
            if rest.startswith("schema:"):
                after_prefix = rest.split(">", 1)
                if len(after_prefix) > 1:
                    rest = after_prefix[1].strip()
            cleaned += " " + rest
        else:
            cleaned += " " + line
    q = cleaned.strip().upper()
    return any(q.startswith(k) for k in valid_keywords)

