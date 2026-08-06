---
type: class
name: Элементы и минералы
class_csv: ['Beneficial element', 'Chelated nutrient', 'Metal / metal-oxide nanoparticles']
substances: []
---

# Класс: Элементы и минералы

Полезные элементы (Si, Co, Se), хелатированные микроудобрения, наночастицы.

CSV-классы семейства: `Beneficial element`, `Chelated nutrient`, `Metal / metal-oxide nanoparticles`.

## Вещества
```dataview
TABLE class AS "Класс (CSV)", efficacy_csv AS "Эффективность", validation_status AS "Статус"
FROM "wiki/substances"
WHERE contains(class_family, "elements_minerals")
SORT validation_status ASC
```
