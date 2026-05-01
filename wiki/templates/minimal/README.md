# My Wiki

A minimal wiki instance started with `python -m wiki init -t minimal`.

## Structure

- `wiki/` — Your knowledge base (add `.md` files here)
- `shapes/` — SHACL shapes for validation (optional)
- `.github/workflows/shacl-validation.yml` — CI pipeline

## Getting Started

1. Add markdown files to `wiki/` with JSON-LD frontmatter
2. Run `python -m wiki shacl validate` to validate
3. Run `python -m wiki sparql "SELECT ..."` to query
