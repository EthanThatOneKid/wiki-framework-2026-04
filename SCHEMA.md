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

### 2. Semantic Metadata

All files in `wiki/` must follow **JSON-LD** principles in YAML frontmatter.

- `id`: Unique identifier (e.g., `wiki:person-name`).
- `type`: Schema.org type (e.g., `Person`, `Project`).
- `name`: Human-readable name.

### 3. Navigation

Maintain `wiki/index.md` as the primary entrance to the graph.

---

Inspired by Andrej Karpathy's `llm-wiki`.
