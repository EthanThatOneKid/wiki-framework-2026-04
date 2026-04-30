---
name: wiki-idea
description: Scaffolds a new idea note in the wiki. Use when capturing a blog concept, product idea, technical exploration, or tagged idea record.
---

# New idea (wiki)

## Output

- **Path:** `wiki/<kebab-case-title>.md`
- **Source scaffold:** [template.md](template.md)

## Steps

1. Check `wiki/` for an existing idea on the same topic.
2. Copy [template.md](template.md). Set `created`, frontmatter `tags`, and H1
   title from `{{title}}`.
3. Write a one-line Summary; pick Category and Status checkboxes.
4. Link related people, projects, or `type/slip` notes under Related.

## Placeholders

| Placeholder | Replace with                                |
| ----------- | ------------------------------------------- |
| `{{date}}`  | `YYYY-MM-DD`                                |
| `{{title}}` | Short idea name (heading and filename stem) |

