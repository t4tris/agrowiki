# AGENTS.md — Схема вики (правит LLM)

Источник метода: Karpathy "LLM Wiki" (gist 442a6bf555914893e9891c11519de94f).
Три слоя: `raw/` (иммутабельно) → `wiki/` (пишет LLM) → `AGENTS.md` (этот файл).
Три операции: **Ingest**, **Query**, **Lint** (Lint включает валидацию и закрытие пробелов веб-поиском).
Язык вики: **русский**; названия веществ латиницей; библиография англоязычная.

## Цель
По каждому веществу из CSV собрать актуальные научные данные и провалидировать CSV-утверждения.
Фокус литературы: **три культуры — томат, огурец, клубника**. Все 271 вещество в вики, но поиск ограничен этими культурами; нет литературы по культуре → честный статус `no_data`.

## Структура vault
```
f:\agrowiki\
├── AGENTS.md          (этот файл — схема)
├── README.md          (хаб для человека)
├── index.md           (каталог; под-индексы index_*.md через Dataview)
├── log.md             (хронология, append-only)
├── task_queue.md      (очередь задач оркестратора)
├── validation.md      (дашборд валидации, Dataview)
├── _templates/        (шаблоны Templater)
├── raw/               (слой 1: ИСТОЧНИКИ, ИММУТАБЕЛЬНЫ)
│   ├── Complete_Action_Oriented_Agronomic_Substances_CLEANED_v6.csv
│   ├── assets/
│   ├── normalization/synonyms.json   (реестр синонимов, CAS → один код)
│   ├── sources/<код>/                (PDF, веб-клипы статей)
│   └── evidence/{A-Z}/<код>/         (артефакты: search_*.json, facts_*.md, validation_*.md; коды с цифр — в 0-9/)
└── wiki/              (слой 2: вики, пишет LLM)
    ├── substances/    (271 карточка вещества)
    ├── categories/    (8 категорий действий)
    ├── classes/       (~20 семейств хим. классов)
    ├── mechanisms/    (механизмы действия)
    ├── crops/         (3 культуры: Томат, Огурец, Клубника)
    ├── syntheses/     (сравнения и ответы-страницы)
    └── overview.md
```

## Типы страниц и frontmatter

### Карточка вещества (`wiki/substances/<код>.md`, type: substance)
```yaml
---
type: substance
code: IBA
name_en: Indole-3-butyric acid
cas: "133-32-4"
formula: C12H13NO2
class: Auxins
action_category: ROOT_DEVELOPMENT
application_csv: "..."          # как в CSV (исходно)
efficacy_csv: HIGH              # MEDIUM | LOW | HIGH | EMPTY
validation_status: unverified   # unverified | verified | corrected | partial | insufficient_data | conflicting
evidence_level: unverified      # strong | moderate | weak | unverified
last_checked: 2026-08-04
next_review: 2026-11-04
sources: []                     # PMID / DOI / URL
notes: []                       # что исправлено/противоречит CSV (не стирать!)
crops:
  tomato: no_data               # found_verified | found_unverified | no_data
  cucumber: no_data
  strawberry: no_data
aliases: []                     # синонимы из PubChem (CAS-совпадение → объединять страницы)
aliases_ru: []                  # русские синонимы (MeJA → Метилжасмонат, GA3 → Гибберелловая кислота) — для русского поиска и графа
eppo_code: null
regulatory_status: null
consensus_score: null
toxicity_window: {}             # ED50/TD50/therapeutic_index/soil_persistence — только из литературы
phi_mrl: {}                     # PHI_days, MRL_EU/USA/Codex — для HIGH-efficacy обязательно
---
```
Секции карточки:
1. `## Идентичность` — название, CAS, формула, класс (проверено PubChem)
2. `## Механизм действия` — с цитатами
3. `## Применение (CSV)` — исходные данные CSV (дозировки, способ, культуры)
4. `## crop_evidence` — по каждой культуре (🍅 Томат / 🥒 Огурец / 🍓 Клубника): дозировки, эффекты, PMID/DOI, или «нет данных по культуре»
5. `## ⚠️ Corrected Dosages (vs CSV)` — таблица: CSV-значение → исправленное → условия → источник
6. `## ⚠️ Toxicity Window` — ED50/TD50/therapeutic index/стойкость в почве; только из литературы, иначе «нет данных» (не выдумывать!)
7. `## 📅 PHI и MRL` — PHI, MRL EU/USA/Codex (EU Pesticides Database, OpenFoodTox, Codex)
8. `## Противоречия` — CSV vs литература (severity)
9. `## Источники` — список PMID/DOI/URL

