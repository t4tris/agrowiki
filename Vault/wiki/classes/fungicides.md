---
type: class
name: Фунгициды
class_csv: ['Triazole fungicide', 'Triazole', 'Benzimidazole fungicide', 'Strobilurin fungicide', 'Anilinopyrimidine fungicide', 'Multi-site fungicide', 'Phenylpyrrole fungicide', 'Phosphonate fungicide/biostimulant']
substances: []
---

# Класс: Фунгициды

Химические средства защиты от грибных болезней: ингибиторы стеролов, дыхания, микротрубочек.

CSV-классы семейства: `Triazole fungicide`, `Triazole`, `Benzimidazole fungicide`, `Strobilurin fungicide`, `Anilinopyrimidine fungicide`, `Multi-site fungicide`, `Phenylpyrrole fungicide`, `Phosphonate fungicide/biostimulant`.

## Вещества
```dataview
TABLE class AS "Класс (CSV)", efficacy_csv AS "Эффективность", validation_status AS "Статус"
FROM "wiki/substances"
WHERE contains(class_family, "fungicides")
SORT validation_status ASC
```

## Связанные пестицидные семейства
- [[fungicides|Фунгициды]] · [[insecticides|Инсектициды]] · [[herbicides|Гербициды]] · [[nematicides|Нематоциды]] · [[acaricides|Акарициды]] · [[antibacterials|Антибактериальные]] · [[antivirals|Противовирусные]]
