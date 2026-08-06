---
type: handoff
created: 2026-08-04
from_session: "Пилот валидации → подготовка к Фазе 3"
contract_version: 1.4
---

# Handoff следующей сессии

> Этот файл — мостик между сессиями. Прочитай его первым, затем `_meta/plan.md` (мастер-план) и `AGENTS.md` (схема). Всё остальное — в `task_queue.md`, `validation.md`, `log.md`.

## Где что лежит

> Пути — от корня проекта `f:\agrowiki` (после реструктуризации 2026-08-04 служебный слой ВНЕ vault).

| Файл | Назначение |
|---|---|
| `_meta/plan.md` | Мастер-план (фазы 0–5) + секция «Результаты пилота» |
| `_meta/session_report_2026-08-04.md` | **Отчёт для внешнего аудита** (часть 1: инфраструктура, 10 коммитов) |
| `_meta/session_report_2026-08-04_part2.md` | **Отчёт для внешнего аудита** (часть 2: ревью + пилот Фазы 3, 5 коммитов) |
| `_meta/session_report_2026-08-04_part3.md` | **Отчёт для внешнего аудита** (часть 3: ревью part 2, 1 коммит) |
| `_meta/session_report_2026-08-06.md` | **Отчёт для внешнего аудита** (2026-08-06: анализ, merge, таксономия 7 семейств, SDD-контекст, стиль-гайд v2 — 4 коммита + незакоммиченная работа) |
| `_meta/handoff.md` | **Этот файл** — состояние и следующие шаги |
| `AGENTS.md` | Схема вики, контракт отчёта **v1.4**, правила честности 1–14, L1–L4 |
| `README.md` | **Человекочитаемый хаб проекта** (этот README) |
| `task_queue.md` | Очередь VALIDATE (HIGH 38 / MEDIUM 133 / LOW 83) + TECHNICAL DEBT (6 задач) + RETRY LOG |
| `validation.md` | Трекер валидации для LLM (Dataview не рендерится — дашборд в `Vault/index.md`) |
| `log.md` | Хронология (append-only) |
| `raw/sources/papers_to_fetch.md` | **Очередь статей на скачивание человеком** (Proline ×3, PBZ-этикетки ×2) |
| `_scripts/extract_report.py` | Извлечение JSON из ответа сабагента; **авто-retry** (до 3 файлов), exit 2 = RETRY_NEEDED, RETRY-лог в task_queue |
| `_scripts/l1_check.py` | L1: схема **v1.4** + type-check + `taxonomy_check` + `supersedes` + PMID esummary + DOI Crossref |
| `_scripts/fallback_europepmc.py` | Europe PMC fallback оркестратора (SRC:PPR) → `orchestrator_fallback_*.json` |
| `_scripts/gen_taxonomy.py` | Таксономия (8 категорий + 29 семейств + 15 механизмов); `--refresh` для пересчёта |
| `_scripts/gen_synonyms.py` | `raw/normalization/synonyms.json` из aliases карточек (267 веществ) |
| `_scripts/bootstrap.py` | Черновики из CSV (**по умолчанию — только карточки**; `--full` перезаписывает служебные файлы!) |
| `raw/evidence/{A,C,G,I,M,P,S,T}/…/search_*.json` | 12 артефактов (5 пилот v1.2 + 5 v1.4 + fallback'и) |
| `Vault/wiki/substances/*.md` | **11 валидированных карточек** + 254 черновика (265 страниц; MeJA→Methyl Jasmonate, TRIA→Triacontanol) |

---

## 🟢 Статус проекта (на 2026-08-04, конец дня)

**Конвейер работает и прошёл 3 цикла внешнего аудита** (все рекомендации выполнены).
Контракт — **v1.4** (включая `taxonomy_check`, `supersedes`, авто-retry, PHI/REI-правило 14).

### Валидировано: 11 / 265 страниц (267 кодов CSV — 2 пары объединены: MeJA→Methyl Jasmonate, TRIA→Triacontanol)

| Вещество | Статус | Evidence | Ключевой вывод |
|---|---|---|---|
| GA3 | partial | moderate | Механизм усов подтверждён; дозировки CSV не верифицированы; +PPR 1188729 (fallback) |
| IBA | corrected | moderate | CSV 100–1000 ppm на 2–3 порядка выше литературы |
| Triacontanol (+TRIA) | partial | moderate | CSV 0.05–0.2 ppm ниже рабочих 0.5–1 ppm |
| Artemisinin | insufficient_data | weak | Обе CSV-заявки не подтверждены |
| Chitosan (+COS/CHOS) | partial | strong | Механизм подтверждён 21 аннотацией; CSV-протоколы нет |
| **Paclobutrazol** | partial | strong | Дозы 25–200 мг/л (CSV 75–300 не верифицированы); **MRL EU 0.01\* LOD получен**; taxonomy correction |
| **Methyl Jasmonate** | corrected | strong | Эффективные 5.6–112 ppm; ⚠️ антракноз клубники; летучесть |
| **Glycine Betaine** | partial | moderate | 117–586 ppm подтверждены; засуха «все культуры» слабо |
| **Proline** | partial | moderate | Фолиарно клубника +23–32%; **seed priming = insufficient_data** (очередь скачивания) |
| **Silicon** | corrected | strong | Дозы 30–75 мг Si/л; taxonomy: mechanism → antioxidant_defense |

### Инфраструктура (сделано за сессию)
- Реструктуризация: служебный слой вне vault; GitHub remote (`main`)
- Таксономия: 8 категорий + 29 семейств + 15 механизмов (267 карточек с `class_family`/`mechanism`)
- `synonyms.json` (267 веществ), авто-retry в extract_report, L1 v1.4, fallback Europe PMC (4 вещества)
- Дубликаты (8) разрешены; заявки CSV — в таблице «Валидация CSV-заявок» (поле `application_csv` удалено в схеме v2.2)
- PHI/REI — практический блокер (правило 14); **MRL Paclobutrazol собран** (EU 0.01\* LOD, Codex нет)
- Навык `.github/copilot-skills/session-audit-report/` — репорты для аудита по стандарту

---

## 🎯 Следующие шаги (Фаза 3)

### 0. Перед стартом — НЕ нужно (закрыто в этой сессии)
- ✅ Europe PMC fallback для GA3/Triacontanol/Chitosan/Silicon — выполнен (orchestrator_fallback)
- ✅ Дубликаты (8) — разрешены; ✅ заявки CSV — в таблице валидации (v2.2)
- ✅ PHI/MRL Paclobutrazol — собран (EU 0.01\* LOD); PHI/REI — очередь на этикетки (papers_to_fetch)

### 1. Полный цикл валидации
Порядок приоритетов (в `task_queue.md`): **HIGH (38)** → MEDIUM (133) → LOW (83).

**Рабочий цикл на вещество** (пакетами по 10–20 за сессию):
1. Запустить research-сабагент (stateless; промпт: CSV-строка + текущая таксономия карточки + контракт **v1.4**).
2. Извлечь JSON: `python _scripts/extract_report.py <ответ1.txt> <dst.json> [<ответ2.txt>] [<ответ3.txt>]` — **проверять `$LASTEXITCODE`**: 0 = ок, 2 = RETRY_NEEDED (повторный запуск сабагента, до 2 попыток; после 2 неудач → `insufficient_data`).
3. L1: `python _scripts/l1_check.py raw/evidence/{A-Z}/<код>/search_*.json` (требует v1.4).
4. При `searches.failed` europepmc → `python _scripts/fallback_europepmc.py <код> "<имя>" "<запросы>"`.
5. Применить `taxonomy_check.corrections` (если есть) → карточка + `gen_taxonomy.py --refresh` при изменении маппинга.
6. Написать карточку (frontmatter + «Валидация CSV-заявок» + «Научные данные по культурам» + toxicity + 📅 PHI/REI/MRL + ограничения + источники).
7. Обновить `task_queue.md` ([x] + RETRY-строки), `validation.md` + проверить `Vault/index.md`, `log.md`, обновить `synonyms.json` (`gen_synonyms.py`).
8. Коммит + push.

### 2. Рекомендуемый следующий пакет (10 веществ, все HIGH)
**Kinetin, 6-BAP, Thidiazuron, PIX, Uniconazole, Ethephon, S-ABA, Trinexapac-ethyl, Chlormequat Chloride, Zeatin** — цитокинины/ретарданты, пересечения с GA3/Paclobutrazol. Для PIX/Uniconazole — PHI/REI (этикетки, см. papers_to_fetch.md).

### 3. Технический долг (TECHNICAL DEBT в task_queue.md)
- **PAPERS_TO_FETCH**: пользователь скачивает статьи/этикетки (Proline ×3, PBZ ×2) → анализ → карточки
- **PHI_REI**: Uniconazole, PIX (этикетки)
- **AUDIT_TAXONOMY-20**: отдельный батч taxonomy_check **до Фазы 4** (синтезы)
- **MIGRATE v1.2→v1.4**: при Lint-перепроверке пилотных карточек (2026-09-04)

---

## 🔑 Ключи API (опционально, пользователь регистрирует)
- **Semantic Scholar** — бесплатный ключ → заголовок `x-api-key` (по IP Forbidden, нужен ключ/VPN).
- **Consensus API** — `api.consensus.app/v1/quick_search`, `x-api-key` → Scientific Consensus Score.
- **ChemSpider (RSC)** — `api.rsc.org/compounds/v1`, бесплатный ключ.
- **EPPO Data Services** — `data.eppo.int` (токен) → регуляторный статус, коды EPPO.
- **AGRICOLA/PubAg** — переехал на Primo (JS), API 403 → только браузер + Web Clipper.
- **Elicit API** — не отвечает с этого IP; браузерный интерфейс может бить CSV-пакеты вручную.

---

## ⚙️ Технические заметки
- Windows PowerShell, без `&&`/`||`. Консоль cp1252 → `$env:PYTHONIOENCODING='utf-8'` перед Python-выводом кириллицы (mojibake косметический; файлы пишутся с `encoding='utf-8'` корректно).
- PubMed ≤3 req/сек без ключа (паузы 0.5–1 с, 1 повтор при ошибке). esummary батчи по 50.
- **Europe PMC заблокирован (IPv6) в среде сабагентов** — выполнять оркестратором (`fallback_europepmc.py`).
- **`fetch_webpage` Copilot может быть недоступен (NotAuthorized)** — Python/urllib; для JS-приложений (EUPD, Codex, нац. реестры) — **Playwright MCP** (navigate → run_code → `page.evaluate`); снапшоты пишутся в `.playwright-mcp/` (в .gitignore).
- CSV: BOM → `utf-8-sig`; 8 кодов дублируются (объединены); 275 строк/267 кодов.
- Не использовать Sci-Hub (нарушение авторских прав) — только Unpaywall/PMC/DOAJ/OA/Web Clipper.
- Параллельность: 5–10 сабагентов за раз; **2 из 5 могут вернуть пустой ответ** → авто-retry в `extract_report.py` (exit 2).
- `bootstrap.py` без флагов = только карточки; `--full` перезаписывает index/task_queue/validation/log/README (требует подтверждения).

---

## 🚫 Чего не делать
- Не перезаписывать иммутабельные `raw/evidence/*/search_*.json` (ошибка схемы → rev2 с `supersedes` + L1!).
- Не выдумывать PMID/DOI/дозировки; `verified: true` только при реально прочитанной аннотации.
- Не подставлять данные другой культуры при `no_data`.
- Не оставлять null-заглушки в `contraindications`/`conflicts` — пустой массив `[]`.
- **Не выдумывать waiting periods (PHI/REI)** — не найдено → `unknown` (правило 14).
- Не запускать `bootstrap.py --full` без необходимости (перезаписывает ручные правки).
