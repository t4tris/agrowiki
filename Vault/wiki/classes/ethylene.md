---
type: class
name: Этилен и регуляторы созревания
class_csv: ['Ethylene', 'Ethylene inhibitor', 'Ethylene releaser']
substances: []
---

# Класс: Этилен и регуляторы созревания

Созревание, старение, опадение; ингибиторы (1-MCP) и стимуляторы (Ethephon).

CSV-классы семейства: `Ethylene`, `Ethylene inhibitor`, `Ethylene releaser`.

## Вещества
```dataview
TABLE class AS "Класс (CSV)", efficacy_csv AS "Эффективность", validation_status AS "Статус"
FROM "wiki/substances"
WHERE contains(class_family, "ethylene")
SORT validation_status ASC
```
