---
type: category
name: Управление плодоношением
action_category: FRUIT_MANAGEMENT
substances: []
---

# Управление плодоношением (FRUIT_MANAGEMENT)

Завязывание, рост, созревание и качество плодов: фиксаторы завязи, регуляторы созревания, прореживание (23 строки).

## Вещества по CSV
```dataview
TABLE efficacy_csv AS "Эффективность", validation_status AS "Статус", crops.tomato AS "Томат", crops.cucumber AS "Огурец", crops.strawberry AS "Клубника"
FROM "wiki/substances"
WHERE contains(action_category, \"FRUIT_MANAGEMENT\")
SORT validation_status ASC
```
