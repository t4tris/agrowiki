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
| `_meta/session_report_2026-08-04.md` | **Отчёт сессии для внешнего аудита** (часть 1: инфраструктура, 10 коммитов) |
| `_meta/session_report_2026-08-04_part2.md` | **Отчёт сессии для внешнего аудита** (часть 2: реализация ревью + пилот Фазы 3, 5 коммитов) |
| `_meta/session_report_2026-08-04_part3.md` | **Отчёт сессии для внешнего аудита** (часть 3: реализация ревью part 2, 1 коммит) |
| `_meta/handoff.md` | **Этот файл** — состояние и следующие шаги |
| `AGENTS.md` | Схема вики, контракт отчёта **v1.3**, правила честности, L1–L4 |
| `task_queue.md` | Очередь VALIDATE (HIGH 43 / MEDIUM 134 / LOW 83) |
| `validation.md` | Трекер валидации для LLM (Dataview в нём не рендерится — дашборд в `Vault/index.md`) |
| `log.md` | Хронология (append-only) |
| `_scripts/extract_report.py` | Извлечение JSON из ответа сабагента (raw_decode) + **идемпотентность (MD5-checksum)** |
| `_scripts/l1_check.py` | L1-проверка: схема + **type-check v1.3** + PMID esummary + DOI Crossref |
| `_scripts/digest.py` | Компактный дайджест отчётов |
| `raw/evidence/{A,C,G,I,T}/…/search_*_2026-08-04.json` | 5 иммутабельных артефактов пилота |
| `Vault/wiki/substances/*.md` | 7 валидированных карточек + 260 черновиков |

---

## 🟢 Статус проекта (на 2026-08-04)

**Пилот завершён и L1-проверен.** Конвейер «сабагент → JSON → оркестратор → карточка» работает. Контракт обновлён до **v1.3** — правки внесены в `AGENTS.md`, `l1_check.py`, `extract_report.py`, `validation.md` и **закрыты дефекты по рекомендациям LLM** (см. ниже). Все скрипты протестированы на сломанных/повторных входах.

### Вердикты пилота (7 карточек записаны)

| Вещество | Статус | Evidence | Ключевой вывод |
|---|---|---|---|
| [[wiki/substances/GA3]] | partial | moderate | Механизм усов подтверждён (4 аннотации); ВСЕ дозировки CSV не верифицированы |
| [[wiki/substances/IBA]] | corrected | moderate | CSV 100–1000 ppm замачивание семян на 2–3 порядка выше литературы (0.5 µM–1.5 мг/л, в осн. in vitro) |
| [[wiki/substances/Triacontanol]] | partial | moderate | CSV 0.05–0.2 ppm ниже рабочих 0.5–1 ppm; фотосинтез подтверждён в осн. в стрессе |
| [[wiki/substances/Artemisinin]] | insufficient_data | weak | Все 3 культуры no_data; обе CSV-заявки не подтверждены (70% галлов нигде нет; нематицидны кислоты A. annua, не артемизинин) |
| [[wiki/substances/Chitosan]] | partial | strong | Механизм подтверждён 21 аннотацией (~30–66% снижение болезней); CSV-протоколы не верифицированы |
| [[wiki/substances/Triacontanol (TRIA)]] | partial | moderate | Дубль Triacontanol — сателлит |
| [[wiki/substances/Chitooligosaccharides]] | partial | strong | Дубль Chitosan — сателлит |

---

## 🔧 Изменения контракта v1.3 (уже внесены в AGENTS.md + l1_check.py)

1. **Сабагенты не пишут файлы** → оркестратор извлекает JSON из ответа (`_scripts/extract_report.py`, **идемпотентен: MD5-checksum, SKIP при совпадении**) и сохраняет артефакт в `raw/evidence/{A-Z}/<код>/`.
2. **`related_evidence`** — новое поле в `crops.<культура>` для статуса `no_data` (ближайшие работы по веществу вне фокусных культур). L1 падает, если `no_data` без `related_evidence`.
3. **Type-check в L1 (усилен по рекомендациям LLM):**
   - `conflicts` — массив dict с **обязательными полями** `csv_field`/`csv_value`/`literature_summary`/`severity`/`sources`; строки вместо dict и null-заглушки **запрещены** (L1 падает).
   - `contraindications` — всегда массив (пустой `[]`), **никогда null**; L1 даёт явную ошибку на null.
