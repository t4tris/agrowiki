---
type: class
name: Прочее
class_csv: ['Related', 'Oxidant', 'Solvent', 'Surfactant']
substances: []
---

# Класс: Прочее

Вспомогательные и трудно классифицируемые соединения: DMSO, децилглюкозид, пероксид водорода.

CSV-классы семейства: `Related`, `Oxidant`, `Solvent`, `Surfactant`.

## Вещества
```dataview
TABLE class AS "Класс (CSV)", efficacy_csv AS "Эффективность", validation_status AS "Статус"
FROM "wiki/substances"
WHERE contains(class_family, "other")
SORT validation_status ASC
```
