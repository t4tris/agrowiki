---
type: class
name: Биостимуляторы и экстракты
class_csv: ['Biostimulant', 'Marine biostimulant', 'Natural biostimulant', 'Organic extract', 'Organic byproduct', 'Fungicide/Biostimulant']
substances: []
---

# Класс: Биостимуляторы и экстракты

Экстракты водорослей (Ascophyllum, Ecklonia), гуминовые вещества, микробные биостимуляторы.

CSV-классы семейства: `Biostimulant`, `Marine biostimulant`, `Natural biostimulant`, `Organic extract`, `Organic byproduct`, `Fungicide/Biostimulant`.

## Вещества
```dataview
TABLE class AS "Класс (CSV)", efficacy_csv AS "Эффективность", validation_status AS "Статус"
FROM "wiki/substances"
WHERE contains(class_family, "biostimulants_extracts")
SORT validation_status ASC
```
