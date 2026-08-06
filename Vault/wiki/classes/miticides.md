---
type: class
name: Митициды (акарициды)
class_csv: []
substances: []
---

# Класс: Митициды (акарициды)

Средства против растительноядных клещей. В CSV веществ нет — семейство создано для полноты классификации пестицидов.

CSV-классы семейства: .

## Вещества
```dataview
TABLE class AS "Класс (CSV)", efficacy_csv AS "Эффективность", validation_status AS "Статус"
FROM "wiki/substances"
WHERE contains(class_family, "miticides")
SORT validation_status ASC
```

## Связанные пестицидные семейства
- [[fungicides|Фунгициды]] · [[insecticides|Инсектициды]] · [[herbicides|Гербициды]] · [[nematicides|Нематоциды]] · [[miticides|Митициды]] · [[antibacterials|Антибактериальные]] · [[antivirals|Противовирусные]]
