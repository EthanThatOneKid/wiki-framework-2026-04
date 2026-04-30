# Hourly heartbeat config

## Agent identity

- **Agent ID**: hourly-synthesis
- **Type**: Synthesis and triage agent (Hourly)
- **Schedule**: Top of every hour (`0 * * * *`)

## Vault path

`/home/workspace/book/`

## Triage parameters

- **Lookback**: 1 hour (`git log --since="1 hour ago"`)
- **Action items**: Parse `[ ]` from new content
- **Loose ends**: Monitor mentions of People, Projects, Concepts

## Hourly template

Use `skills/hourly/template.md` for the triage section structure.

## Output

- **Modifies**: `wiki/daily-YYYY-MM-DD.md` (updates the `## Hourly triage`
  section)
- **Commit type**: `process`
- **Commit scope**: `daily`

