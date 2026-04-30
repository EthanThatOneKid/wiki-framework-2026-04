---
name: wiki-person
description: Scaffolds a new person record in the wiki. Use when creating a contact, profile, or people entry in wiki/, or when the user adds someone to the network.
---

# New person (wiki)

## Output

- **Path:** `wiki/<kebab-case-name>.md` (lowercase, hyphens; see AGENTS.md)
- **Source scaffold:** [template.md](template.md)

## Steps

1. Search `wiki/` for an existing note for this person; extend it instead of
   duplicating.
2. Choose filename from display name (e.g. `Jordan Oram` → `jordan-oram.md`).
3. Copy [template.md](template.md). Set `created` to ISO date (`YYYY-MM-DD`).
   Set the H1 `# {{name}}` to the person’s name.
4. Fill Role, Relationship, Context, Contact, Notes; add wikilinks under
   Related.
5. Update hubs (`network.md`, `index.md`, etc.) per AGENTS.md hub cascade.

## Placeholders

| Placeholder | Replace with                              |
| ----------- | ----------------------------------------- |
| `{{date}}`  | `YYYY-MM-DD`                              |
| `{{name}}`  | Person’s name (title case in the heading) |

