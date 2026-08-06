---
type: class
name: Синтетические регуляторы роста
class_csv: ['Nitrophenolate', 'Growth inhibitor', 'Acylcyclohexanedione', 'Quaternary ammonium', 'Synthetic tertiary amine', 'Defoliant/regulator', 'Pyrimidine', 'Diazine', 'Synthetic polymer', 'Halogenated pyruvate', 'Alkylating agent', 'Nucleoside analog', 'Polymeric guanidine', 'Nitrile']
substances: []
---

# Класс: Синтетические регуляторы роста

Синтетические соединения, регулирующие рост: нитрофеноляты (Atonik), DA-6, дефолианты.

CSV-классы семейства: `Nitrophenolate`, `Growth inhibitor`, `Acylcyclohexanedione`, `Quaternary ammonium`, `Synthetic tertiary amine`, `Defoliant/regulator`, `Pyrimidine`, `Diazine`, `Synthetic polymer`, `Halogenated pyruvate`, `Alkylating agent`, `Nucleoside analog`, `Polymeric guanidine`, `Nitrile`.

## Вещества
```dataview
TABLE class AS "Класс (CSV)", efficacy_csv AS "Эффективность", validation_status AS "Статус"
FROM "wiki/substances"
WHERE contains(class_family, "synthetic_growth_regulators")
SORT validation_status ASC
```
