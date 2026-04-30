# Agent guidelines

Follow these guidelines when working as an agent in this wiki.

## [[one-right-way]]

[[one-right-way]]: Prioritize canonical, predictable patterns over custom
solutions to reduce cognitive load.

## [[minimal-entropy]]

[[minimal-entropy]]: Eliminate accidental complexity to maintain high velocity
and low friction.

## [[ssot|Single Source of Truth (SSoT)]]

Single Source of Truth (SSoT): "A picture says 1000 words"; do not repeat
information. Find the most conducive spot (or create one) and link to it to form
the semantic connection using [[ssot]]. If a source is removed, its information
is gone or must be re-homed. Embodies the "DRY" (Don't Repeat Yourself)
principle.

## [[leave-it-better-than-you-found-it|Leave it better than you found it]]

[[leave-it-better-than-you-found-it|Leave it better than you found it]]: Treat
the vault as a living garden. Repair damage, refine existing notes, and
proactively update files to align with evolving standards whenever you visit
them.

## Conflict prevention

Before starting a task, check the status of the git repository to ensure it is
synchronized with the remote. If the repository is not synchronized, attempt to
synchronize it quietly (e.g., `git pull --rebase`). If synchronization status
cannot be confirmed or synchronization fails, include a warning in the response
advising caution before proceeding with edits. Otherwise, proceed quietly.

## Small commits

- One change per commit: Keep commits logical and focused.
- Commit early and often: Manage and revert small commits more easily.
- Meaningful messages: Explain what and why. Format: `type(scope): description`.
- Commit types: Use `feat` (new feature), `fix` (bug fix), `docs` (docs),
  `refactor` (code change), `process` (workflow), or `wip` (work in progress).

## When to commit

- Commit your changes after you complete a task.
- Commit your changes before you start a major refactor.
- At the end of each conversation turn (the period between user messages),
  commit once if any changes were made. If no changes were made, commit nothing.
- Push your changes immediately after every commit to ensure visibility.

## Autonomous commits

After completing an autonomous edit, commit with `ai(scope): description` so
changes are traceable and rollback-able. Reference
[Google's small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html)
for intent-based commits; keep scope narrow, explain the change clearly. Don't
commit mechanically per-file; commit per meaningful unit of work. This balances
automation (stuff just works) with the ability to inspect and revert if
something goes wrong. Always review automated changes against the style
guidelines in this file before committing.

## Vault rules

- Raw is append-only: Never edit files in `/raw/`. Add new artifacts only.
- Wiki is flattened: Place all living resources (people, projects,
  organizations, hubs, and daily reviews) in `wiki/`.
- Zet (zettelkasten): Captured ideas and atomic one-idea notes live in `wiki/` as
  `zet-*.md` with tag `type/zet`. These are primary sources and historical
  records. Distilled evergreen wiki cards should link back to zet as primary
  sources. Use `@type: [CreativeWork, Zet]` to distinguish them.
- Search first: Check the wiki before you make a new record. Link to existing
  items to prevent duplicates.
- Auto-link: Link mentioned people, projects, and concepts to their wiki records
  using WikiLinks `[[slug]]` (the "One Right Way" for internal links). Follow
  the
  [[obsidian-markdown]](file:///skills/obsidian/markdown/skill.md)
  skill for syntax.
- Proactive item creation: When referencing a future event, person, project, or
  concept that doesn't exist in the wiki yet, create a stub record immediately.
  Perform a brief web search to include high-level context—acting as a technical
  dossier—that includes location, parent organization, or core mission, along
  with relevant external links (portfolios, social media profiles, or GitHub
  repos) to ensure the record is immediately useful for connection-forming. This
  enables canonical linking and ensures follow-ups are not lost. Add a todo to
  populate deeper details later.
- Update records: Update the `wiki/` record immediately when you find new
  details about a person or project.
- Clean names: Use lowercase kebab-case for all filenames (e.g.,
  `opal-security.md`). Do not use spaces or uppercase letters.
- Zet filenames: Use `zet-YYYYMMDDHHMM-[slug].md` in `raw/` (e.g.,
  `zet-202604090045-agentic-unification.md`) so zet sort by time and stay
  unique. Semantic-only names are for living wiki cards (people, projects); zet
  always use the timestamp prefix.
- Progressive disclosure: Avoid a global "master index" file. `AGENTS.md` is the
  source of truth for vault navigation; discover content by searching `wiki/`.
- Hub cascade: Update relevant hubs recursively to reflect changes. Canonical
  hubs include:
  - `network.md` (People & Organizations)
  - `projects.md` (Active & Past Projects)
  - `opportunities.md` (Leads & Potential Work)
  - `concepts.md` (Engineering & Design Ideas)
  - `index.md` (High-level Navigation)
- Canonical frontmatter: Use JSON-LD style properties from
  [Schema.org](https://schema.org) in all markdown files. Quote keys starting
  with `@` (e.g., `"@type": "Person"`) and include a canonical `@context` with
  property-to-ID mappings for semantic properties.

  ### Person records

  All person records in `wiki/` should use this canonical schema:

  ```yaml
  "@context":
    "@vocab": "https://schema.org/"
    "wiki": "https://{{owner}}.github.io/{{repo}}/wiki/"
    "foaf": "http://xmlns.com/foaf/0.1/"
  "@type": Person
  givenName: FirstName
  familyName: LastName
  jobTitle: Role
  worksFor:
    - "@id": wiki:org-name.md
  url: https://example.com
  sameAs:
    - https://twitter.com/handle
    - https://github.com/handle
  foaf:account:
    foaf:accountName: handle
    foaf:accountServiceHomepage: https://twitter.com
  knows:
    - "@id": wiki:person.md
  colleague:
    - "@id": wiki:person.md
  family:
    - "@id": wiki:person.md
  status: permanent | one-off
  context: One-liner describing the relationship
  keywords:
    - priority/high
    - status/active
  dateCreated: "YYYY-MM-DD"
  ```

  **Required for Person records:** `@type`, `givenName`, `familyName`, `context`, `status`, `dateCreated`

  **Use `status: permanent`** for recurring relationships (colleagues, friends, family).
  **Use `status: one-off`** for single-interaction connections.

  Rely on these properties instead of `type/*` tags. These properties are the
  single source of truth for record types and relationships.

  **Network view:** `wiki/network.md` is auto-generated from frontmatter queries — do not edit manually. Edit individual person records to update the network.

## SHACL Validation

Before committing changes to wiki files, validate frontmatter against the canonical schema:

```bash
uv run python -m src shacl validate
```

Summary view:
```bash
uv run python -m src shacl validate --summary
```

SPARQL queries:
```bash
uv run python -m src sparql --dry-run
uv run python -m src sparql "PREFIX schema: <https://schema.org/> SELECT ?name WHERE { ?s a schema:Person }"
```

This is required — CI will block commits with invalid frontmatter. See `.github/workflows/shacl-validation.yml` for the automated check.

## Semantic Inference

The vault uses OWL-RL inference to maintain a flexible and robust query layer. Logic for semantic mappings and bidirectional relationships lives in `reasoning/`, itemized by standard (e.g., `foaf.ttl`, `dc.ttl`) and internal logic (e.g., `schema.ttl`).

- **Canonical First** — Agents must always prioritize writing canonical Schema.org properties (e.g., `dateCreated`, `keywords`). Inference is a safety net for legacy or external data, not a license for inconsistent writes.
- **Proactive mapping** — If you discover a new frontmatter key variation, add it as an `owl:equivalentProperty` to the appropriate file in `reasoning/` immediately.
- **SHACL as the Enforcer** — While reasoning makes variants queryable, SHACL validation still flags them as non-standard to encourage data hardening and normalization.
- **Verification** — After updating inference axioms, verify with a SPARQL query to ensure the expected triples are being materialized.

## Information preservation

- **Human work takes priority** — Never overwrite manual notes or roles with
  automated AI summaries.
- **Merge, do not replace** — Append new insights from transcripts while you
  keep the original manual context intact.

## Refactoring

- Immediate staging: Stage renames (`git add .`) immediately so Git tracks them
  correctly.
- Link audits: Search for and fix all internal links after you move any files.

## Self-healing

Maintain the vault's integrity by proactively addressing structural and semantic decay.

- **Link audits** — Whenever you edit a file, check for and repair broken internal
  links (`[[slug]]`) within the file and related hubs.
- **Metadata reconciliation** — If you discover new information about a person or
  organization (e.g., a new job or Twitter handle), update their canonical wiki
  record immediately and propagate the change across relevant hubs. For key
  ecosystem members (e.g., Substrate/Zo team), verify specific leadership roles
  (CEO vs Co-founder) against the SSoT to prevent generic role assignment.
- **Task triage** — Proactively mark completed tasks in `wiki/daily-*.md` and
  `wiki/reminders.md` when you observe them being resolved in the conversation or
  code.
- **Guidelines evolution** — If a rule in `AGENTS.md` is consistently leading to
  friction or entropy, propose a revision to the user.

## Surfacing cadence

- **Daily Heartbeat** — Write a summary, track priorities, and plan the next day
  at Midnight PST. Generated automatically by the `daily` skill.
- **Hourly Heartbeat** — Proactively synthesizes recent activity, triages action
  items, and connects loose ends at the top of every hour. Handled by the
  `hourly` skill.
- **On-demand requests** — Answer questions and surface notes as the user
  requests them.
- **Proactive monitoring** — Nudge the user regarding blockers or monitor
  relevant GitHub issues.

## Todo list convention

When the user says "todo list", "my todos", or "tasks", default to today's
daily review file: `wiki/daily-YYYY-MM-DD.md`. Infer the date from context.

### Semantic task management

Actions live as individual wiki files with `@type: Action` frontmatter. Use the
`action-` prefix for discoverability (e.g., `wiki/action-apply-govini.md`).

- **Create actions** using `skills/book/action/skill.md`. One file per action.
- **Complete actions** by setting `actionStatus: CompletedActionStatus` on the
  action file. Add `dateCompleted` if useful.
- **Do NOT embed `potentialAction` arrays** in daily reviews, reminders, or other
  files. Each action is its own SSoT.
- **Link actions** to parent projects/people via `about: "@id": wiki:slug.md`.
- **Priority** — Set `priority: high | medium | low` to control surfacing frequency.

### Backoff surfacing

The daily heartbeat surfaces actions using priority-weighted exponential backoff
instead of showing everything every day. See `skills/book/daily/config.md` for
the schedule parameters.

| Priority | Base | Multiplier | Max interval |
|----------|------|-----------|-------------|
| `high`   | 1d   | 1.5x      | 3d          |
| `medium` | 2d   | 2x        | 7d          |
| `low`    | 3d   | 2x        | 14d         |

When the daily skill surfaces an action, it increments `surfaceCount` and
updates `lastSurfaced` on the action file. If the user interacts with an action
(mentions it, edits it), reset `surfaceCount` to 0.

## Backlog

`wiki/reminders.md` is a hub page with a Dataview query against `action-*.md`
files. It does not store action data directly. All actions live in their own
files regardless of whether they are "active" or "someday/maybe"; priority
determines surfacing frequency.

## Backlog triage cadence

Quarterly (or on request), review all `low` priority actions. Promote, archive,
or discard each item. Never let actions sit untouched for more than six months
without a review.

## Completed work: zet/wiki convergence

Zets (atomic notes) have been migrated from `raw/` to `wiki/` as first-class
records. They are distinguished by the `zet-` prefix and `@type: [CreativeWork, Zet]`
frontmatter.

## Style guidelines

- Use sentence case headings: Capitalize only the first word and proper nouns in
  headings.
- Use active voice: Write in the active voice and use imperative verbs when
  giving instructions.
- Use unordered lists: Avoid unnecessarily numbered or ordered lists when
  the order is arbitrary.
- Minimal stylistic formatting: Do not use bold (\*\*) or other stylistic
  formatting unless grammatically necessary.
- Formal conjunctions: Avoid the em-dash character as an awkward conjunction;
  use a more formal conjunction instead.
- Handle formatting: For person records, list primary social/professional handles
  on a single line immediately below the title heading. Format:
  `**Handles:** [handle](link) (Platform) · [handle](link) (Platform)`.
- Link audit cadence: When editing any wiki file, check for unlinked mentions of
  "High-Priority Slugs" identified in [[index.md]] or [[projects.md]] (e.g.,
  Zo, Letta, Substrate) and repair them ambiently.

## New file scaffolds

Use the skills under `skills/` when creating structured notes; each folder has
`skill.md` (workflow) and `template.md` (scaffold):

| Kind              | Path                   |
| ----------------- | ---------------------- |
| Daily review      | `skills/book/daily/`   |
| Hourly heartbeat  | `skills/book/hourly/`  |
| Person            | `skills/book/person/`  |
| Project           | `skills/book/project/` |
| Idea              | `skills/book/idea/`    |
| Zet (atomic note) | `skills/book/zet/`     |

## Core capabilities

| Kind           | Path                        |
| -------------- | --------------------------- |
| Web clipper    | `skills/web/defuddle/`      |
| Obsidian CLI   | `skills/obsidian/cli/`      |
| Markdown tools | `skills/obsidian/markdown/` |
| Data views     | `skills/obsidian/bases/`    |
| Canvas tools   | `skills/obsidian/canvas/`   |

## Nightly surfacing agent setup

To set up the book nightly surfacing agent, create a scheduled agent with:

- **RRULE:** `FREQ=DAILY;BYHOUR=0;BYMINUTE=0` (midnight PST)
- **Skill:** `skills/book/daily/skill.md` (workflow) + `skills/book/daily/config.md` (configuration)
- **Instruction:** Run the book nightly surfacing agent — follow `skills/book/daily/skill.md` and `skills/book/daily/config.md` to generate the daily review, commit it, and push to origin main
- **Delivery:** email

The agent generates `wiki/daily-YYYY-MM-DD.md` using the daily skill template, covering yesterday's progress, today's priorities, project status, and open actions.

## Zo Space Mirror
Live at: https://etok.zo.space
Source: https://github.com/{{owner}}/{{repo}}
This repo follows the standard Zo Space mirror sync convention.
