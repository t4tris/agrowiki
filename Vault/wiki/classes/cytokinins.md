---
type: class
name: Цитокинины
class_csv: ['Cytokinin', 'Synthetic cytokinin', 'Phenylurea cytokinin', 'Cytokinin analog']
substances: []
---

# Класс: Цитокинины

Деление клеток, побегообразование, задержка старения, выход из покоя.

CSV-классы семейства: `Cytokinin`, `Synthetic cytokinin`, `Phenylurea cytokinin`, `Cytokinin analog`.

## Вещества
```dataview
TABLE class AS "Класс (CSV)", efficacy_csv AS "Эффективность", validation_status AS "Статус"
FROM "wiki/substances"
WHERE contains(class_family, "cytokinins")
SORT validation_status ASC
```