### Страница культуры (`wiki/crops/<Культура>.md`, type: crop)
```yaml
---
type: crop
name: Томат
name_latin: Solanum lycopersicum
substances: []   # обратные ссылки
---
```
Секции: `## Вещества по CSV`, `## Валидированные дозировки` (Dataview), `## Синтезы`.

### Категория / Класс / Механизм (type: category | class | mechanism)
Frontmatter: `type`, `name`, `substances: []`, опционально `evidence_level`, `notes`.

### Синтез (`wiki/syntheses/*.md`, type: synthesis)
Frontmatter: `type: synthesis`, `question`, `substances: []`, `crops: []`, `created`, `sources: []`.
Структура: ответ → доказательства с цитатами → противоречия → вывод.

## Нормализация
- **Синонимы веществ:** перед поиском PubChem по `csv_name` → `synonyms` + `iupac_name`; все синонимы в запросы (OR). Реестр: `raw/normalization/synonyms.json`.
- **Русские синонимы:** `aliases_ru` в frontmatter карточки (MeJA → Метилжасмонат, GA3 → Гибберелловая кислота, IBA → Индолилмасляная кислота) — русский поиск по вики работает, граф не ломается.
- **Конверсия единиц:** ppm ≈ mg/L (водные растворы); µM/mM конвертируются через молярную массу из PubChem, конверсия записывается в `dosage_normalized` с источником. Без молярной массы (не найдена) — единицы не сравнивать, пометить в notes.
- **Фенофазы BBCH:** при валидации искать ключи BBCH / growth stage / phenological / anthesis / fruit set / veraison; фаза применения указывается в `conditions.bbch_stages` (BBCH 61 = 10% цветков открыто, BBCH 73 = зелёная ягода).
- **Совпадение CAS** у двух кодов CSV → объединить в одну страницу, коды в `aliases`.
- **Культуры:** Томат = Solanum lycopersicum, Огурец = Cucumis sativus, Клубника = Fragaria × ananassa. Синонимы использовать в fallback-запросах.
- **Единицы:** ppm/mg/L/µM не конвертировать, писать как в источнике + в CSV.
- **Классы:** 89 CSV-классов → ~20 семейств (страницы `wiki/classes/`).

