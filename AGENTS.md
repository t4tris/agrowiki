# AGENTS.md — Схема вики (правит LLM)

Источник метода: Karpathy "LLM Wiki" (gist 442a6bf555914893e9891c11519de94f).
Три слоя: `raw/` (иммутабельно) → `wiki/` (пишет LLM) → `AGENTS.md` (этот файл).
Три операции: **Ingest**, **Query**, **Lint** (Lint включает валидацию и закрытие пробелов веб-поиском).
Язык вики: **русский**; названия веществ латиницей; библиография англоязычная.

## Цель
По каждому веществу из CSV собрать актуальные научные данные и провалидировать CSV-утверждения.
Фокус литературы: **три культуры — томат, огурец, клубника**. Все 271 вещество в вики, но поиск ограничен этими культурами; нет литературы по культуре → честный статус `no_data`.

## Структура проекта
```
f:\agrowiki\           ← КОРЕНЬ ПРОЕКТА (git repo, НЕ часть Obsidian)
├── AGENTS.md          (этот файл — схема для LLM, ВНЕ vault)
├── log.md             (хронология, append-only, ВНЕ vault)
├── task_queue.md      (очередь задач оркестратора, ВНЕ vault)
├── validation.md      (трекер валидации для LLM; Dataview в нём не рендерится — дашборд живёт в Vault/index.md)
├── _meta/             (plan.md, handoff.md — служебные документы)
├── _scripts/          (bootstrap.py, extract_report.py, l1_check.py, digest.py)
├── .secrets/          (API-ключи, в git НЕ попадает)
├── raw/               (слой 1: ИСТОЧНИКИ, ИММУТАБЕЛЬНЫ, ВНЕ vault)
│   ├── Complete_Action_Oriented_Agronomic_Substances_CLEANED_v6.csv
│   ├── assets/
│   ├── normalization/synonyms.json   (реестр синонимов, CAS → один код)
│   ├── sources/<код>/                (PDF, веб-клипы статей)
│   └── evidence/{A-Z}/<код>/         (артефакты: search_*.json, facts_*.md, validation_*.md; коды с цифр — в 0-9/)
└── Vault/             ← OBSIDIAN VAULT (только контент вики!)
    ├── .obsidian/     (настройки Obsidian, плагины)
    ├── index.md       (каталог + дашборд статусов, Dataview)
    ├── README.md      (хаб для человека)
    ├── _templates/    (шаблоны Templater)
    ├── raw/           (рабочая папка пользователя: черновики будущих sources, вне конвейера, в .gitignore)
    └── wiki/          (слой 2: вики, пишет LLM)
        ├── substances/    (271 карточка вещества)
        ├── categories/    (9 категорий действий)
        ├── classes/       (29 семейств хим. классов)
        ├── mechanisms/    (механизмы действия)
        ├── crops/         (3 культуры: Томат, Огурец, Клубника)
        ├── syntheses/     (сравнения и ответы-страницы)
        └── overview.md
```

## Правила ссылок (после выноса служебного слоя из vault)
- **Внутри vault:** только вики-ссылки `[[...]]` (страницы, wiki/подпапки). Dataview `FROM "wiki/..."` — относительно корня vault.
- **На файлы ВНЕ vault** (`AGENTS.md`, `log.md`, `task_queue.md`, `validation.md`, `raw/`, `_meta/`, `_scripts/`) — **обычные markdown-ссылки с относительными путями**, напр. `[AGENTS.md](../AGENTS.md)`, `[search_IBA_2026-08-04.json](../../../raw/evidence/I/IBA/search_IBA_2026-08-04.json)` (из `wiki/substances/`). Obsidian не резолвит `[[...]]` за пределы vault — такие ссылки будут «мёртвыми».
- Служебные файлы в корне (log.md, task_queue.md и т.д.) могут ссылаться на vault-страницы **только текстом/путями** (например, `Vault/wiki/substances/IBA.md` или `[[wiki/substances/IBA]]` для человека-читателя) — Obsidian их не отрендерит, это нормально.

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
class_family: auxins              # семейство хим. класса (страница wiki/classes/<slug>.md)
mechanism: auxin_signaling        # механизм действия (страница wiki/mechanisms/<slug>.md)
action_category: ROOT_DEVELOPMENT # категория из CSV (Dataview категорийных страниц); фактические методы применения — в «Научных данных по культурам»
efficacy_csv: HIGH              # MEDIUM | LOW | HIGH | EMPTY (из CSV; Dataview дашбордов)
validation_status: unverified   # unverified | verified | corrected | partial | insufficient_data | conflicting
evidence_level: unverified      # strong | moderate | weak | unverified
last_checked: 2026-08-04
next_review: 2026-11-04
notes: []                     # только не-табличные факты (объединение кодов, миграции); вердикты и эффекты — в секциях, не дублировать
crops:
  tomato: no_data               # found_verified | found_unverified | no_data
  cucumber: no_data
  strawberry: no_data
