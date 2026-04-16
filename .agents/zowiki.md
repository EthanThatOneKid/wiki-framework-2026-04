# Zowiki Agent Context (.agents/zowiki.md)

This file provide the high-level operational context for any AI agent
interacting with the Zowiki repository.

## 🧱 Repository Architecture

- **`wiki/`**: The "Compiled Brain" (Evergreen knowledge, JSON-LD frontmatter).
- **`raw/`**: The "Immutable Ledger" (Append-only primary sources, transcripts,
  captures).
- **`skills/`**: The "Automation Layer" (Deno-based skills and workflows).
- **`SCHEMA.md`**: The "Operating System" Rules and Commit Protocols.

## 🤖 Interaction Model

Agents must treat **`SCHEMA.md`** as their primary directive.

### Core Behaviors:

1. **Semantic Integrity**: Use wikilinks and OFM for connectivity.
2. **Minimal Entropy**: Follow canonical patterns; refine during every visit.
3. **Audit Trail**: Adhere to the machine-readable commit protocol.
4. **Heartbeat**: Pulse nightly daily reviews and hourly synthesis.

## 🛠️ Essential Skills

- **`skills/lint.ts`**: Run `deno task lint` after any frontmatter changes.
- **`skills/book/heartbeat.ts`**: Run `deno task heartbeat` to generate daily
  review.

---

_For operational details, read SCHEMA.md._
