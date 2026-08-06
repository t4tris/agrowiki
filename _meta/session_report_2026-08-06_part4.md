---
type: session_report
session: 2026-08-06 (part 4 — реализация ревью part 3, оценка 7/10)
audience: внешний аудит другой LLM
created: 2026-08-06
commits_span: 0f6c671..HEAD (реализация контракта v1.5)
prev_report: _meta/session_report_2026-08-06_part3.md
review: ревью 2026-08-06 part 3 (в чате, оценка 7/10)
---

# Отчёт сессии 2026-08-06 (part 4) — «Реализация ревью 7/10: контракт v1.5 (source_type), восстановление данных, защита конвейера»

> Репорт для внешнего аудита. Ответ на ревью part 3: 🔴 критический дефект (потеря данных
> Figueiredo 2015) исправлен полностью, 🟡 5 рекомендаций реализованы, 🟢 2 — в очереди.

## 1. Контекст проекта

Агрономическая Obsidian-вики (Karpathy LLM Wiki). CSV 267 веществ, фокус — томат/огурец/клубника.
Контракт отчёта сабагентов: v1.5 (новое), стиль-гайд v2.3, репозиторий `github.com/t4tris/agrowiki`.

## 2. Стартовое состояние (после ревью part 3)

Ревью part 3 (оценка 7/10) выявило: 🔴 потеря данных Figueiredo 2015 (Trinexapac-ethyl) —
системный дефект контракта v1.4 (источники без DOI ~20–25% литературы выпадали); 🟡 хвосты
бутстрапа повторились, служебная обвязка PHI/MRL, невалидный enum `mechanism`, retry-ответы
не пишутся в файлы; 🟢 мусор сабагентов в `_scripts/`, папка extract_report.

## 3. Рекомендации ревью → статус

| # | Рекомендация | Статус | Доказательство |
|---|---|---|---|
| 1 | 🔴 Контракт v1.5: `source_type` enum (openalex/isbn/url_verified/label) + правило честности 15 + L1-проверка новых типов | ✅ выполнено | `AGENTS.md` (контракт v1.5, правило 15), `l1_check.py` v1.5 (OpenAlex API/URL HTTP/ISBN check digit/label manual_read; обратная совместимость с v1.4) |
| 2 | 🔴 Пересмотр карточки Trinexapac: вернуть 2 claim Figueiredo 2015 | ✅ выполнено | `search_Trinexapac-ethyl_2026-08-06_rev2.json` — 2 claim в `claims` с `source_type: openalex`, `verification_method: openalex_api`; карточка — факты в «Научные данные», источник OpenAlex W1790097572; статус `partial` |
| 3 | 🟡 Автоматический writer карточек | ⏳ в техдолге | задача CARD_WRITER (SDD-кандидат) в task_queue; правило 10 + smoke_test остаются страховкой |
| 4 | 🟡 Процесс сохранения retry-ответов | ✅ выполнено | правило 12 дополнено (сохранять `subagent_response_retry.txt` → `search_*_rev2.json` с supersedes; служебный файл в git НЕ включать); `subagent_response_retry.txt` удалён из индекса; задача RETRY_PROCESS в task_queue |
| 5 | 🟢 Убрать `required_for` из контракта | ✅ выполнено | `phi_mrl.required_for` удалён из схемы v1.5 (вместо него `phi_mrl.source` с фактическим источником) |
| 6 | 🟢 Усилить описание enum в промптах | ✅ частично | контракт v1.5: enum `source_type`, `verification_method`, `paper_type` (+conference, regional_journal) — строгие; L1 type-check их проверяет |
| 7 | 🟢 Мусор сабагентов в `_scripts/` | ✅ выполнено | `.gitignore`: `_tmp_*`, `ccc_*`, `*_research.py`, `*_final.py`, `*_batch.py`, `*_verify.py`, `*_abs.py/json`, `*_results.json`, `*_oa_abs.json`, `subagent_response_retry.txt` |
| 8 | 🟢 `extract_report.py` папка | ✅ подтверждено | `os.makedirs(exist_ok=True)` уже есть в скрипте (DirectoryNotFound был при ручном Copy-Item) |
| 9 | 🟡 AUDIT_TAXONOMY-20 до Фазы 4 | ✅ в очереди | task_queue.md (без изменений) |

## 4. Задачи сессии и результаты

### Задача 1. Контракт v1.5 (source_type enum) — AGENTS.md
**Сделано:** правки v1.5 в контракте: `source_type` (`pmid|doi|openalex|isbn|url_verified|label`),
`verification_method` (`esummary|crossref|openalex_api|manual_read`), `paper_type` (+conference,
regional_journal), `phi_mrl.required_for` удалён, процедура retry-сохранения. Правило честности 15:
реальная работа без DOI цитируется при верификации (OpenAlex/ISBN/URL), verified:true и явном
источнике идентификации; потеря фактов из-за отсутствия DOI — ошибка дизайна.

