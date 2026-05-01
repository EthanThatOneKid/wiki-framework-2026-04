"""Tests for SPARQL module."""

from pathlib import Path
from wiki.sparql import load_graph, graph_stats, validate_query


def test_validate_query_valid():
    """Test validating a valid SPARQL query."""
    query = "SELECT ?s WHERE { ?s a ?type }"
    assert validate_query(query) is True


def test_validate_query_invalid():
    """Test validating an invalid SPARQL query."""
    query = "NOT A REAL QUERY"
    assert validate_query(query) is False


def test_load_graph(tmp_path):
    """Test loading graph from wiki directory."""
    wiki_dir = tmp_path / "wiki"
    wiki_dir.mkdir()
    
    md_file = wiki_dir / "test.md"
    md_content = """---
{"@type": "Thing", "name": "Test"}
---

# Test
"""
    md_file.write_text(md_content)
    
    graph = load_graph(wiki_dir=wiki_dir)
    stats = graph_stats(graph)
    assert "triples" in stats
    assert stats["triples"] >= 0


def test_load_graph_with_raw(tmp_path):
    """Test loading graph with raw directory."""
    wiki_dir = tmp_path / "wiki"
    wiki_dir.mkdir()
    raw_dir = tmp_path / "raw"
    raw_dir.mkdir()
    
    graph = load_graph(wiki_dir=wiki_dir, raw_dir=raw_dir)
    assert graph is not None


def test_graph_stats_empty():
    """Test graph stats for empty graph."""
    from rdflib import Graph
    g = Graph()
    stats = graph_stats(g)
    assert stats["triples"] == 0
    assert stats["subjects"] == 0
    assert stats["predicates"] == 0
