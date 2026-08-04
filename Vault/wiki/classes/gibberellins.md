---
type: class
name: Гиббереллины и ингибиторы GA
class_csv: ['Gibberellin', 'GA inhibitor']
substances: []
---

# Класс: Гиббереллины и ингибиторы GA

Вытягивание стебля, прорастание, цветение; ингибиторы — ретарданты (Paclobutrazol и др.).

CSV-классы семейства: `Gibberellin`, `GA inhibitor`.

## Вещества
```dataview
TABLE class AS "Класс (CSV)", efficacy_csv AS "Эффективность", validation_status AS "Статус"
FROM "wiki/substances"
WHERE contains(class_family, "gibberellins")
SORT validation_status ASC
```
