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

## 🟡 Частично подтверждено (partial)
```dataview
LIST
FROM "wiki/substances"
WHERE validation_status = "partial"
SORT evidence_level DESC
```

## ⚪ Нет данных (insufficient_data)
```dataview
LIST
FROM "wiki/substances"
WHERE validation_status = "insufficient_data"
```

## 🔄 Требуют Europe PMC-повторного запроса (orchestrator_fallback)
Вещества, у сабагентов которых Europe PMC был недоступен (IPv6) — оркестратор должен выполнить запрос сам и дополнить артефакт (`raw/evidence/{A-Z}/<код>/orchestrator_fallback_<дата>.json`).
```dataview
TABLE searches_failed AS "Failed", fallback_status AS "Fallback"
FROM "wiki/substances"
WHERE contains(fallback_status, "orchestrator") OR contains(fallback_status, "europepmc_unavailable")
```

## 📊 Прогресс
```dataview
TABLE length(rows) AS "Всего"
FROM "wiki/substances"
GROUP BY validation_status
```
