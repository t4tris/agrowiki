---
type: class
name: Углеводы
class_csv: ['Disaccharide', 'Polysaccharide', 'Monosaccharide', 'Carbohydrate source']
substances: []
---

# Класс: Углеводы

Сахара и полисахариды: энергия, осмопротекция, структура клеточной стенки.

CSV-классы семейства: `Disaccharide`, `Polysaccharide`, `Monosaccharide`, `Carbohydrate source`.

## Вещества
```dataview
TABLE class AS "Класс (CSV)", efficacy_csv AS "Эффективность", validation_status AS "Статус"
FROM "wiki/substances"
WHERE contains(class_family, "carbohydrates")
SORT validation_status ASC
```
