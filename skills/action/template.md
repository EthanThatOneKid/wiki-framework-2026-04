---
"@context":
  "@vocab": "https://schema.org/"
  wiki: "https://{{owner}}.github.io/{{repo}}/wiki/"
"@type": Action
name: "{{name}}"
actionStatus: PotentialActionStatus
priority: "{{priority}}"
dateCreated: "{{date}}"
about:
  - "@id": "wiki:{{parent}}"
keywords:
  - "{{area}}"
---

# {{name}}

{{context}}

## Related

- [[{{parent}}]]