4. **Europe PMC fallback:** сабагент помечает `searches.failed` с `retry_by_orchestrator: true` → **оркестратор сам выполняет Europe PMC-запрос** в своей среде, дополняет отчёт как `orchestrator_fallback` (файл `raw/evidence/{A-Z}/<код>/orchestrator_fallback_<дата>.json`). Если и оркестратор не может → `europepmc_unavailable`, не блокирует валидацию. Полный блок правила в AGENTS.md.
5. **`validation.md`** — добавлен дашборд «Требуют Europe PMC-повторного запроса» (Dataview по `fallback_status` = orchestrator / europepmc_unavailable).
6. Оценка времени: ~5 мин/вещество на поиск (не 15–45 мин).

**Проверено:** `l1_check.py` ловит все 6 дефектов на сломанном отчёте; `extract_report.py` корректно SKIP-ит повторный запуск.

---

## 🎯 Следующие шаги (Фаза 3)

### 0. Перед стартом — обработать пилотные пробелы
- [ ] **Europe PMC-повторные запросы** для GA3, Triacontanol, Chitosan (у них `searches.failed` с europepmc, `retry_by_orchestrator: true`) — выполнить оркестратором, дополнять карточки препринтами (SRC:PPR), сохранить в `raw/evidence/{A-Z}/<код>/orchestrator_fallback_<дата>.json`, отметить `fallback_status` в карточке.
- [ ] Пилотные артефакты — **v1.2**, иммутабельны, не перезаписывать. `l1_check.py` теперь требует v1.3 → новые отчёты должны быть v1.3.

### 1. Полный цикл валидации
Порядок приоритетов (в `task_queue.md`): **4 дубликата** (Phosphite, Serotonin, Carbonic acid, Humic Acid, Maleic Hydrazide, Melatonin — уточнить, какие именно остались неразрешёнными) → **HIGH (43)** → MEDIUM (134) → LOW (83).

**Рабочий цикл на вещество** (пакетами по 10–20 за сессию):
1. Запустить research-сабагент (stateless, самодостаточный промпт: CSV-строка + список API + контракт v1.3).
2. Извлечь JSON из ответа: `python _scripts/extract_report.py <ответ.txt> <код>`.
3. L1-проверка: `python _scripts/l1_check.py raw/evidence/{A}/<код>/search_*.json`.
4. При `searches.failed` с `retry_by_orchestrator: true` → оркестратор выполняет Europe PMC-запрос, дополняет артефакт (`orchestrator_fallback`), сохраняет `orchestrator_fallback_<дата>.json`, ставит `fallback_status` в карточке.
5. Написать карточку `wiki/substances/<код>.md` (frontmatter + crop_evidence + corrected_dosages + toxicity_window + PHI/MRL + contraindications + conflicts + источники).
6. Обновить `task_queue.md` (задача [x]), `validation.md`, `log.md`.
7. Коммит.

### 2. Рекомендуемые следующие вещества (HIGH, репрезентативные)
- **Paclobutrazol** — проверить узкий toxicity window (75 vs 300 ppm), остаточность в почве до 3 лет.
- **MeJA / Methyl Jasmonate** — летучесть при T>25°C, BBCH-фазы цветения томата.
- **Glycine Betaine** — стресс-протектор, много литературы.
- **Proline** — засухоустойчивость, Consensus-подобный вопрос.
- **Silicon** — HIGH, широко изучен на томате/огурце.

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
- Windows PowerShell, без `&&`/`||`. Консоль cp1252 → ставить `$env:PYTHONIOENCODING='utf-8'` перед Python-выводом кириллицы (mojibake косметический; файлы пишутся с `encoding='utf-8'` корректно).
- PubMed ≤3 req/сек без ключа (паузы 0.5–1 с, 1 повтор при ошибке). esummary батчи по 50.
- **Europe PMC заблокирован (IPv6) в среде сабагентов** — выполнять оркестратором.
- CSV: BOM → `utf-8-sig`; 8 кодов дублируются (объединены в сателлиты); 275 строк/267 уникальных кодов.
- Не использовать Sci-Hub (нарушение авторских прав) — только Unpaywall/PMC/DOAJ/OA-ссылки/Web Clipper.
- Параллельность: 5–10 сабагентов за раз.

---

## 🚫 Чего не делать
- Не перезаписывать иммутабельные `raw/evidence/*/search_*.json`.
- Не выдумывать PMID/DOI/дозировки; `verified: true` только при реально прочитанной аннотации.
- Не подставлять данные другой культуры при `no_data`.
- Не оставлять null-заглушки в `contraindications`/`conflicts` — пустой массив `[]`.
