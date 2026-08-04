---
type: class
name: Летучие органические соединения (VOC)
class_csv: ['VOC', 'Volatile compounds']
substances: []
---

# Класс: Летучие органические соединения (VOC)

Летучие сигналы растений: защита, коммуникация, ароматы.

CSV-классы семейства: `VOC`, `Volatile compounds`.

## Вещества
```dataview
TABLE class AS "Класс (CSV)", efficacy_csv AS "Эффективность", validation_status AS "Статус"
FROM "wiki/substances"
WHERE contains(class_family, "voc_volatiles")
SORT validation_status ASC
```