aliases: []                     # синонимы из PubChem (CAS-совпадение → объединять страницы)
aliases_ru: []                  # русские синонимы (MeJA → Метилжасмонат, GA3 → Гибберелловая кислота) — для русского поиска и графа
fallback_status: null           # orchestrator | europepmc_unavailable | null (после Europe PMC fallback; дашборд в validation.md)
---
```
Секции карточки:
1. `## Идентичность` — название, CAS, формула, класс (проверено PubChem)
2. `## Механизм действия` — с цитатами
3. `## ⚠️ Валидация CSV-заявок` — ЕДИНСТВЕННОЕ место сопоставления CSV↔литература. Таблица:
   `| CSV-заявка | Вердикт | Уточнение | Условия | Severity | Источники |`
   Вердикты: ✅ подтверждена · ⚠️ частично · ❌ не подтверждена · ⚪ нет данных.
   Одна строка = одна CSV-заявка (доза/способ/ожидаемый эффект).
   Исходные CSV-значения — в колонке «CSV-заявка» таблицы; в frontmatter остаются только
   `action_category` и `efficacy_csv` (нужны Dataview-дашбордам).
   Заменяет прежние секции `Применение (CSV)`, `Corrected Dosages` и `Противоречия`.
4. `## Научные данные по культурам` (бывш. crop_evidence) — по каждой культуре
   (🍅 Томат / 🥒 Огурец / 🍓 Клубника): только факты литературы с указанием МЕТОДА применения
   (in vitro, полевой опыт, черенкование, биотест…), дозировок, эффектов, PMID/DOI;
   нет данных → «Нет данных о …» (без описания процесса поиска); отсылки к CSV-заявкам
   запрещены — их вердикты в таблице п.3
5. `## ⚠️ Toxicity Window` — ED50/TD50/therapeutic index/стойкость в почве; только из литературы, иначе ровно «**Нет данных.**» (без пояснений, не выдумывать!)
6. `## 📅 PHI и MRL` — PHI, MRL EU/USA/Codex; отсутствуют → ровно «**Нет данных.**»; какие БД опрашивались — в артефакт, не в карточку
7. `## ⚠️ Ограничения и противопоказания` — НЕ-CSV ограничения: сорт-зависимость, контраиндикации,
   взаимодействия, летучесть (severity + источники). Секция — только при наличии данных
8. `## Источники` — список PMID/DOI/URL (+ ссылка на артефакт поиска)

### Стиль карточек: конечные факты, не процесс (стиль-гайд v2.0, 2026-08-06)
Карточка — это конечные факты с источниками, а НЕ отчёт о работе. Всё процессное уместно
только в артефактах `raw/evidence/**` и `raw/sources/**`. Обязательно:

1. **Нет баннеров и служебной метаинформации.** Статусы и даты (`validation_status`,
   `evidence_level`, `last_checked`, `next_review`, контракт, фаза, «валидировано …») живут
   ТОЛЬКО в frontmatter. Баннеры вида «✅ Валидировано 2026-08-04 … Статус: …» в теле запрещены.
2. **Нет описания процесса поиска.** Запрещено: «запросы → 0 PMID», «fallback → 0»,
   «искали в PubMed/Europe PMC», «только title_only», «БД не опрашивались», «по правилам
   честности», «null по правилам честности». Процесс и provenance — в артефактах.
