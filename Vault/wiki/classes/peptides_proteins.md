---
type: class
name: Пептиды и белки
class_csv: ['Peptide', 'Peptide hormone', 'Tripeptide', 'Enzyme', 'RNA']
substances: []
---

# Класс: Пептиды и белки

Сигнальные пептиды (CLE, CEP, PSK), ферменты, регуляторные белки.

CSV-классы семейства: `Peptide`, `Peptide hormone`, `Tripeptide`, `Enzyme`, `RNA`.

## Вещества
```dataview
TABLE class AS "Класс (CSV)", efficacy_csv AS "Эффективность", validation_status AS "Статус"
FROM "wiki/substances"
WHERE contains(class_family, "peptides_proteins")
SORT validation_status ASC
```
