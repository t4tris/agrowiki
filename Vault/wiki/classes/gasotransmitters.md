---
type: class
name: Газотрансмиттеры
class_csv: ['Gasotransmitter', 'Iron nitrosyl complex', 'Sulfide salt']
substances: []
---

# Класс: Газотрансмиттеры

NO, H2S, CO — газовые сигнальные молекулы (доноры оксида азота, сульфида).

CSV-классы семейства: `Gasotransmitter`, `Iron nitrosyl complex`, `Sulfide salt`.

## Вещества
```dataview
TABLE class AS "Класс (CSV)", efficacy_csv AS "Эффективность", validation_status AS "Статус"
FROM "wiki/substances"
WHERE contains(class_family, "gasotransmitters")
SORT validation_status ASC
```
