---
name: wiki-project
description: Scaffolds a new project record in the wiki. Use when adding a tracked project, repo, or initiative with status and roadmap.
---

# New project (wiki)

## Output

- **Path:** `wiki/<kebab-case-title>.md`
- **Source scaffold:** [template.md](template.md)

## Steps

1. Search `wiki/` and hubs (`projects.md`, `index.md`) for an existing project.
2. Copy [template.md](template.md). Set `created`, tags, and H1 from the project
   name.
3. Fill Summary, Status, Priority, Details (type, repo, stack), Roadmap,
   Dependencies.
4. Update project hubs if applicable.

## Placeholders

| Placeholder | Replace with |
| ----------- | ------------ |
| `{{date}}`  | `YYYY-MM-DD` |
| `{{title}}` | Project name |

