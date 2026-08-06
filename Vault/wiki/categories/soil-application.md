---
type: category
name: Внесение в почву
action_category: SOIL_APPLICATION
substances: []
---

# Внесение в почву (SOIL_APPLICATION)

Корневые подкормки, полив, капельное орошение, мелиоранты, биостимуляция ризосферы (16 строк).

## Вещества по CSV
```dataview
TABLE efficacy_csv AS "Эффективность", validation_status AS "Статус", crops.tomato AS "Томат", crops.cucumber AS "Огурец", crops.strawberry AS "Клубника"
FROM "wiki/substances"
WHERE action_category = "SOIL_APPLICATION"
SORT validation_status ASC
```
