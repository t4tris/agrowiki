---
type: class
name: Сигналы SAR
class_csv: ['SAR Signal', 'Plant hormone + disaccharide']
substances: []
---

# Класс: Сигналы SAR

Сигналы системной приобретённой устойчивости: салициловая кислота и её индукторы.

CSV-классы семейства: `SAR Signal`, `Plant hormone + disaccharide`.

## Вещества
```dataview
TABLE class AS "Класс (CSV)", efficacy_csv AS "Эффективность", validation_status AS "Статус"
FROM "wiki/substances"
WHERE contains(class_family, "sar_signals_elicitors")
SORT validation_status ASC
```
