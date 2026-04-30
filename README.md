# wiki

An opinionated, engine-agnostic, and agent-friendly wiki framework.

## Overview

This repository provides the core architecture, rules, and skills for maintaining a structured knowledge base (Second Brain). It is designed to be used as a template or a shared core for personal wiki instances like `book`.

## Architecture

The framework follows a three-layer stack:
1. **`raw/`**: Immutable primary sources and atomic captures.
2. **`wiki/`**: Curated, evergreen knowledge records.
3. **`RULES.md`**: The "Operating System" — guidelines for human and AI collaboration.

## Core Features

- **Semantic Integrity**: Standardized JSON-LD frontmatter rooted in Schema.org.
- **Agent-Ready**: Explicit guidelines and workflows for AI coding assistants.
- **Portable Skills**: Automations for dailies, ingestion, and link auditing.
- **Validation**: Built-in SHACL and SPARQL tools for data hardening.

## Getting Started

1. Create a new repository using this one as a template.
2. Set up your personal instance (e.g., `my-wiki`).
3. Use the `sync` mechanism to stay updated with framework improvements.

## Rules

See [RULES.md](RULES.md) for detailed guidelines on how to interact with the vault.

---
Managed by **EthanThatOneKid**
