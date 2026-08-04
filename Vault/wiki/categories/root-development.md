---
type: category
name: Развитие корневой системы
action_category: ROOT_DEVELOPMENT
substances: []
---

# Развитие корневой системы (ROOT_DEVELOPMENT)

Стимуляция корнеобразования: ауксины, укоренители черенков, ризогенез (10 строк).

## Вещества по CSV
```dataview
TABLE efficacy_csv AS "Эффективность", validation_status AS "Статус", crops.tomato AS "Томат", crops.cucumber AS "Огурец", crops.strawberry AS "Клубника"
FROM "wiki/substances"
WHERE action_category = "ROOT_DEVELOPMENT"
SORT validation_status ASC
```
