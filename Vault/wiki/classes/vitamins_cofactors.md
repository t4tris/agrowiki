---
type: class
name: Витамины и кофакторы
class_csv: ['Vitamin', 'Vitamin-like']
substances: []
---

# Класс: Витамины и кофакторы

Аскорбиновая кислота, тиамин, ниацин, холин и др. — антиоксиданты и кофакторы метаболизма.

CSV-классы семейства: `Vitamin`, `Vitamin-like`.

## Вещества
```dataview
TABLE class AS "Класс (CSV)", efficacy_csv AS "Эффективность", validation_status AS "Статус"
FROM "wiki/substances"
WHERE contains(class_family, "vitamins_cofactors")
SORT validation_status ASC
```
