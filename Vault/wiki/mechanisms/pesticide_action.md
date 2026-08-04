---
type: mechanism
name: Пестицидное действие
substances: []
---

# Механизм: Пестицидное действие

Фунгициды (триазолы, стробилурины, бензимидазолы) и инсектициды (неоникотиноиды): прямое подавление патогенов и вредителей.

## Вещества
```dataview
TABLE class_family AS "Семейство", efficacy_csv AS "Эффективность", validation_status AS "Статус"
FROM "wiki/substances"
WHERE mechanism = "pesticide_action"
SORT validation_status ASC
```
