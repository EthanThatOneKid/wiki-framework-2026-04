"""Tests for init command."""

from pathlib import Path
import argparse
from wiki.__main__ import _run_init


def test_init_default_template(tmp_path, capsys):
    """Test initializing a new wiki with default template."""
    target_dir = tmp_path / "my-wiki"
    
    args = argparse.Namespace(template="default", dir=str(target_dir), list_templates=False)
    result = _run_init(args)
    
    assert result ==0
    assert target_dir.exists()
    assert (target_dir / "wiki").exists()
    assert (target_dir / "shapes").exists()
    assert (target_dir / ".github" / "workflows" / "shacl-validation.yml").exists()
    assert (target_dir / "pyproject.toml").exists()


def test_init_git_initialized(tmp_path):
    """Test that init creates a git repository."""
    target_dir = tmp_path / "my-wiki"
    
    args = argparse.Namespace(template="default", dir=str(target_dir), list_templates=False)
    _run_init(args)
    
    assert (target_dir / ".git").exists()


def test_init_nonexistent_template(tmp_path, capsys):
    """Test init with non-existent template."""
    target_dir = tmp_path / "my-wiki"
    
    args = argparse.Namespace(template="nonexistent", dir=str(target_dir), list_templates=False)
    result = _run_init(args)
    
    assert result == 1
    captured = capsys.readouterr()
    assert "not found" in captured.err


def test_init_target_not_empty(tmp_path, capsys):
    """Test init when target directory is not empty."""
    target_dir = tmp_path / "my-wiki"
    target_dir.mkdir()
    (target_dir / "existing.txt").write_text("already exists")
    
    args = argparse.Namespace(template="default", dir=str(target_dir), list_templates=False)
    result = _run_init(args)
    
    assert result == 1
    captured = capsys.readouterr()
    assert "not empty" in captured.err


def test_init_list_templates(capsys):
    """Test list-templates flag."""
    args = argparse.Namespace(list_templates=True)
    result = _run_init(args)
    
    assert result == 0
    captured = capsys.readouterr()
    assert "Available templates:" in captured.out