### Задача 2. L1 v1.5 (l1_check.py)
**Сделано:** версии 1.4/1.5 принимаются; source обязан иметь pmid/doi ИЛИ source_type+id;
верификация: openalex → OpenAlex API (title), url_verified → HTTP 200 (HEAD), isbn → контрольная
цифра ISBN-10/13, label → только verified:true + manual_read; type-check verification_method,
paper_type. **Обратная совместимость:** все новые артефакты 2026-08-06 и rev2 проходят L1 v1.5 ✅
(старые пилотные v1.2 имеют известные дефекты — задача MIGRATE).

### Задача 3. Восстановление данных Figueiredo 2015 (Trinexapac-ethyl)
**Сделано:** 2 claim возвращены в `claims` rev2 с `source_type: "openalex"`, `id: OpenAlex:W1790097572`,
`verification_method: openalex_api`, `paper_type: regional_journal`; L1 подтвердил работу через
OpenAlex API («COMPORTAMENTO DE PLANTAS DE TOMATEIRO INDETERMINADO NA PRESENÇA DE REGULADOR DE
CRESCIMENTO», 2015). Карточка: факты в «Научные данные по культурам» (томат), таблица валидации
«контроль междоузлий» → ⚠️ Частично, статус `partial`, crops.tomato `found_verified`, источник
OpenAlex W1790097572 в «Источники».

### Задача 4. Защита конвейера
**Сделано:** `.gitignore` — паттерны временных файлов сабагентов; `subagent_response_retry.txt`
удалён из индекса git (правило 12: служебный, не коммитить); task_queue: CARD_WRITER (SDD-кандидат),
RETRY_PROCESS, MIGRATE v1.2→v1.5.

## 5. Итоговое состояние

| Метрика | Было (part 3) | Стало (part 4) |
|---|---|---|
| Контракт | v1.4 | **v1.5** (source_type enum) |
| Правила честности | 14 | **15** (источники без DOI) |
| L1 | v1.4 (pmid/doi только) | **v1.5** (openalex/url/isbn/label + обратная совместимость) |
| Trinexapac-ethyl | insufficient_data, данные потеряны | **partial**, 2 claim восстановлены (source_type=openalex) |
| phi_mrl.required_for | в схеме | **удалён** |
| retry-файлы | закоммичен `subagent_response_retry.txt` | **в gitignore**, из индекса убран |
| .gitignore | базовые паттерны | **+ временные файлы сабагентов** |
| Дерево git | — | **чистое** |

## 6. Коммиты сессии

```
0f6c671 fix: Trinexapac-ethyl — восстановлены полезные данные Figueiredo 2015; insufficient_data → partial, rev2 дополнен
(далее коммит реализации ревью part 4)
```

## 7. Замечания для аудитора (что проверять / открытые вопросы)

1. **L1 v1.5 на старых пилотных артефактах v1.2** (2026-08-04): Artemisinin (no_data без
   related_evidence), Chitosan/GA3 (severity «moderate»/None), IBA/Triacontanol (элементы-строки
   в contraindications) — **известные дефекты пилота**, НЕ регрессия от v1.5. Ожидают миграции
   (задача MIGRATE v1.2→v1.5 при Lint 2026-09-04). Вопрос: мигрировать артефакты или
   пере-валидировать?
2. **CARD_WRITER (автоматический writer карточек)** — SDD-кандидат: скрипт, перезаписывающий
   файл целиком из отчёта v1.5. Пока правило 10 + smoke_test — единственная защита от хвостов.
3. **`subagent_response_retry.txt`** — файл остался на диске (в .gitignore), но из git удалён.
   Контент retry-ответа (полный JSON v1.4) в нём — полезен для истории, не для git.
4. **OpenAlex-верификация в L1** — зависимость от api.openalex.org (без ключа, лимиты ~10 req/s).
   При недоступности API → L1 ошибка, нужен повтор.
5. **`source_type: label`** — самое слабое (название без ID). Допустимо только manual_read;
   риск злоупотребления — L1 проверяет verified:true, но не качество.
6. **Контракт v1.5 в промптах сабагентов** — нужно обновить шаблон промпта (enum'ы source_type/
   verification_method), чтобы сабагенты сразу генерировали v1.5. В следующих пакетах.
7. **21/265 валидировано (7.9%)**, HIGH 28. Темп ~10/сессия устойчив.

## 8. Следующие шаги

1. **Пакет HIGH (10–12 веществ) на контракте v1.5**: 1-MCP, 4-CPA, BNOA, Carbendazim, Cyanamide,
   DA-6, DMSO, Ethylene, Fulvic Acid, GA1, GA4, Leonardite.
2. **CARD_WRITER** — SDD-спека и реализация.
3. **AUDIT_TAXONOMY-20** до Фазы 4; **MIGRATE** пилотных артефактов при Lint.
4. **PHI_REI / PAPERS_TO_FETCH** — ручной сбор этикеток пользователем.
