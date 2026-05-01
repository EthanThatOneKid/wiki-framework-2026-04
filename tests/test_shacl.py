"""Tests for SHACL validation module."""

from pathlib import Path
from wiki.shacl import load_shapes, validate_all, validate_file, validate_summary


def test_load_shapes(tmp_path):
    """Test loading SHACL shapes from directory."""
    shapes_dir = tmp_path / "shapes"
    shapes_dir.mkdir()
    
    shape_file = shapes_dir / "test.ttl"
    shape_content = """@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix schema: <https://schema.org/> .

schema:ThingShape a sh:NodeShape ;
    sh:targetClass schema:Thing ;
    sh:property [
        sh:path schema:name ;
        sh:minCount 1 ;
    ] .
"""
    shape_file.write_text(shape_content)
    
    shapes_graph = load_shapes(shapes_dir)
    triples = list(shapes_graph.triples((None, None, None)))
    assert len(triples) > 0


def test_load_shapes_empty_dir(tmp_path):
    """Test loading shapes from empty directory."""
    shapes_dir = tmp_path / "empty_shapes"
    shapes_dir.mkdir()
    
    shapes_graph = load_shapes(shapes_dir)
    triples = list(shapes_graph.triples((None, None, None)))
    assert len(triples) == 0


def test_load_shapes_missing_dir():
    """Test loading shapes from non-existent directory."""
    shapes_graph = load_shapes(Path("/non/existent/path"))
    triples = list(shapes_graph.triples((None, None, None)))
    assert len(triples) == 0


def test_validate_all_no_shapes(tmp_path, capsys):
    """Test validate_all returns True when no shapes exist."""
    wiki_dir = tmp_path / "wiki"
    wiki_dir.mkdir()
    
    md_file = wiki_dir / "test.md"
    md_content = """---
{"@type": "Thing", "name": "Test"}
---

# Test
"""
    md_file.write_text(md_content)
    
    shapes_dir = tmp_path / "shapes"
    shapes_dir.mkdir()
    
    result = validate_all(wiki_dir=wiki_dir, shapes_dir=shapes_dir)
    assert result is True
    
    captured = capsys.readouterr()
    assert "Warning: No shapes found" in captured.out


def test_validate_file_valid(tmp_path):
    """Test validating a file with valid frontmatter."""
    shapes_dir = tmp_path / "shapes"
    shapes_dir.mkdir()
    
    shape_file = shapes_dir / "thing.ttl"
    shape_content = """@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix schema: <https://schema.org/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

schema:ThingShape a sh:NodeShape ;
    sh:targetClass schema:Thing ;
    sh:property [
        sh:path schema:name ;
        sh:minCount 1 ;
        sh:maxCount 1 ;
        sh:datatype xsd:string ;
    ] .
"""
    shape_file.write_text(shape_content)
    
    wiki_dir = tmp_path / "wiki"
    wiki_dir.mkdir()
    md_file = wiki_dir / "test.md"
    md_content = """---
{"@type": "Thing", "name": "Test Page"}
---

# Test Page
"""
    md_file.write_text(md_content)
    
    result = validate_file(md_file, shapes_dir=shapes_dir)
    assert result is True


def test_validate_summary_no_shapes(tmp_path, capsys):
    """Test validate_summary handles missing shapes gracefully."""
    wiki_dir = tmp_path / "wiki"
    wiki_dir.mkdir()
    shapes_dir = tmp_path / "shapes"
    shapes_dir.mkdir()
    
    result = validate_summary(wiki_dir=wiki_dir, shapes_dir=shapes_dir)
    assert "skipped" in result
    assert result["skipped"] is True
    
    captured = capsys.readouterr()
    assert "Warning: No shapes found" in captured.out
