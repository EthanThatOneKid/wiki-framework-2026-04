# Action creation skill

Creates a new action file in `wiki/`.

## When to use

Use this skill whenever:
- The user mentions a new task, todo, or action item.
- An ingested note contains an actionable item.
- A meeting transcript yields a follow-up.

## Workflow

1. **Check for duplicates** — Search `wiki/` for an existing action (`@type: Action`)
   with a similar name before creating a new one.
2. **Choose a slug** — Use semantic kebab-case like Wikipedia article titles.
   Add discriminating details as needed (e.g., `apply-govini-2026.md` not just
   `apply.md`). Prefix action slugs with `action-` for discoverability.
3. **Set priority** — Infer from context:
   - `high` — Has a deadline within 7 days, is blocking other work, or the user
     said "urgent" / "ASAP".
   - `medium` — Active project work, networking follow-ups, applications.
   - `low` — Someday/maybe items, learning goals, entertainment.
4. **Link context** — Use `about` to link the action to its parent project,
   person, or concept wiki page.
5. **Fill the template** — Use `skills/action/template.md`.

## Backoff surfacing properties

The daily heartbeat uses these fields to decide when to surface an action:

- `lastSurfaced` — Updated by the daily skill each time it includes the action.
- `surfaceCount` — Incremented each time the action is surfaced.
- `priority` — Determines the backoff schedule.

Do NOT set `lastSurfaced` or `surfaceCount` when creating a new action. The daily
skill initializes them on first surfacing.

## Completing an action

When an action is done:
1. Set `actionStatus` to `CompletedActionStatus`.
2. Set `dateCompleted` to the completion date (YYYY-MM-DD).
3. Add a brief note in the body documenting the outcome or any milestones.
4. The action stays in `wiki/` for historical record.

