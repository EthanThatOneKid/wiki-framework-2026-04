# Daily heartbeat config

## Agent identity

- **Agent ID**: daily-heartbeat
- **Type**: Scheduled surfacing agent (Daily)
- **Schedule**: Daily at midnight PST (`0 0 * * *`)

## Vault path

`/home/workspace/book/`

## Tracked GitHub repos

Monitor recent commits across all EthanThatOneKid repos, especially:

- `EthanThatOneKid/book` — this vault
- `postcardhq/postcard` — Worlds platform
- `wazootech/worlds` — Worlds API
- `EthanThatOneKid/dvd-collection` — DVD collection site

## Daily template

Use `skills/daily/template.md` as the template structure.

## Backoff parameters

These parameters control the exponential backoff surfacing algorithm. The daily
skill reads these values when deciding which `action-*.md` files to surface.

| Priority | Base interval (days) | Backoff multiplier | Max interval (days) |
|----------|---------------------|--------------------|---------------------|
| `high`   | 1                   | 1.5                | 3                   |
| `medium` | 2                   | 2                  | 7                   |
| `low`    | 3                   | 2                  | 14                  |

Override rules:
- **Deadline proximity:** Any action with a `deadline` within 2 days always
  surfaces.
- **High priority grace:** `high` priority actions surface unconditionally for
  the first 3 surfacing cycles (before backoff kicks in).
- **Never surfaced:** Actions with no `lastSurfaced` date always surface.

## Output

- File: `wiki/daily-YYYY-MM-DD.md`
- Commit type: `process`
- Commit scope: `daily`

