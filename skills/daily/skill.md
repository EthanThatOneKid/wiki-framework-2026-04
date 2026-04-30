# Daily heartbeat (midnight)

Generates a daily review note in the book vault at midnight PST, then commits
and pushes.

## Vault structure

```
/home/workspace/book/
├── wiki/            # Daily reviews, action files, and living notes
├── raw/             # Append-only artifacts
└── skills/daily/    # This agent (config.md, skill.md, template.md)
```

## Core behavior

1. **Read yesterday's daily review** from `wiki/` to understand prior state.
2. **Check recent GitHub activity** across tracked repos.
3. **Surface actions using backoff algorithm:**
   - Query all `wiki/action-*.md` files with `actionStatus: PotentialActionStatus`.
   - For each action, compute whether it should surface today based on the
     backoff schedule (see below).
   - Group surfaced actions by priority (high, medium, low).
4. **Generate today's daily review** using `skills/daily/template.md`, filling in:
   - Yesterday's actual progress (from prior daily + git log).
   - Today's surfaced actions (from backoff algorithm).
   - Project status table.
5. **Update surfaced actions** — For each action that was surfaced today:
   - Increment `surfaceCount` by 1.
   - Set `lastSurfaced` to today's date.
6. **Write the file** to `wiki/daily-YYYY-MM-DD.md`.
7. **Hub cascade**: Update `wiki/index.md` to link the new daily log.
8. **EA Integration**: Calls `ea:briefing` to generate the morning strategy.
9. **Commit** with message: `process(daily): add review for YYYY-MM-DD`
10. **Push** to origin main.

## Backoff surfacing algorithm

The algorithm uses priority-weighted exponential backoff to prevent task fatigue.

### Schedule

| Priority | Base interval | Backoff multiplier | Max interval |
|----------|--------------|-------------------|-------------|
| `high`   | 1 day        | 1.5x              | 3 days      |
| `medium` | 2 days       | 2x                | 7 days      |
| `low`    | 3 days       | 2x                | 14 days     |

### Decision function

```
interval = base_interval * (backoff_multiplier ^ surfaceCount)
interval = min(interval, max_interval)

shouldSurface =
  (today - lastSurfaced) >= interval
  OR deadline is within 2 days
  OR (priority == "high" AND surfaceCount < 3)
  OR lastSurfaced is empty (never surfaced before)
```

### Reset conditions

- If the user interacts with the action (mentions it, edits it, or references
  it in conversation), reset `surfaceCount` to 0 so it regains visibility.
- If `actionStatus` changes to `CompletedActionStatus`, stop surfacing entirely.

## Important constraints

- **Do NOT copy action data into the daily frontmatter.** The daily file contains
  no `potentialAction` array. Actions live in their own `wiki/action-*.md` files.
- **Do NOT carry forward tasks between dailies.** The backoff algorithm handles
  resurfacing automatically.
- **Daily files are narrative summaries**, not data stores. They reference actions
  via `[[action-slug]]` WikiLinks but do not duplicate action metadata.

