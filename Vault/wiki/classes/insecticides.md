---
type: class
name: Инсектициды
class_csv: ['Neonicotinoid']
substances: []
---

# Класс: Инсектициды

Химические средства защиты от насекомых: неоникотиноиды (агонисты nAChR).

CSV-классы семейства: `Neonicotinoid`.

## Вещества
```dataview
TABLE class AS "Класс (CSV)", efficacy_csv AS "Эффективность", validation_status AS "Статус"
FROM "wiki/substances"
WHERE contains(class_family, "insecticides")
SORT validation_status ASC
```
