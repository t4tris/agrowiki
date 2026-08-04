# Дашборд валидации

```dataview
TABLE validation_status AS "Статус", evidence_level AS "Доказательность",
      crops.tomato AS "Томат", crops.cucumber AS "Огурец", crops.strawberry AS "Клубника"
FROM "wiki/substances"
SORT validation_status ASC
```

## 🔴 Требуют внимания (conflicting)
```dataview
LIST
FROM "wiki/substances"
WHERE validation_status = "conflicting"
```

## ✅ Проверено (verified / corrected)
```dataview
LIST
FROM "wiki/substances"
WHERE validation_status = "verified" OR validation_status = "corrected"
SORT evidence_level DESC
```

## 📊 Прогресс
```dataview
TABLE length(rows) AS "Всего"
FROM "wiki/substances"
GROUP BY validation_status
```
