---
type: category
name: Внекорневая обработка
action_category: FOLIAR_APPLICATION
substances: []
---

# Внекорневая обработка (FOLIAR_APPLICATION)

Обработка растений по листу (опрыскивание): биостимуляторы, регуляторы роста, удобрения. Самая массовая категория CSV (171 строка).

## Вещества по CSV
```dataview
TABLE efficacy_csv AS "Эффективность", validation_status AS "Статус", crops.tomato AS "Томат", crops.cucumber AS "Огурец", crops.strawberry AS "Клубника"
FROM "wiki/substances"
WHERE action_category = "FOLIAR_APPLICATION"
SORT validation_status ASC
```
