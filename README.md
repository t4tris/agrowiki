# 🌱 АгровИки — база валидированных агрономических веществ

> Obsidian-вики по методу Karpathy LLM Wiki: **каждое вещество из CSV → научно валидированная
> карточка** с уровнем доказательности, дозировками и ссылками на литературу.
> Фокус: **три культуры — томат, огурец, клубника**.

## 🎯 Что это

Исходник — коммерческий CSV со 267 агрономическими веществами (стимуляторы, ретарданты,
фунгициды, биостимуляторы…). CSV неполон и неточен, поэтому LLM-агент **валидирует каждую
строку по научной литературе** (PubMed, Europe PMC, OpenAlex, PubChem) и пишет карточку:
что подтверждено, что исправлено, чего в литературе нет (честный статус `no_data`).

**Главный принцип — честность:** никаких выдуманных дозировок и PMID; «нет данных» — это
статус, а не повод придумать.

## 📊 Текущее состояние (2026-08-04)

| Показатель | Значение |
|---|---|
| Веществ в базе | 267 |
| Валидировано карточек | **11** (HIGH-приоритет, контракт v1.4; MeJA и TRIA объединены в Methyl Jasmonate и Triacontanol) |
| Очередь | HIGH 38 · MEDIUM 133 · LOW 83 |
| Уровень доказательности | strong / moderate / weak / unverified |
| Статусы валидации | verified · corrected · partial · insufficient_data · conflicting |
| Источники | PMID + DOI (проверяются автоматически L1) + препринты PPR |

## 📁 Структура проекта

```
f:\agrowiki\
├── AGENTS.md            ← схема для LLM (правила, контракт отчёта v1.4)
├── log.md               ← хронология всех операций
├── task_queue.md        ← очередь валидации и тех. долга
├── validation.md        ← трекер для LLM
├── raw/                 ← источники (иммутабельно)
│   ├── *.csv            ← исходные данные
│   ├── evidence/        ← артефакты поиска (search_*.json, orchestrator_fallback)
│   ├── sources/         ← PDF/клипы статей + papers_to_fetch.md (очередь скачивания)
│   └── normalization/   ← synonyms.json (реестр синонимов)
├── _scripts/            ← Python-инструменты конвейера
├── _meta/               ← plan.md, handoff.md, session_report_*.md (для аудитов)
└── Vault/               ← Obsidian vault (только контент)
    ├── index.md         ← каталог + дашборд статусов (Dataview)
    ├── raw/             ← рабочая папка: черновики будущих sources (в Obsidian, в .gitignore)
    └── wiki/
        ├── substances/  ← 265 страниц (267 кодов CSV, 2 пары объединены)
        ├── categories/  ← 9 категорий применения
        ├── classes/     ← 29 семейств химических классов
        ├── mechanisms/  ← 15 механизмов действия
        ├── crops/       ← 3 культуры-хаба
        └── syntheses/   ← сравнительные ответы (Фаза 4)
```

## 🚀 Как пользоваться

### Для человека (Obsidian)
1. Откройте vault: **Obsidian → Open folder → `f:\agrowiki\Vault`**
2. `index.md` — каталог и живой дашборд статусов (Dataview)
3. Поиск по русским названиям работает: `aliases_ru` в карточках (напр., «метилжасмонат» → MeJA)

### Как читать карточку вещества (`wiki/substances/<код>.md`)
- **Frontmatter** — машиночитаемые поля: `validation_status`, `evidence_level`, `crops` (по 3 культурам), `class_family`, `mechanism`, `aliases_ru`
- **Секции**: Идентичность → Механизм действия → ⚠️ Валидация CSV-заявок → Научные данные по культурам (по культурам с PMID/DOI) → Toxicity Window → 📅 PHI и MRL → Ограничения и противопоказания → Источники
- Статусы: ✅ `verified`/`corrected` — подтверждено; 🟡 `partial` — частично; ⚪ `insufficient_data` — данных мало; 🔴 `conflicting` — противоречия

### Для LLM-агента
Работа строго по `AGENTS.md`: контракт отчёта **v1.4** (сабагент возвращает JSON,
оркестратор сохраняет артефакт → L1-проверка → карточка). Отчёты сессий для внешнего аудита —
`_meta/session_report_*.md` (навык `.github/copilot-skills/session-audit-report/`).

## ⚙️ Инструменты конвейера (`_scripts/`)

| Скрипт | Назначение |
|---|---|
| `extract_report.py` | Извлечение JSON из ответа сабагента; **авто-retry** (до 3 файлов), exit 2 = нужен повторный запуск |
| `l1_check.py` | L1: схема v1.4 + type-check + `taxonomy_check` + `supersedes` + PMID (esummary) + DOI (Crossref) |
| `fallback_europepmc.py` | Europe PMC fallback оркестратора (SRC:PPR препринты) → `orchestrator_fallback_*.json` |
| `gen_taxonomy.py` | Таксономия: 9 категорий + 29 семейств + 15 механизмов (`--refresh` для пересчёта) |
| `gen_synonyms.py` | `raw/normalization/synonyms.json` из aliases карточек |
| `bootstrap.py` | Черновики карточек из CSV (по умолчанию — только карточки; `--full` перезаписывает служебные файлы!) |
| `digest.py` | Компактный дайджест отчётов |

## 🔑 API и доступы

- **Без ключей**: PubMed E-utilities, Europe PMC, PubChem, OpenAlex, Crossref, PPDB (регуляторика),
  EU Pesticides Database + Codex (через **Playwright MCP**), Wikipedia
- **По ключу (опционально)**: Semantic Scholar, Consensus, ChemSpider, EPPO — `.secrets/api_keys.env`
- `fetch_webpage` Copilot может быть недоступен → Python/urllib + Playwright MCP

## 📜 Правила (коротко)

- `raw/` — **иммутабельно** (артефакты не редактируются; правка → новый файл с `supersedes`)
- PHI/REI — практический блокер для пестицидов (**не выдумывать waiting periods** → `unknown`);
  MRL — справочно
- Противоречия не стираются — фиксируются в `notes`/`conflicts`
- Служебный слой — вне vault; внутри vault — только вики-ссылки `[[...]]`

## 📚 Документы

| Файл | Что это |
|---|---|
| `AGENTS.md` | Схема для LLM (контракт v1.4, правила честности 1–14, процедуры) |
| `_meta/plan.md` | Мастер-план (фазы 0–5) |
| `_meta/handoff.md` | Мостик для следующей сессии |
| `_meta/sdd_openspec_context.md` | Контекст для SDD-переосмысления проекта (OpenSpec-брейншторм: философия, эмпирика, подводные камни) |
| `log.md` / `task_queue.md` / `validation.md` | Журнал / очередь / трекер |
| `_meta/session_report_2026-08-04*.md` | Репорты для внешних аудитов (части 1–3) |
| `Vault/index.md` | Каталог + дашборд (Dataview) |

## 🤝 Контрибьюция (человек)

1. **Скачивание статей**: очередь `raw/sources/papers_to_fetch.md` → файлы в `raw/sources/<код>/`
2. **PHI/REI**: этикетки препаратов/нац. реестры → `raw/sources/<код>/`
3. **Ревью**: конфликтные карточки (`validation_status: conflicting`) — дашборд «Требуют внимания»
4. Git: ветка `main`, push на `github.com/t4tris/agrowiki` (Obsidian Git: «Commit and sync»)