## Контракт отчёта сабагента поиска (JSON v1.3)
Один запуск = одно вещество × 3 культуры. Схема (обязательные поля, enum'ы строгие):

**Правки v1.3 (по итогам пилота 2026-08-04):**
- Сабагент **НЕ пишет файлы** — возвращает JSON в финальном сообщении (может обернуть в ```json или дописать текст после JSON). Артефакт сохраняет **оркестратор** через `_scripts/extract_report.py` (raw_decode на каждой `{`).
- Добавлено поле **`related_evidence`** в `crops.<культура>` — для статуса `no_data`: ближайшие работы по веществу ВНЕ целевой культуры (чтобы «нет данных» было обосновано, а не голословно).
- `contraindications` и `conflicts` — **только массивы объектов**; пусто → `[]`, **запрещены** null-заглушки и строки вместо dict (L1 это проверяет).
- **Europe PMC** часто недоступен в среде сабагента (IPv6-блок) → сабагент помечает в `searches.failed`, а **оркестратор сам выполняет Europe PMC-запрос** в своей среде и дополняет артефакт перед записью карточки.
```json
{
  "contract_version": "1.3",
  "substance": {"code": "IBA", "csv_name": "...", "queried_name": "..."},
  "searches": {
    "performed": ["pubmed_tomato", "pubmed_cucumber", "pubmed_strawberry", "openalex", "pubchem"],
    "failed": [{"endpoint": "europepmc", "reason": "IPv6 blocked", "query": "..."}],
    "queries_used": ["..."],
    "fallback_tries": [{"query": "...", "results": 0}]
  },
  "identity": {"cas": "...", "cid": "...", "formula": "...", "iupac": "...",
               "class_confirmed": true, "class_evidence": ["PMID:..."],
               "synonyms": ["..."], "synonyms_ru": ["..."],
               "molar_mass_g_mol": 346.39, "notes": "..."},
  "mode_of_action": {"summary": "...", "evidence": ["PMID:..."], "confirmed": true},
  "crops": {
    "tomato": {
      "status": "found_verified|found_unverified|no_data",
      "search_stats": {"pubmed": 12, "europe_pmc": 8, "culture_mentioned": 0},
      "claims": [{
        "type": "dosage|effect|method|efficacy",
        "value": "...", "context": "...",
        "dosage_normalized": {"original": "0.5 mM", "ppm_equivalent": 173,
                              "molar_mass_used_g_mol": 346.39,
                              "conversion_source": "PubChem CID 6466",
                              "note": "ppm ≈ mg/L для водных растворов"},
        "conditions": {"photoperiod": "...", "formulation": "...", "ph": "...",
                       "stress": "...", "stage": "...",
                       "bbch_stages": ["BBCH 61", "BBCH 73"],
                       "temperature_range": "18-28°C", "time_of_day": "evening",
                       "light_sensitivity": true, "humidity_min": "60%"},
        "relevance": "directly_supports|directly_contradicts|partially_relevant|irrelevant",
        "evidence_quality": "direct_abstract|title_only|inferred",
        "stats": {"n_studies": 3, "p_value": 0.001, "effect_size": "large"},
        "sources": [{"pmid": "...", "year": 2006, "verified": true,
                     "paper_type": "review|trial|trial_in_vitro|mechanistic|preprint",
                     "doi": "...", "oa_url": null}],
        "quote": "..."
      }],
      "gap": "...",
      "related_evidence": [{"pmid": "...", "year": 2022, "claim": "...", "note": "работа по веществу, но культура не входит в фокус (томат/огурец/клубника)"}]
    },
    "cucumber": {...}, "strawberry": {...}
  },
  "toxicity_window": {"ED50_ppm": null, "TD50_ppm": null, "therapeutic_index": null,
                      "soil_persistence": null, "notes": "только из литературы"},
  "phi_mrl": {"PHI_days": null, "MRL_EU_mg_kg": null, "MRL_USA_mg_kg": null,
              "MRL_Codex_mg_kg": null, "source": "EU Pesticides Database|OpenFoodTox|Codex",
              "required_for": "HIGH-efficacy вещества"},
  "contraindications": [{"condition": "...", "effect": "...", "severity": "high|medium|low", "sources": ["PMID:..."]}],
  "conflicts": [{"csv_field": "...", "csv_value": "...", "literature_summary": "...",
                 "severity": "high|medium|low", "sources": ["PMID:..."]}],
  "verdict": {"evidence_level": "strong|moderate|weak|unverified",
              "status_suggested": "verified|corrected|partial|insufficient_data|conflicting",
              "reason": "..."},
  "sources_index": ["PMID:...", "DOI:..."]
}
```

## Правила честности (жёсткие, не нарушать)
1. `verified: true` — только если аннотация реально прочитана; иначе `title_only` или `inferred`.
2. Нет результатов по культуре → `no_data`. **Запрещено** подставлять данные другой культуры.
3. Никаких выдуманных PMID/DOI/дозировок/цитат. Не извлёк — не пишет.
4. Все неудавшиеся эндпоинты → `searches.failed`.
5. «Нет данных» ≠ «плохо искал»: <5 результатов по культуре → fallback-цепочка: (a) запрос без культуры + проверка упоминания культуры в тексте; (b) синонимы культуры. Всё ещё 0 → `no_data` + `search_stats` + `related_evidence` (ближайшие работы по веществу вне фокусных культур).
6. Противоречия не стираются: CSV-значение сохраняется, конфликт фиксируется в `notes`/`conflicts`.
7. **Единицы:** без молярной массы из PubChem единицы (µM/mM vs ppm) не сравнивать; конверсию записывать в `dosage_normalized` с источником. Токсичность/PHI/MRL — только реальные данные из литературы, иначе null.
8. Лимиты API: PubMed ≤3 запроса/сек, паузы 0.5–1 с, 1 повтор при ошибке, таймауты.
9. **Типы (v1.3):** `conflicts` и `contraindications` — массивы объектов или пустые `[]`. Строки вместо dict, null-заглушки и placeholders **запрещены** — L1 падает на type-check.
10. **Europe PMC:** если у сабагента `searches.failed` содержит europepmc → оркестратор сам выполняет запрос в своей среде и дополняет артефакт.

## Принцип «тонкий агент — толстый артефакт»
- Агент stateless: читает артефакт → одно действие → пишет новый артефакт. Памяти между вызовами нет.
- Артефакт самодостаточен: provenance (кто, когда, из каких источников) внутри файла.
- `raw/evidence/{A-Z}/<код>/search_*.json` — иммутабелен (не редактировать!).
- `raw/evidence/{A-Z}/<код>/facts_*.md` — извлечённые факты.
- `raw/evidence/{A-Z}/<код>/validation_*.md` — отчёт валидации vs CSV.
- Wiki-карточка — обновляемое представление артефактов (история в git).
- Оркестратор (главный агент) — финальный арбитр task_queue.md и log.md.

## Проверка отчётов (4 уровня)
- **L1 Автопроверка (`_scripts/l1_check.py`):** JSON по схеме; **type-check** обязательных полей — `conflicts`/`contraindications` должны быть массивами объектов (не строки, не null); каждый PMID через esummary (существует, заголовок матчит); DOI через Crossref.
- **L2 Перекрёстная:** дубли PMID между культурами допустимы, claims не должны противоречить; противоречия → `conflicts`.
- **L3 Человек:** `conflicting` и критичные исправления → дашборд «требуют внимания» в validation.md, пользователь просматривает.
- **L4 Повторная (Lint):** next_review; новый поиск публикаций по ключевым веществам.

## Процедуры

### Ingest (новые источники)
1. Файл/клип → `raw/sources/<код вещества>/` (иммутабельно, имя: `<дата>_<описание>.pdf|md`)
2. Запись в log.md: `## [дата] ingest | <вещество> | <источник>`
3. Если источник добавляет факты → обновить карточку и `raw/evidence/.../facts_*.md`

### Validation (ядро работы)
Цикл на вещество: поиск по 3 культурам (сабагент) → сабагент возвращает JSON в финальном сообщении → **оркестратор извлекает и сохраняет артефакт** (`_scripts/extract_report.py` → `raw/evidence/{A-Z}/<код>/search_*.json`) → при `searches.failed` с europepmc оркестратор сам дополняет запрос → L1/L2 проверка → карточка + crop_evidence → corrected_dosages → task_queue.md + validation.md + log.md.
Критерий готовности: `validation_status ≠ unverified` И ≥1 источник по любой из трёх культур.
Приоритет: 4 дубликата → HIGH (46) → MEDIUM (146) → LOW (83).

### Query
Вопрос → синтез с цитатами из карточек → ценный ответ → новая страница `wiki/syntheses/` → index.md.

### Lint
- Сироты (нет обратных ссылок), пустые страницы, устаревшие (`next_review` прошёл)
- **Ежемесячный цикл:** новые публикации по ключевым веществам (PubMed, Europe PMC SRC:PPR за последний месяц) → новые VALIDATE-задачи в task_queue.md
- Результат → task_queue.md + log.md

## Форматы служебных файлов

### log.md (append-only)
```
## [2026-08-04] ingest | CSV | 275 строк → raw/
## [2026-08-04] bootstrap | 271 черновик карточек создан
## [2026-08-04] discover | IBA × tomato | 12 статей (PubMed)
## [2026-08-04] validate | IBA | status: corrected | conflicts: 5
```

### task_queue.md
```
## 🔴 HIGH PRIORITY
- [ ] VALIDATE: IBA × tomato → raw/evidence/IBA/
## 🟡 MEDIUM PRIORITY
- [ ] VALIDATE: GA3 × strawberry (конфликт дозировок)
## ✅ COMPLETED
- [x] INGEST: CSV → 271 черновик (2026-08-04)
```
Каждый агент обновляет queue; финальный арбитр — оркестратор.

### index.md
Хаб со ссылками на под-индексы (Dataview): по категориям (index_foliar…), по культурам (index_tomato…), по статусу валидации (index_verified / index_conflicting / index_unverified).

### validation.md
Дашборд: TABLE validation_status, evidence_level, claims по культурам; секции «🔴 Требуют внимания (conflicting)», «✅ Проверено».

## API-эндпоинты (рабочие, без ключей)
- PubMed E-utilities: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=...&retmode=json&retmax=20`
- esummary: `.../esummary.fcgi?db=pubmed&id=...&retmode=json` (проверка PMID)
- Europe PMC: `https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=...&format=json&pageSize=25` (препринты: `AND SRC:PPR`)
- bioRxiv: `https://api.biorxiv.org/details/biorxiv/{дата_с}/{дата_по}/{курсор}`
- PubChem: `https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{name}/property/.../JSON` + `synonyms/JSON` + `xrefs/RegistryID/JSON` (CAS)
- OpenAlex: `https://api.openalex.org/works?search=...&per-page=25`
- Crossref: `https://api.crossref.org/works/{doi}` (проверка DOI)
- Unpaywall: `https://api.unpaywall.org/v2/{doi}?email=...` (нужен реальный email)
- PHI/MRL: EU Pesticides Database (efsa.europa.eu, браузер + Web Clipper), OpenFoodTox (EFSA, датасет), Codex MRLs
- Ключи (опционально, в .secrets/api_keys.env): Semantic Scholar (x-api-key), Consensus (x-api-key), ChemSpider RSC, EPPO token.

## Приоритеты и расписание
1 сессия = пакет 10–20 веществ (5–10 сабагентов параллельно) → карточки → трекер.
Оценка: 80–120 ч ≈ 30–40 сессий по 2–3 ч. HIGH ≈ 3–5 сессий.
