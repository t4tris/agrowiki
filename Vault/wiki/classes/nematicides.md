---
type: class
name: Нематоциды
class_csv: []
substances: []
---

# Класс: Нематоциды

Средства против нематод. В CSV: артемизинин (MoA «Nematicidal agent») — заявка не подтверждена валидацией (insufficient_data).

CSV-классы семейства: .

## Вещества
```dataview
TABLE class AS "Класс (CSV)", efficacy_csv AS "Эффективность", validation_status AS "Статус"
FROM "wiki/substances"
WHERE contains(class_family, "nematicides")
SORT validation_status ASC
```

## Связанные пестицидные семейства
- [[fungicides|Фунгициды]] · [[insecticides|Инсектициды]] · [[herbicides|Гербициды]] · [[nematicides|Нематоциды]] · [[miticides|Митициды]] · [[antibacterials|Антибактериальные]] · [[antivirals|Противовирусные]]
