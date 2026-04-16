# Zowiki System Prompt (SCHEMA.md)

This file defines the protocols and metadata standards for an AI agent
maintaining the second brain vault.

## Hubs

- **wiki/**: Evergreen knowledge and compiles notes.
- **raw/**: Immutable sources (PDFs, transcripts, clippings).
- **skills/**: Automated scripts and automation.

## Core Protocols

### 1. Ingest Protocol

- **Source**: `raw/`
- **Output**: Create or update relevant notes in `wiki/`.
- **Log**: Append entry to `wiki/log.md`.
- **Constraint**: Do not modify files in `raw/`.

### 2. Semantic Metadata & Formatting

All files in `wiki/` must follow **Obsidian-flavored Markdown (OFM)**:

- **Wikilinks**: Use `[[note]]` for all internal links.
- **Frontmatter**: Use JSON-LD-inspired YAML (e.g., `id`, `type`, `name`).

### 3. Navigation

Maintain `wiki/index.md` as the primary entrance to the graph.

---

Inspired by Andrej Karpathy's `llm-wiki`.
