---
type: class
name: АБК, стриголактоны и каррикины
class_csv: ['ABA', 'Strigolactone', 'Karrikin']
substances: []
---

# Класс: АБК, стриголактоны и каррикины

Абсцизовая кислота (стресс, устьица), стриголактоны (симбиоз, ветвление), каррикины (прорастание).

CSV-классы семейства: `ABA`, `Strigolactone`, `Karrikin`.

## Вещества
```dataview
TABLE class AS "Класс (CSV)", efficacy_csv AS "Эффективность", validation_status AS "Статус"
FROM "wiki/substances"
WHERE contains(class_family, "aba_strigolactones_karrikins")
SORT validation_status ASC
```
