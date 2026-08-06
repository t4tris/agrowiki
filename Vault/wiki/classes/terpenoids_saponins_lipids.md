---
type: class
name: Терпеноиды, сапонины, липиды
class_csv: ['Sesquiterpene lactone', 'Saponin', 'Phospholipid', 'Long-chain alcohol', 'Aldehyde']
substances: []
---

# Класс: Терпеноиды, сапонины, липиды

Вторичные метаболиты и липиды: Triacontanol, Artemisinin, диосгенин и др.

CSV-классы семейства: `Sesquiterpene lactone`, `Saponin`, `Phospholipid`, `Long-chain alcohol`, `Aldehyde`.

## Вещества
```dataview
TABLE class AS "Класс (CSV)", efficacy_csv AS "Эффективность", validation_status AS "Статус"
FROM "wiki/substances"
WHERE contains(class_family, "terpenoids_saponins_lipids")
SORT validation_status ASC
```
