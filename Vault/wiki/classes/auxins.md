---
type: class
name: Ауксины
class_csv: ['Auxin', 'Synthetic auxin', 'Auxin transport inhibitor', 'Auxin-like', 'Aryloxy acid']
substances: []
---

# Класс: Ауксины

Натуральные и синтетические ауксины: ризогенез, тропизмы, апикальное доминирование, завязь.

CSV-классы семейства: `Auxin`, `Synthetic auxin`, `Auxin transport inhibitor`, `Auxin-like`, `Aryloxy acid`.

## Вещества
```dataview
TABLE class AS "Класс (CSV)", efficacy_csv AS "Эффективность", validation_status AS "Статус"
FROM "wiki/substances"
WHERE contains(class_family, "auxins")
SORT validation_status ASC
```
