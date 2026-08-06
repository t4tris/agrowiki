---
type: class
name: Гербициды
class_csv: ['Synthetic auxin']
substances: []
---

# Класс: Гербициды

Синтетические ауксиновые гербициды (2,4-D, MCPA, дикамба, пиклорам, триклопир): сверхоптимальные дозы ауксинов вызывают неконтролируемый рост и гибель двудольных сорняков. В CSV выделены по Mode_of_Action (Auxin herbicide, Weed control at high dose).

CSV-классы семейства: `Synthetic auxin`.

## Вещества
```dataview
TABLE class AS "Класс (CSV)", efficacy_csv AS "Эффективность", validation_status AS "Статус"
FROM "wiki/substances"
WHERE contains(class_family, "herbicides")
SORT validation_status ASC
```

## Связанные пестицидные семейства
- [[fungicides|Фунгициды]] · [[insecticides|Инсектициды]] · [[herbicides|Гербициды]] · [[nematicides|Нематоциды]] · [[miticides|Митициды]] · [[antibacterials|Антибактериальные]] · [[antivirals|Противовирусные]]
