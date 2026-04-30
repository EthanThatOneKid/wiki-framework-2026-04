# Hourly heartbeat

The vault's proactive intelligence layer. The hourly heartbeat ensures that new
information is instantly contextualized and no loose ends are left dangling.

## Core behavior

1. **Delta analysis**: Diffs the repository since the last hourly push
   (`git log --since="1 hour ago"`) to identify newly created Zet notes, updated
   Wiki items, or new Raw artifacts.
2. **Automatic triage**:
   - Scans new Zet notes and Raw logs for `[ ]` action items.
   - Automatically promotes these items to the `## Hourly triage` section of
     `wiki/daily-YYYY-MM-DD.md`.
3. **Connection engine (connecting loose ends)**:
   - Identifies mentions of People, Projects, or Concepts in new content.
   - Proactively verifies if these entities exist in the Wiki.
   - If missing, creates a stub record.
   - If existing, ensures the parent hub (e.g., `network.md`, `projects.md`) is
     updated to reflect recent activity.
4. **Nudge & Accountability (Proactive Bumping)**:
   - **Stalled task detection**: Identifies high-priority actions that haven't been touched in >4 hours.
   - **Contextual Bumping**: If the user is working on a specific project (detectable via Git diffs), surfaces related "someday/maybe" ideas or loose ends for that project.
   - **Interactive check-in**: Appends a specific question or "nudge" to the `## Hourly triage` section (e.g., "You've been deep in `worlds-api` for 2 hours; should we draft that documentation zet now?").
6. **EA Integration**:
   - Calls `ea:prepare-upcoming-meetings` to prep for events in the next hour.
   - Surfaces prep context in `## Hourly triage`.
7. **Distillation check**: Evaluates if multiple new Zet notes on a similar
   topic warrant a "Hub update" or a distilled "Wiki card" promotion.

## Output

- **Modifies**: `wiki/daily-YYYY-MM-DD.md` (updates the `## Hourly triage`
  section).
- **Proactive Notification**: If a critical blocker or high-priority stalled task
  is identified, the agent may initiate a brief "nudge" turn to ask the user
  for status.
- **Commit**: `process(daily): hourly synthesis and triage [HH:00]`
- **Push**: Immediately to main.

## Principles

- **Synthesis**: Don't just list changes; explain the connectivity and impact.
- **Triage**: Automatically move tasks into the daily buffer for human review.
- **Loose ends**: Never allow a new entity to remain unlinked or un-hubbed for
  more than an hour.
- **Silent by Default**: If no activity, connection, or prep-flow triggers are
  detected, skip the triage update and notification entirely.
- **Accuracy**: Reflect current Git/Vault state precisely.

