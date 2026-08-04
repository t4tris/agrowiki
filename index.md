# Index — Агрономическая вики

База валидированных агрономических веществ (267 веществ, 3 фокусные культуры).
Схема: [[AGENTS.md]] · Журнал: [[log]] · Очередь: [[task_queue]] · Дашборд: [[validation]]

## По статусу валидации
```dataview
TABLE efficacy_csv AS "Эффективность (CSV)", evidence_level AS "Доказательность"
FROM "wiki/substances"
WHERE validation_status != "verified" AND validation_status != "corrected"
SORT validation_status ASC
```

## По культурам
- [[Томат]] · [[Огурец]] · [[Клубника]]

## Структура
- [[wiki/substances|Вещества]] · [[wiki/categories|Категории]] · [[wiki/classes|Классы]] · [[wiki/mechanisms|Механизмы]] · [[wiki/syntheses|Синтезы]]