3. **«Нет данных» — конечный ответ.** Секция без данных содержит ровно «**Нет данных.**»
   (допустимо уточнение предмета, например «об укоренении усов в полевых условиях»).
   Без пояснений, как и почему искали.
4. **Одна CSV-заявка — одна строка таблицы `Валидация CSV-заявок`.** Вердикты по CSV
   («не подтверждено», «частично», «доза выше/ниже литературной») упоминаются ТОЛЬКО в этой
   таблице; в других секциях (Научные данные по культурам, Идентичность, Механизм, Toxicity)
   отсылки к CSV-заявкам запрещены. Секций «Corrected Dosages» и «Противоречия» больше нет.
5. **Gap-строки в научных данных** — только «Нет данных о …», без деталей поиска («0 PMID»,
   списков запросов, fallback-цепочек).
6. **Frontmatter `notes`** — только не-табличные факты: объединение кодов, миграции, связи с
   другими карточками. Резюме вердиктов (таблица валидации) и эффектов (Научные данные
   по культурам) дублировать ЗАПРЕЩЕНО. Нет таких фактов → `notes: []`.
7. **Нейтральные формулировки:** «эффективен при X (PMID)», «данных нет», «CSV-значение Y
   не подтверждено литературой (PMID)». Без «мы», «нашлось», «обнаружили», «проверили».
8. **Заголовки без служебных пометок:** `### 🍅 Томат (Solanum lycopersicum)` — без суффиксов
   вроде `— found_verified`; статусы культур живут в frontmatter `crops`.
9. **Frontmatter — только поля с машинными потребителями** (Dataview, скрипты, LLM-парсинг):
   `action_category`, `efficacy_csv`, `crops`, `aliases`, `aliases_ru`, `fallback_status` и т.п.
   Поля-зеркала секций (application_csv, sources, toxicity_window, phi_mrl) и всегда-null
   заглушки (eppo_code, regulatory_status, consensus_score) ЗАПРЕЩЕНЫ.
10. **Полная замена файла при валидации — без хвостов от черновика.** При записи
    валидированной карточки файл перезаписывается ЦЕЛИКОМ (все секции черновика заменяются
    фактическими). Запрещено оставлять нижние секции-заглушки бутстрапа: HTML-комментарии
    (`<!-- нет данных по культуре -->`, `<!-- ED50/TD50... -->`, `<!-- PMID / DOI / URL -->`),
    повторяющиеся заголовки `##` (дубли секций) и «хвосты» в конце файла. `smoke_test.py`
    проверяет: у валидированных карточек нет комментариев-заглушек, дублей секций и
    служебной обвязки в секции «📅 PHI и MRL» (задача PHI_REI, «в открытых БД»,
    «этикеткой препарата», «национальной авторизацией», EUPD/PPDB).

Пример (эталон): `Vault/wiki/substances/IBA.md` — обновлён по стиль-гайду v2.0.

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
- **Синонимы веществ:** перед поиском PubChem по `csv_name` → `synonyms` + `iupac_name`; все синонимы в запросы (OR). Реестр: `raw/normalization/synonyms.json` (генерируется `_scripts/gen_synonyms.py` из frontmatter карточек; **обновлять после валидации**, когда в карточку добавлены aliases).
- **Русские синонимы:** `aliases_ru` в frontmatter карточки (MeJA → Метилжасмонат, GA3 → Гибберелловая кислота, IBA → Индолилмасляная кислота) — русский поиск по вики работает, граф не ломается.
- **Конверсия единиц:** ppm ≈ mg/L (водные растворы); µM/mM конвертируются через молярную массу из PubChem, конверсия записывается в `dosage_normalized` с источником. Без молярной массы (не найдена) — единицы не сравнивать, пометить в notes.
- **Фенофазы BBCH:** при валидации искать ключи BBCH / growth stage / phenological / anthesis / fruit set / veraison; фаза применения указывается в `conditions.bbch_stages` (BBCH 61 = 10% цветков открыто, BBCH 73 = зелёная ягода).
- **Совпадение CAS** у двух кодов CSV → объединить в одну страницу, коды в `aliases`.
- **Культуры:** Томат = Solanum lycopersicum, Огурец = Cucumis sativus, Клубника = Fragaria × ananassa. Синонимы использовать в fallback-запросах.
- **Единицы:** ppm/mg/L/µM не конвертировать, писать как в источнике + в CSV.
- **Классы:** 89 CSV-классов → 29 семейств (страницы `wiki/classes/`, маппинг в `_scripts/gen_taxonomy.py`). Поле `class_family` в карточке — slug семейства, `mechanism` — slug механизма (страницы `wiki/mechanisms/`, 15 механизмов). При генерации новых карточек запускать `python _scripts/gen_taxonomy.py` (идемпотентно).

