---
type: class
name: Индоламины
class_csv: ['Indolamine', 'Indolamine derivative', 'Indoleamine']
substances: []
---

# Класс: Индоламины

Производные триптофана: серотонин, мелатонин — антиоксиданты и регуляторы развития.

CSV-классы семейства: `Indolamine`, `Indolamine derivative`, `Indoleamine`.

## Вещества
```dataview
TABLE class AS "Класс (CSV)", efficacy_csv AS "Эффективность", validation_status AS "Статус"
FROM "wiki/substances"
WHERE contains(class_family, "indolamines")
SORT validation_status ASC
```
