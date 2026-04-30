---
"@context": "https://schema.org"
"@type": "Review"
dateCreated: "{{date}}"
---

# Daily review

## Date

{{date}}

## Yesterday's progress

-

## Today's surfaced actions

```dataviewjs
const BACKOFF = {
  high:   { base: 1, mult: 1.5, max: 3,  grace: 3 },
  medium: { base: 2, mult: 2,   max: 7,  grace: 0 },
  low:    { base: 3, mult: 2,   max: 14, grace: 0 },
};

const today = new Date();
const toDate = (s) => s ? new Date(s) : null;
const daysBetween = (a, b) => Math.floor((b - a) / 86400000);

const actions = dv.pages('"wiki"')
  .where(p => p["@type"] === "Action" && p.actionStatus === "PotentialActionStatus")
  .where(p => {
    const priority = p.priority || "medium";
    const cfg = BACKOFF[priority] || BACKOFF.medium;
    const count = p.surfaceCount || 0;
    const last = toDate(p.lastSurfaced);
    const dl = toDate(p.deadline);

    // Never surfaced before — always show.
    if (!last) return true;

    // Deadline within 2 days — always show.
    if (dl && daysBetween(today, dl) <= 2) return true;

    // High priority grace period.
    if (priority === "high" && count < cfg.grace) return true;

    // Exponential backoff.
    const interval = Math.min(cfg.base * Math.pow(cfg.mult, count), cfg.max);
    return daysBetween(last, today) >= interval;
  });

for (const pri of ["high", "medium", "low"]) {
  const group = actions.where(p => (p.priority || "medium") === pri);
  if (group.length > 0) {
    dv.header(3, pri.charAt(0).toUpperCase() + pri.slice(1) + " priority");
    dv.table(
      ["Action", "Created", "Surfaced"],
      group.map(p => [p.file.link, p.dateCreated, p.surfaceCount || 0])
    );
  }
}

if (actions.length === 0) {
  dv.paragraph("*No actions surfaced today. All caught up!*");
}
```

## Projects status

### Active

| Project | Status | Blocker |
| ------- | ------ | ------- |

### Needs attention

| Project | Issue | Action |
| ------- | ----- | ------ |

## Open questions

-

## Notes

-

