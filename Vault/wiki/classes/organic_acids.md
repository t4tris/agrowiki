---
type: class
name: Органические кислоты
class_csv: ['Organic Acid']
substances: []
---

# Класс: Органические кислоты

Цитрат, сукцинат, фульвовые кислоты: метаболизм, хелатирование, pH, энергетика.

CSV-классы семейства: `Organic Acid`.

## Вещества
```dataview
TABLE class AS "Класс (CSV)", efficacy_csv AS "Эффективность", validation_status AS "Статус"
FROM "wiki/substances"
WHERE contains(class_family, "organic_acids")
SORT validation_status ASC
```
