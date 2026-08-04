---
type: category
name: Регуляция роста
action_category: GROWTH_REGULATION
substances: []
---

# Регуляция роста (GROWTH_REGULATION)

Ретарданты и стимуляторы вегетативного роста, ветвление, высота растения (22 строки).

## Вещества по CSV
```dataview
TABLE efficacy_csv AS "Эффективность", validation_status AS "Статус", crops.tomato AS "Томат", crops.cucumber AS "Огурец", crops.strawberry AS "Клубника"
FROM "wiki/substances"
WHERE action_category = "GROWTH_REGULATION"
SORT validation_status ASC
```
