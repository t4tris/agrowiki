---
type: class
name: Антибактериальные
class_csv: ['Polymeric guanidine', 'Oxidant']
substances: []
---

# Класс: Антибактериальные

Бактерициды и дезинфектанты: полимерные гуанидины (PHMG), активный хлор (HOCl, гипохлорит натрия).

CSV-классы семейства: `Polymeric guanidine`, `Oxidant`.

## Вещества
```dataview
TABLE class AS "Класс (CSV)", efficacy_csv AS "Эффективность", validation_status AS "Статус"
FROM "wiki/substances"
WHERE contains(class_family, "antibacterials")
SORT validation_status ASC
```

## Связанные пестицидные семейства
- [[fungicides|Фунгициды]] · [[insecticides|Инсектициды]] · [[herbicides|Гербициды]] · [[nematicides|Нематоциды]] · [[miticides|Митициды]] · [[antibacterials|Антибактериальные]] · [[antivirals|Противовирусные]]
