---
type: class
name: Брассиностероиды
class_csv: ['Brassinosteroid']
substances: []
---

# Класс: Брассиностероиды

Стероидные гормоны: рост, стрессоустойчивость, фотоморфогенез.

CSV-классы семейства: `Brassinosteroid`.

## Вещества
```dataview
TABLE class AS "Класс (CSV)", efficacy_csv AS "Эффективность", validation_status AS "Статус"
FROM "wiki/substances"
WHERE contains(class_family, "brassinosteroids")
SORT validation_status ASC
```