## Контракт отчёта сабагента поиска (JSON v1.4)
Один запуск = одно вещество × 3 культуры. Схема (обязательные поля, enum'ы строгие):

**Правки v1.3 (по итогам пилота 2026-08-04):**
- Сабагент **НЕ пишет файлы** — возвращает JSON в финальном сообщении (может обернуть в ```json или дописать текст после JSON). Артефакт сохраняет **оркестратор** через `_scripts/extract_report.py` (raw_decode на каждой `{`).
- Добавлено поле **`related_evidence`** в `crops.<культура>` — для статуса `no_data`: ближайшие работы по веществу ВНЕ целевой культуры (чтобы «нет данных» было обосновано, а не голословно).
- `contraindications` и `conflicts` — **только массивы объектов**; пусто → `[]`, **запрещены** null-заглушки и строки вместо dict (L1 это проверяет).
- **Europe PMC** часто недоступен в среде сабагента (IPv6-блок) → сабагент помечает в `searches.failed`, а **оркестратор сам выполняет Europe PMC-запрос** в своей среде и дополняет артефакт перед записью карточки.

**Правки v1.4 (по итогам внешнего аудита 2026-08-04):**
- Добавлено поле **`taxonomy_check`** — сабагент обязан подтвердить или исправить таксономию карточки: в промпт передаются текущие `class_family` и `mechanism` из frontmatter карточки; сабагент сверяет их с литературой и сообщает `class_family_confirmed` / `mechanism_confirmed` (bool). При исправлении — заполняет `corrections` (массив `{field, from, to, reason}`). L1 проверяет обязательность и типы.
- Оркестратор применяет `corrections` к frontmatter карточки (поле `mechanism`/`class_family`), фиксирует в `notes`; обратные изменения в `_scripts/gen_taxonomy.py` (OVERRIDES) — только через `--refresh` после правки маппинга (по умолчанию скрипт ручные правки не перезаписывает).
```json
{
  "contract_version": "1.4",
  "substance": {"code": "IBA", "csv_name": "...", "queried_name": "..."},
  "searches": {
    "performed": ["pubmed_tomato", "pubmed_cucumber", "pubmed_strawberry", "openalex", "pubchem"],
    "failed": [{"endpoint": "europepmc", "reason": "IPv6 blocked", "query": "...", "retry_by_orchestrator": true}],
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
  "taxonomy_check": {"class_family_confirmed": true, "mechanism_confirmed": true,
                     "corrections": [{"field": "mechanism", "from": "pesticide_action",
                                      "to": "antioxidant_defense", "reason": "..."}],
                     "notes": "..."},
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
10. **Europe PMC:** если у сабагента `searches.failed` содержит `{endpoint: "europepmc", retry_by_orchestrator: true}` → оркестратор сам выполняет запрос в своей среде, дополняет отчёт как `orchestrator_fallback` (файл `raw/evidence/{A-Z}/<код>/orchestrator_fallback_<дата>.json`) и логирует в log.md. Если и оркестратор не может → `europepmc_unavailable`, не блокирует валидацию.
11. **Иммутабельность артефактов (v1.4, по итогам аудита):** `raw/evidence/**/search_*.json` **НИКОГДА не редактируются** (включая мелкие type-fix). Ошибка схемы в отчёте → оркестратор **не правит файл**, а: (а) возвращает сабагенту на перезапуск, либо (б) создаёт новый артефакт `search_<код>_<дата>_rev2.json` с полем `"supersedes": "<имя старого файла>"` (старый остаётся иммутабельным). L1 проверяет существование supersedes-файла. **При создании rev2-артефакта ОБЯЗАТЕЛЬНО прогнать его через L1** (дополнение аудита).
12. **Retry сабагентов (v1.4):** пустой/незавершённый ответ сабагента — не блокер: автоматический повторный запуск (до 2 попыток), причина фиксируется в `task_queue.md` (строка `RETRY: <код> — <причина>`). Если после retry ответа нет → карточка `insufficient_data` с gap-описанием, очередь не блокируется.
13. **Препринты PPR:** источники `PPR:<id>`/`paper_type: preprint` — **не учитываются как strong-доказательство** (evidence_level strong только по PMID/DOI-рецензированным); DOI препринтов проходят Crossref-проверку L1. В карточках PPR помечаются словом «препринт».
14. **PHI/REI (v1.4, уточнено по итогам практики):** для пестицидов/ретардантов (class_family: fungicides, insecticides, synthetic_growth_regulators с efficacy HIGH) практический блокер — **PHI (Pre-Harvest Interval, срок ожидания до уборки) и REI (Re-entry Interval, срок выхода на работы)**, а не MRL. Источники PHI/REI: этикетки конкретных препаратов, национальные реестры СЗР (e-phy FR, BVL DE, EPA/US, Госреестр РФ), инструкции производителя; в открытых БД (EUPD/PPDB/Codex) PHI/REI, как правило, отсутствуют. **Сбор PHI/REI — процесс (артефакт `raw/sources/`, задача PHI_REI в task_queue), НЕ содержимое карточки.** В карточке PHI/REI пишется лаконично: если реальных данных из литературы/этикеток нет → **«Нет данных.»**; если есть реальные значения (из этикеток/реестров) → факт с источником. В карточку **запрещено** переносить формулировки процесса («в открытых БД не найдены», «задача PHI_REI в task_queue», «устанавливаются этикеткой препарата/национальной авторизацией») — это служебная обвязка, её место в артефакте/очереди. Статус при отсутствии PHI/REI-данных не выше `partial`. **Выдумывать waiting periods ЗАПРЕЩЕНО** — не найдено → `unknown`. MRL — справочная информация (EUPD доступен через Playwright MCP: секция MRLs; Codex — API /jsoncodexpest/), **не блокер**; реальные MRL-значения (если собраны) — полезный факт в карточке.

## Принцип «тонкий агент — толстый артефакт»
- Агент stateless: читает артефакт → одно действие → пишет новый артефакт. Памяти между вызовами нет.
- Артефакт самодостаточен: provenance (кто, когда, из каких источников) внутри файла.
- `raw/evidence/{A-Z}/<код>/search_*.json` — иммутабелен (не редактировать!).
- `raw/evidence/{A-Z}/<код>/facts_*.md` — извлечённые факты.
- `raw/evidence/{A-Z}/<код>/validation_*.md` — отчёт валидации vs CSV.
- Wiki-карточка — обновляемое представление артефактов (история в git).
- Оркестратор (главный агент) — финальный арбитр task_queue.md и log.md.

## Europe PMC Fallback
Если сабагент сообщает о недоступности Europe PMC (`searches.failed` с `endpoint: "europepmc"`, `retry_by_orchestrator: true`):
1. **Оркестратор повторяет запрос в своей среде** (у него Europe PMC работает).
2. Найденные результаты добавляются в отчёт как `orchestrator_fallback` и сохраняются в `raw/evidence/{A-Z}/<код>/orchestrator_fallback_<дата>.json`.
3. Если и оркестратор не может → статус `europepmc_unavailable` в `searches.failed[].status`, **не блокирует валидацию** (PubMed/OpenAlex/Crossref всё равно работают).
4. Запись в log.md: `## [дата] europepmc_fallback | <вещество> | N результатов`.

## Проверка отчётов (4 уровня)
- **L1 Автопроверка (`_scripts/l1_check.py`):** JSON по схеме; **type-check** обязательных полей — `conflicts`/`contraindications` должны быть массивами объектов (не строки, не null); каждый PMID через esummary (существует, заголовок матчит); DOI через Crossref.
- **L2 Перекрёстная:** дубли PMID между культурами допустимы, claims не должны противоречить; противоречия → `conflicts`.
- **L3 Человек:** `conflicting` и критичные исправления → дашборд «требуют внимания» в validation.md, пользователь просматривает.
- **L4 Повторная (Lint):** next_review; новый поиск публикаций по ключевым веществам.

## Процедуры

### Ingest (новые источники)
1. Файл/клип → `raw/sources/<код вещества>/` (иммутабельно, имя: `<дата>_<описание>.pdf|md`);
   черновики пользователя из `Vault/raw/` (рабочая папка в Obsidian, gitignored) переносить сюда же
2. Запись в log.md: `## [дата] ingest | <вещество> | <источник>`
3. Если источник добавляет факты → обновить карточку и `raw/evidence/.../facts_*.md`

### Validation (ядро работы)
Цикл на вещество: поиск по 3 культурам (сабагент) → сабагент возвращает JSON в финальном сообщении → **оркестратор извлекает и сохраняет артефакт** (`_scripts/extract_report.py` → `raw/evidence/{A-Z}/<код>/search_*.json`) → при `searches.failed` с europepmc оркестратор сам дополняет запрос → L1/L2 проверка → карточка + «Научные данные по культурам» + «Валидация CSV-заявок» → task_queue.md + validation.md + log.md. **При записи карточки файл перезаписывается ЦЕЛИКОМ** (стиль-гайд правило 10): не оставлять секции-заглушки черновика, HTML-комментарии и «хвосты» в конце; после пакета — `python _scripts/smoke_test.py` (exit 0).
**Обработка exit code extract_report.py (аудит 2026-08-04):** после каждого запуска проверять `$LASTEXITCODE` И stdout: `0` = ок (JSON извлечён); `2` = `RETRY_NEEDED` → выполнить повторный запуск сабагента (до 2 попыток), новые файлы ответа передать как `[src2] [src3]`; после 2 неудач → карточка `insufficient_data`, очередь не блокируется. RETRY-строки логируются скриптом в task_queue.md автоматически.
**Синхронизация дашбордов:** при обновлении `validation.md` ОБЯЗАТЕЛЬНО проверить `Vault/index.md` (живой Dataview-дашборд) — оба должны отражать одно состояние.
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
> ⚠️ Инструмент `fetch_webpage` Copilot может быть недоступен (NotAuthorized) — использовать
> Python/urllib в терминале; для JS-приложений (EUPD, Codex, национальные реестры) — **Playwright MCP**
> (браузер: navigate → snapshot/find → run_code → таблицы через `page.evaluate`).
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

## Эксплуатация скриптов (аудит 2026-08-06)
- **НЕ запускать `bootstrap.py` «просто посмотреть»/для проверки синтаксиса** — он ПЕРЕЗАПИСЫВАЕТ
  unverified-черновики (регрессия 2026-08-06: пересоздал объединённые карточки MeJA/TRIA и стёр
  таксономию). Проверка: `python -m py_compile _scripts/bootstrap.py` или `bootstrap.py --dry-run`
  (ничего не пишет, показывает CREATE/REWRITE/SKIP). Реальный запуск — только для перегенерации
  черновиков; после него bootstrap сам вызывает `gen_taxonomy.py` (заполняет class_family/mechanism).
- **Smoke-тест:** после любых массовых операций с карточками `python _scripts/smoke_test.py`
  (exit 0 = ок): проверяет отсутствие дублей кодов, запрещённых полей frontmatter, старых секций
  и баннеров у валидированных карточек, наличие таксономии у всех; у валидированных карточек —
  отсутствие хвостов бутстрапа (HTML-комментарии-заглушки, дубли секций ##) и служебной обвязки
  в секции «📅 PHI и MRL» (задача PHI_REI, «в открытых БД», «этикеткой препарата»,
  «национальной авторизацией», EUPD/PPDB).
- **EOL:** репозиторий CRLF для md/json/csv, LF для .py (`.gitattributes`); после изменения
  `.gitattributes` — `git add --renormalize .`; файлы писать через Python с явной кодировкой/EOL,
  НЕ через Add-Content (пишет ANSI).

## Приоритеты и расписание
1 сессия = пакет 10–20 веществ (5–10 сабагентов параллельно) → карточки → трекер.
Оценка: 80–120 ч ≈ 30–40 сессий по 2–3 ч. HIGH ≈ 3–5 сессий.
