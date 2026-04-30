# New zet (atomic note)

Scaffolds a zettelkasten-style note in the wiki. Use for atomic notes,
one-idea captures, and short linked thoughts.

## Output

- **Path:** `wiki/zet-YYYYMMDDHHMM-[slug].md` (timestamp prefix keeps entries
  sortable and unique; slug is lowercase kebab-case)
- **Source scaffold:** [template.md](template.md)

## Steps

1. Prefer linking to existing `wiki/` records or other `wiki/zet-*.md` atoms
   before creating a new one.
2. Copy [template.md](template.md). Set `dateCreated` to `YYYY-MM-DD`, add
   topical keywords.
3. Keep one main idea per file; link out with WikiLinks under Related.
4. Optional: add `aliases:` in frontmatter if the title is long.

## Placeholders

| Placeholder | Replace with                 |
| ----------- | ---------------------------- |
| `{{date}}`  | `YYYY-MM-DD`                 |
| `{{title}}` | Short atomic title (heading) |

## Note on convergence

Zets now live in `wiki/` alongside all other records instead of `raw/`. They
are distinguished by the `zet-` prefix and `@type: [CreativeWork, Zet]`
frontmatter for semantic querying.

The `raw/` directory remains append-only for non-atomic artifacts (transcripts,
downloaded files, etc.) that are not canonical wiki records.

