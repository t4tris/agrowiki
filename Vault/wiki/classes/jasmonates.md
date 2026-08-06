---
type: class
name: Жасмонаты
class_csv: ['Jasmonate', 'Synthetic jasmonate']
substances: []
---

# Класс: Жасмонаты

Сигнальные липидные гормоны: защита от стресса, аромат, отпугивание вредителей.

CSV-классы семейства: `Jasmonate`, `Synthetic jasmonate`.

## Вещества
```dataview
TABLE class AS "Класс (CSV)", efficacy_csv AS "Эффективность", validation_status AS "Статус"
FROM "wiki/substances"
WHERE contains(class_family, "jasmonates")
SORT validation_status ASC
```
