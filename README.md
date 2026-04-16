# 🧠 Zowiki

**An idiomatic, engine-agnostic second brain template.**

Inspired by
[Andrej Karpathy's LLM-Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

## 🏗️ Architecture

Zowiki provides a robust structure for a machine-readable knowledge base:

1. **`raw/`**: Immutable storage for your source materials.
2. **`wiki/`**: Your compiled, interlinked knowledge base ("The Vault").
3. **`SCHEMA.md`**: The protocols and rules for your AI maintainer.

## ✨ Features

- **Obsidian-flavored Markdown (OFM)**: Standardized on wikilinks (`[[link]]`)
  and callouts for maximum connectivity.
- **Semantic Web Integrity**: Standardized JSON-LD in YAML frontmatter.
- **Agent-Ready**: Explicit protocols for AI-driven ingestion and maintenance.
- **Forkable & Syncable**: Built-in GitHub Action to stay up-to-date with
  template improvements.

## 🛠️ Adding an Engine (Optional)

Zowiki is engine-agnostic by design. You can layer your favorite publishing or
visualization tool on top:

- **Quartz 4**:
  1. `npx quartz create` in this directory.
  2. Set `content` to `wiki/` (e.g., via symlink or config).
- **Obsidian**:
  1. Open the `wiki/` folder as a new vault.
- **Logseq**:
  1. Import the `wiki/` directory.

## 🚀 Getting Started

1. **Use this Template**: Create a new repository from this one.
2. **Start Your Log**: Open `wiki/log.md` and document your first realization.
3. **Invite an Agent**: Point your AI assistant to `SCHEMA.md` to begin
   automated ingestion.

---

Built with ❤️ by [EthanThatOneKid](https://github.com/EthanThatOneKid) and his
AI coding assistant.
