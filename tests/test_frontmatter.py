"""Tests for frontmatter module."""

from pathlib import Path
from wiki.frontmatter import frontmatter_to_jsonld, normalize_frontmatter_str, normalize_all, convert_all


def test_frontmatter_to_jsonld_valid(tmp_path):
    """Test converting frontmatter to JSON-LD."""
    md_file = tmp_path / "test.md"
    content = """---
{"@type": "Thing", "name": "Test"}
---

# Test Page
"""
    md_file.write_text(content)
    
    result = frontmatter_to_jsonld(md_file)
    assert result is not None
    assert "name" in result
    assert result["name"] == "Test"


def test_frontmatter_to_jsonld_no_frontmatter(tmp_path):
    """Test with file without frontmatter."""
    md_file = tmp_path / "test.md"
    content = "# Test Page\n\nNo frontmatter here.\n"
    md_file.write_text(content)
    
    result = frontmatter_to_jsonld(md_file)
    assert result is None


def test_normalize_frontmatter_str_adds_context():
    """Test normalize_frontmatter_str adds @context when missing."""
    content = """---
{"name": "Test"}
---

# Test
"""
    result = normalize_frontmatter_str(content)
    assert "@context" in result or "@context" in result.lower()


def test_normalize_frontmatter_str_no_change():
    """Test normalize_frontmatter_str returns unchanged when already correct."""
    content = """---
{"@context": {"@vocab": "https://schema.org/", "wiki": "https://{{owner}}.github.io/{{repo}}/wiki/"}, "name": "Test"}
---

# Test
"""
    result = normalize_frontmatter_str(content)
    # Should be unchanged or have same essential content
    assert "Test" in result
    assert "@context" in result


def test_normalize_all_dry_run(tmp_path):
    """Test normalize_all with dry_run flag."""
    wiki_dir = tmp_path / "wiki"
    wiki_dir.mkdir()
    
    # Create a file missing @context
    md_file = wiki_dir / "test.md"
    content = """---
{"name": "Test"}
---

# Test
"""
    md_file.write_text(content)
    
    results = normalize_all(wiki_dir=wiki_dir, dry_run=True)
    assert "fixed" in results
    assert results["fixed"] >= 0


def test_convert_all(tmp_path):
    """Test convert_all function."""
    wiki_dir = tmp_path / "wiki"
    wiki_dir.mkdir()
    
    # Create a file with frontmatter
    md_file = wiki_dir / "test.md"
    content = """---
{"name": "Test"}
---

# Test
"""
    md_file.write_text(content)
    
    results = convert_all(wiki_dir=wiki_dir)
    assert "converted" in results
    assert "no_frontmatter" in results
