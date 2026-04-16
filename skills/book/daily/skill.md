# Daily Review Skill (daily)

The **Daily Heartbeat** ensures the vault remains an authoritative active-todo
surface. It runs at midnight PST.

## Workflow

1. **Read** yesterday's daily review (`wiki/daily-YYYY-MM-DD.md`).
2. **Scan** `raw/` for recent activity logs and zettelkasten captures.
3. **Generate** today's review using the `template.md`.
4. **Update** `wiki/index.md` and `wiki/reminders.md`.
5. **Commit** with `process(daily): update heartbeat for YYYY-MM-DD`.

## Execution

Use the `skills/book/heartbeat.ts` Deno script.
