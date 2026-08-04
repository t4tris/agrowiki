---
type: category
name: Усиление фотосинтеза
action_category: PHOTOSYNTHESIS_ENHANCEMENT
substances: []
---

# Усиление фотосинтеза (PHOTOSYNTHESIS_ENHANCEMENT)

Стимуляция фотосинтетического аппарата, содержание хлорофилла, CO2-фиксация (3 строки).

## Вещества по CSV
```dataview
TABLE efficacy_csv AS "Эффективность", validation_status AS "Статус", crops.tomato AS "Томат", crops.cucumber AS "Огурец", crops.strawberry AS "Клубника"
FROM "wiki/substances"
WHERE action_category = "PHOTOSYNTHESIS_ENHANCEMENT"
SORT validation_status ASC
```
