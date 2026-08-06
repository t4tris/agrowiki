---
type: category
name: Обработка семян
action_category: SEED_TREATMENT
substances: []
---

# Обработка семян (SEED_TREATMENT)

Предпосевная обработка: замачивание, инкрустация, прайминг. Цель — прорастание, стартовая энергия, защита всходов (27 строк).

## Вещества по CSV
```dataview
TABLE efficacy_csv AS "Эффективность", validation_status AS "Статус", crops.tomato AS "Томат", crops.cucumber AS "Огурец", crops.strawberry AS "Клубника"
FROM "wiki/substances"
WHERE action_category = "SEED_TREATMENT"
SORT validation_status ASC
```
