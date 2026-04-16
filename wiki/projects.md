---
"@context":
  "@vocab": "https://schema.org/"
  wiki: "https://zowiki.etok.me/wiki/"
"@type": CollectionPage
"@id": "wiki:projects.md"
name: Projects
---

# 🚀 Projects

The living registry of active, planned, and archived work.

## 🟢 Active

```dataview
TABLE status, description
FROM "wiki"
WHERE "@type" = "Project" AND status = "active"
SORT dateModified DESC
```

## ⏳ Planned

```dataview
TABLE description
FROM "wiki"
WHERE "@type" = "Project" AND status = "planned"
```

---

[[index|↩ Back to Index]]
