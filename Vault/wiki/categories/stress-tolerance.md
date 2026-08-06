---
type: category
name: Устойчивость к стрессу
action_category: STRESS_TOLERANCE
substances: []
---

# Устойчивость к стрессу (STRESS_TOLERANCE)

Защита от абиотических стрессов: засуха, жара, соль, заморозки (3 строки).

## Вещества по CSV
```dataview
TABLE efficacy_csv AS "Эффективность", validation_status AS "Статус", crops.tomato AS "Томат", crops.cucumber AS "Огурец", crops.strawberry AS "Клубника"
FROM "wiki/substances"
WHERE action_category = "STRESS_TOLERANCE"
SORT validation_status ASC
```
