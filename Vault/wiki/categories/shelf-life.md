---
type: category
name: Хранение и лёжкость (shelf-life)
action_category: SHELF_LIFE
substances: []
---

# Хранение и лёжкость (shelf-life) (SHELF_LIFE)

Постхарвест-обработки и управление лёжкостью: продление срока хранения, подавление гнилей при хранении, покрытия, регуляторы созревания/старения (в CSV категории нет — расширение схемы 2026-08-06; назначается по подтверждённым постхарвест-фактам карточек).

## Вещества по CSV
```dataview
TABLE efficacy_csv AS "Эффективность", validation_status AS "Статус", crops.tomato AS "Томат", crops.cucumber AS "Огурец", crops.strawberry AS "Клубника"
FROM "wiki/substances"
WHERE contains(action_category, \"SHELF_LIFE\")
SORT validation_status ASC
```
