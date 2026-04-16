---
"@context":
  "@vocab": "https://schema.org/"
  wiki: "https://zowiki.etok.me/wiki/"
"@type": CollectionPage
"@id": "wiki:network.md"
name: Network
---

# 🌐 Network

The living registry of personal and professional connections.

## 👥 People

```dataview
LIST
FROM "wiki"
WHERE "@type" = "Person"
SORT name ASC
```

## 🤝 Relationships

```dataview
LIST
FROM "wiki"
WHERE "@type" = "Person" AND length(knows) > 0
```

---

[[index|↩ Back to Index]]
