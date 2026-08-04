---
type: class
name: Фенольные соединения
class_csv: ['Phenolic', 'Polyphenol']
substances: []
---

# Класс: Фенольные соединения

Фенолкислоты, флавоноиды, лигнины: антиоксиданты, сигнальные молекулы, защита от УФ.

CSV-классы семейства: `Phenolic`, `Polyphenol`.

## Вещества
```dataview
TABLE class AS "Класс (CSV)", efficacy_csv AS "Эффективность", validation_status AS "Статус"
FROM "wiki/substances"
WHERE contains(class_family, "phenolics_polyphenols")
SORT validation_status ASC
```
