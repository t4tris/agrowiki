---
type: class
name: Аминокислоты и полиамины
class_csv: ['Amino Acid', 'Amino acid', 'Polyamine', 'Osmoprotectant']
substances: []
---

# Класс: Аминокислоты и полиамины

Строительные блоки белков, предшественники гормонов, осмопротекторы (Glycine Betaine, Proline).

CSV-классы семейства: `Amino Acid`, `Amino acid`, `Polyamine`, `Osmoprotectant`.

## Вещества
```dataview
TABLE class AS "Класс (CSV)", efficacy_csv AS "Эффективность", validation_status AS "Статус"
FROM "wiki/substances"
WHERE contains(class_family, "amino_acids_polyamines")
SORT validation_status ASC
```
