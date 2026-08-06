---
type: handoff
created: 2026-08-06
from_session: "Стиль-гайд v2.3 + реализация ревью 6.5/10 → подготовка к Фазе 3"
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
| `_meta/session_report_2026-08-06_part2.md` | **Отчёт для внешнего аудита** (реализация ревью 6.5/10: коммит, STYLE_MIGRATE, smoke_test, bootstrap-защита, EOL) |
| `_meta/session_report_2026-08-06_part3.md` | **Отчёт для внешнего аудита** (Фаза 3: валидация 10 HIGH-веществ, фикс хвостов бутстрапа, PHI/REI — не блокер, 4 коммита) |
| `_meta/session_report_2026-08-06_part4.md` | **Отчёт для внешнего аудита** (реализация ревью 7/10: контракт v1.5 source_type, восстановление Figueiredo 2015, защита конвейера) |
| `_meta/session_report_2026-08-06_part5.md` | **Отчёт для внешнего аудита** (реализация ревью 8/10: промпт v1.5, OpenAlex backoff, label ≤20%) |
| `_meta/subagent_prompt_v1.5.md` | **Шаблон промпта research-сабагента (контракт v1.5)** — использовать для запуска сабагентов |
| `_meta/sdd_openspec_context.md` | Контекст для SDD-переосмысления (OpenSpec-брейншторм, актуализирован 2026-08-06) |
| `_meta/handoff.md` | **Этот файл** — состояние и следующие шаги |
| `AGENTS.md` | Схема вики, контракт отчёта **v1.5** (source_type enum), правила честности 1–15, L1–L4 |
| `README.md` | **Человекочитаемый хаб проекта** (этот README) |
| `task_queue.md` | Очередь VALIDATE (HIGH 28 / MEDIUM 133 / LOW 83) + TECHNICAL DEBT (6 задач) + RETRY LOG |
| `validation.md` | Трекер валидации для LLM (Dataview не рендерится — дашборд в `Vault/index.md`) |
| `log.md` | Хронология (append-only) |
| `raw/sources/papers_to_fetch.md` | **Очередь статей на скачивание человеком** (Proline ×3, PBZ-этикетки ×2) |
| `_scripts/extract_report.py` | Извлечение JSON из ответа сабагента; **авто-retry** (до 3 файлов), exit 2 = RETRY_NEEDED, RETRY-лог в task_queue |
| `_scripts/l1_check.py` | L1: схема **v1.4** + type-check + `taxonomy_check` + `supersedes` + PMID esummary + DOI Crossref |
| `_scripts/fallback_europepmc.py` | Europe PMC fallback оркестратора (SRC:PPR) → `orchestrator_fallback_*.json` |
| `_scripts/gen_taxonomy.py` | Таксономия (9 категорий + 29 семейств + 15 механизмов); `--refresh` для пересчёта |
| `_scripts/gen_synonyms.py` | `raw/normalization/synonyms.json` из aliases карточек (267 веществ) |
| `_scripts/bootstrap.py` | Черновики из CSV (**по умолчанию — только карточки**; `--full` перезаписывает служебные файлы!; `--dry-run` для проверки; автозапуск gen_taxonomy) |
| `_scripts/smoke_test.py` | Целостность после массовых операций (exit 0 = ок): дубли, запрещённые поля, старые секции/баннеры, таксономия |
| `.gitattributes` | EOL-политика: md/json/csv — CRLF, py — LF |
| `raw/evidence/{A,C,G,I,M,P,S,T}/…/search_*.json` | 12 артефактов (5 пилот v1.2 + 5 v1.4 + fallback'и) |
| `Vault/wiki/substances/*.md` | **11 валидированных карточек** (все на стиль-гайде v2.3) + 254 черновика (265 страниц; MeJA→Methyl Jasmonate, TRIA→Triacontanol) |

---

## 🟢 Статус проекта (на 2026-08-06, конец дня)

**Конвейер работает и прошёл 5 циклов внешнего аудита** (ревью 2026-08-06 part 4, оценка 8/10 —
реализовано: контракт v1.5, промпт v1.5 проверен в бою на DA-6). Контракт — **v1.5**
(source_type: pmid|doi|openalex|isbn|url_verified|label); стиль-гайд карточек **v2.3** «конечные
факты»; все 22 валидированные карточки на новой схеме (эталон — IBA.md). Валидировано
**11 новых HIGH-веществ** (11 → 22), добавлены 2 rev2-артефакта, расширен smoke_test (правило 10),
правило 14 — PHI/REI не блокер, правило 15 — источники без DOI.

### Валидировано: 22 / 265 страниц (267 кодов CSV — 2 пары объединены: MeJA→Methyl Jasmonate, TRIA→Triacontanol)

| Вещество | Статус | Evidence | Ключевой вывод |
|---|---|---|---|
| GA3 | partial | moderate | Механизм усов подтверждён; дозировки CSV не верифицированы; +PPR 1188729 |
| IBA | corrected | moderate | CSV 100–1000 ppm на 2–3 порядка выше литературы |
| Triacontanol (+TRIA) | partial | moderate | CSV 0.05–0.2 ppm ниже рабочих 0.5–1 ppm |
| Artemisinin | insufficient_data | weak | Обе CSV-заявки не подтверждены |
| Chitosan | partial | strong | Механизм подтверждён 21 аннотацией; CSV-протоколы нет |
| Chitooligosaccharides | partial | strong | COS/CHOS: 50 мг/л при холоде огурца; защита от мучнистой росы томата |
| **Paclobutrazol** | partial | strong | Дозы 25–200 мг/л (CSV 75–300 не верифицированы); **MRL EU 0.01\* LOD получен** |
| **Methyl Jasmonate** | corrected | strong | Эффективные 5.6–112 ppm; ⚠️ антракноз клубники; летучесть |
| **Glycine Betaine** | partial | moderate | 117–586 ppm подтверждены; засуха «все культуры» слабо |
| **Proline** | partial | moderate | Фолиарно клубника +23–32%; **seed priming = insufficient_data** (очередь скачивания) |
| **Silicon** | corrected | strong | Дозы 30–75 мг Si/л; taxonomy: mechanism → antioxidant_defense |
| **Kinetin** | partial | moderate | Анти-сенесцентное действие подтверждено; CSV 10–50 ppm не подтверждена напрямую |
| **6-BAP** | partial | strong | Доза 100 ppm подтверждена для томата (+108.4% урожайности); цвет плодов не затрагивает |
| **Thidiazuron** | verified | strong | Фолиарный TDZ 50 мг/л ×3 — рост пазушных почек клубники; томат/огурец no_data |
| **PIX** | partial | moderate | Контроль столонов клубники; **taxonomy → synthetic_growth_regulators** |
| **Uniconazole** | corrected | moderate | Дозы 2.5–10 мг/л (томат), 10–20 ppm (клубника); **taxonomy → synthetic_growth_regulators** |
| **Ethephon** | corrected | strong | 100 ppm ускоряет созревание томата; 7 mmol/L≈1011 ppm не подтверждён |
| **S-ABA** | verified | moderate | Стресс-толерантность; созревание клубники (не-климактерический плод) |
| **Zeatin** | partial | moderate | Эндогенный транс-зеатин в цветках/плодах; CSV 5–25 ppm не подтверждена |
| **Trinexapac-ethyl** | insufficient_data | weak | Механизм GA-ингибитор подтверждён; по фокусным культурам нет верифицируемых PMID/DOI |
| **Chlormequat Chloride** | partial | moderate | Контроль высоты рассады; CSV 250–500 ppm и ускорение созревания не подтверждены |
| **DA-6** | partial | moderate | 10–30 ppm эффективны на томате/клубнике (стресс); 40–50 ppm ингибируют; огурец no_data; **первый артефакт v1.5 с source_type=openalex** |

### Инфраструктура (сделано к 2026-08-06)
- Стиль-гайд v2.3 «конечные факты»: таблица «Валидация CSV-заявок», «Научные данные по культурам»,
  frontmatter −7 полей-зеркал; все 11 валидированных карточек мигрированы (STYLE_MIGRATE ✅)
- Таксономия: 9 категорий (+SHELF_LIFE) + 29 семейств (7 пестицидных, acaricides) + 15 механизмов
- `smoke_test.py` (целостность), `bootstrap.py --dry-run` + автозапуск gen_taxonomy, `.gitattributes` (EOL)
- `synonyms.json` (265 веществ), авто-retry в extract_report, L1 v1.4, fallback Europe PMC
- Дубликаты (8) разрешены; PHI/REI — правило 14; **MRL Paclobutrazol собран** (EU 0.01\* LOD, Codex нет)
- Навык `.github/copilot-skills/session-audit-report/` + 4 цикла аудита (репорты в `_meta/`)
- SDD-контекст для OpenSpec-переосмысления (`_meta/sdd_openspec_context.md`); Vault/raw/ — gitignored

---

## 🎯 Следующие шаги (Фаза 3)

### 0. Перед стартом — закрыто в этой сессии (part 3)
- ✅ Валидировано 10 новых HIGH-веществ: Kinetin, 6-BAP, Thidiazuron, PIX, Uniconazole, Ethephon, S-ABA, Zeatin, Trinexapac-ethyl, Chlormequat Chloride (11 → 21)
- ✅ Smoke_test расширен (правило 10: комментарии-заглушки, дубли секций, служебная обвязка PHI/MRL)
- ✅ Правило 14: PHI/REI — не блокер (AGENTS.md, README, task_queue)
- ✅ 2 rev2-артефакта (Uniconazole, Trinexapac-ethyl) с `supersedes`, L1 пройден
- ✅ Хвосты бутстрапа удалены из всех валидированных карточек

### 1. Полный цикл валидации
Порядок приоритетов (в `task_queue.md`): **HIGH (28)** → MEDIUM (133) → LOW (83).

**Рабочий цикл на вещество** (пакетами по 10–20 за сессию):
1. Запустить research-сабагент (stateless; промпт **по шаблону `_meta/subagent_prompt_v1.5.md`**: CSV-строка + текущая таксономия карточки + контракт **v1.5**).
2. Извлечь JSON: `python _scripts/extract_report.py <ответ1.txt> <dst.json> [<ответ2.txt>] [<ответ3.txt>]` — **проверять `$LASTEXITCODE`**: 0 = ок, 2 = RETRY_NEEDED (повторный запуск сабагента, до 2 попыток; после 2 неудач → `insufficient_data`).
3. L1: `python _scripts/l1_check.py raw/evidence/{A-Z}/<код>/search_*.json` (требует v1.4).
4. При `searches.failed` europepmc → `python _scripts/fallback_europepmc.py <код> "<имя>" "<запросы>"`.
5. Применить `taxonomy_check.corrections` (если есть) → карточка + `gen_taxonomy.py --refresh` при изменении маппинга.
6. Написать карточку **строго по стиль-гайду v2.3** (AGENTS.md): frontmatter (18 полей) + «Валидация CSV-заявок» (одна заявка = одна строка) + «Научные данные по культурам» (методы применения) + toxicity + 📅 PHI/REI/MRL + ограничения + источники. Без баннеров, процесса поиска, дублей. **ВАЖНО: файл перезаписывать ЦЕЛИКОМ** (правило 10) — НЕ только верхнюю часть через replace_string, иначе в конце остаются секции-заглушки черновика (повторялось 2 раза в этой сессии!).
7. Обновить `task_queue.md` ([x] + RETRY-строки), `validation.md` + проверить `Vault/index.md`, `log.md`, обновить `synonyms.json` (`gen_synonyms.py`).
8. `python _scripts/smoke_test.py` (exit 0 = ок) → коммит + push.

### 2. Рекомендуемый следующий пакет (HIGH, остаток 28)
**1-MCP, 4-CPA, BNOA, Carbendazim, Cyanamide, DA-6, DMSO, Ethylene, Fulvic Acid, GA1, GA4, Leonardite, MCPA, Magnesium, Maleic Hydrazide, NAD, NHP, PDJ, Phosphite, Polyaspartic, Polyglutamic, Propiconazole, Pyraclostrobin, STS, Tebuconazole, Thiabendazole, Thiophanate, Trifloxystrobin.** Для пестицидов/ретардантов (Carbendazim, Propiconazole, Tebuconazole, Thiabendazole, Thiophanate, Trifloxystrobin) — PHI/REI справочно (не блокер), MRL — из этикеток.

### 3. Технический долг (TECHNICAL DEBT в task_queue.md)
- **PAPERS_TO_FETCH**: пользователь скачивает статьи/этикетки (Proline ×3, PBZ ×2) → анализ → карточки
- **PHI_REI**: Uniconazole, PIX, Chlormequat (этикетки)
- **AUDIT_TAXONOMY-20**: отдельный батч taxonomy_check **до Фазы 4** (синтезы)
- **MIGRATE v1.2→v1.4**: при Lint-перепроверке пилотных карточек (2026-09-04)
- **SDD-сессия**: брейншторм OpenSpec по `_meta/sdd_openspec_context.md` (отложено до Фазы 5)
- **Усилить конвейер** (из репорта part 3): автоматический writer карточек (правило 10), фильтр `required_for` из отчётов, сохранение retry-ответов, унификация папок evidence для кодов с цифрами

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
- **НЕ запускать `bootstrap.py` для проверки синтаксиса/«посмотреть»** — он перезаписывает unverified-черновики (регрессия 2026-08-06). Проверка: `--dry-run` или `py_compile`; после генерации — `smoke_test.py`.
- **EOL:** `.gitattributes` (md CRLF / py LF); после правок — нормализация + `git add --renormalize .`; файлы писать через Python с явной кодировкой, НЕ через Add-Content (ANSI).

---

## 🚫 Чего не делать
- Не перезаписывать иммутабельные `raw/evidence/*/search_*.json` (ошибка схемы → rev2 с `supersedes` + L1!).
- Не выдумывать PMID/DOI/дозировки; `verified: true` только при реально прочитанной аннотации.
- Не подставлять данные другой культуры при `no_data`.
- Не оставлять null-заглушки в `contraindications`/`conflicts` — пустой массив `[]`.
- **Не выдумывать waiting periods (PHI/REI)** — не найдено → `unknown` (правило 14).
- Не запускать `bootstrap.py --full` без необходимости (перезаписывает ручные правки); для проверки — `--dry-run`.
- Не писать карточки по старой схеме (баннеры, «Применение (CSV)», Corrected Dosages, Противоречия, crop_evidence, found_verified в заголовках) — только стиль-гайд v2.3; `smoke_test.py` это проверяет.
