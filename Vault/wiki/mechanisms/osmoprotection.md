---
type: mechanism
name: Осмопротекция
substances: []
---

# Механизм: Осмопротекция

Совместимые осмолиты (Glycine Betaine, Proline, трегалоза) стабилизируют белки и мембраны при засухе, засолении и заморозках.

## Вещества
```dataview
TABLE class_family AS "Семейство", efficacy_csv AS "Эффективность", validation_status AS "Статус"
FROM "wiki/substances"
WHERE mechanism = "osmoprotection"
SORT validation_status ASC
```
