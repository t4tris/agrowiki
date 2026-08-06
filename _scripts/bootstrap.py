# -*- coding: utf-8 -*-
"""Bootstrap: CSV -> substance cards (+ crop hubs + index/log/task_queue/validation on --full).

DEFAULT (safe): regenerates ONLY substance cards (SKIPs cards with validation_status
!= unverified unless --force). Pass --full to also overwrite crops/index.md/
task_queue.md/validation.md/log.md/README.md (requires confirmation or --yes).
"""
import argparse
import csv
import os
import re
import subprocess
import sys
from collections import defaultdict

# Коды CSV, объединённые в карточки-каноны (dedup/merge, см. log.md) — карточек не имеют,
# НЕ пересоздавать при генерации черновиков (синхронизировано с gen_taxonomy.MERGED_CODES)
MERGED_CODES = {'MeJA (Methyl Jasmonate)', 'Triacontanol (TRIA)'}

CSV = r'f:\agrowiki\raw\Complete_Action_Oriented_Agronomic_Substances_CLEANED_v6.csv'
VAULT = r'f:\agrowiki\Vault'

CROP_KEYWORDS = {
    'tomato': ['tomato'],
    'cucumber': ['cucumber'],
    'strawberry': ['strawberry'],
}
CROP_RU = {'tomato': 'Томат', 'cucumber': 'Огурец', 'strawberry': 'Клубника'}
CROP_LATIN = {'tomato': 'Solanum lycopersicum', 'cucumber': 'Cucumis sativus',
              'strawberry': 'Fragaria × ananassa'}
PRIO = {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}


def sanitize(name):
    return re.sub(r'[\\/:*?"<>|]', '_', name).strip()


def crop_mentions(tc):
    t = (tc or '').lower()
    return {c for c, kws in CROP_KEYWORDS.items() if any(k in t for k in kws)}


def esc(v):
    v = (v or '').strip().replace('|', '\\|')
    return v or '—'


def code_priority(groups, code):
    return min(PRIO.get(r['Efficacy_Level'].strip().upper(), 3) for r in groups[code])


def main():
    parser = argparse.ArgumentParser(description='Bootstrap substance cards from CSV')
    parser.add_argument('--full', action='store_true',
                        help='ПОЛНЫЙ запуск: карточки + crops/index/task_queue/validation/log/README '
                             '(перезаписывает ручные правки; требует подтверждения или --yes)')
    parser.add_argument('--yes', action='store_true',
                        help='подтвердить --full без интерактивного prompt')
    parser.add_argument('--force', action='store_true',
                        help='перегенерировать и не-unverified карточки (по умолчанию они пропускаются)')
    parser.add_argument('--dry-run', action='store_true',
                        help='ничего не писать: вывести, что было бы сделано (использовать вместо запуска '
                             'для проверки! скрипт ПЕРЕЗАПИСЫВАЕТ unverified-черновики)')
    args = parser.parse_args()

    with open(CSV, encoding='utf-8-sig') as f:
        rows = list(csv.DictReader(f))

    groups = defaultdict(list)
    for r in rows:
        groups[r['Active_Substance_Code'].strip()].append(r)

    codes = sorted(groups.keys())
    print(f'rows={len(rows)} unique_codes={len(codes)} '
          f'dups={[c for c in codes if len(groups[c]) > 1]}')

    # ---- substance cards ----
    subst_dir = os.path.join(VAULT, 'wiki', 'substances')
    os.makedirs(subst_dir, exist_ok=True)
    for code in codes:
        rs = groups[code]
        crops_yml = '\n'.join(
            f'  {c}: no_data' for c in ('tomato', 'cucumber', 'strawberry'))
        eff = min(PRIO.get(r['Efficacy_Level'].strip().upper(), 3) for r in rs)
        eff_name = {0: 'HIGH', 1: 'MEDIUM', 2: 'LOW'}.get(eff, 'EMPTY')
        name_en = esc(rs[0]['Active_Substance_Name'])
        classes = sorted({r['Chemical_Class'].strip() for r in rs if r['Chemical_Class'].strip()})
        cats = sorted({r['Action_Category'].strip() for r in rs if r['Action_Category'].strip()})
        claims = '\n'.join(
            f'| {esc(r["Action_Category"])} | {esc(r["Specific_Action"])} | '
            f'{esc(r["Application_Method_Dosage"])} | {esc(r["Expected_Result"])} | '
            f'{esc(r["Efficacy_Level"])} | {esc(r["Target_Crops"])} |'
            for r in rs)
        moa = esc(rs[0]['Mode_of_Action'])
        claims = '\n'.join(
            f'| {esc(r["Specific_Action"])}{": " + esc(r["Application_Method_Dosage"]) if r["Application_Method_Dosage"].strip() else ""} | ⚪ Нет данных | — | — | — | — |'
            for r in rs)

        page = f"""---
type: substance
code: {code}
name_en: {name_en}
cas: 
formula: 
class: {'; '.join(classes) if classes else '—'}
action_category: {', '.join(cats) if cats else '—'}
efficacy_csv: {eff_name}
validation_status: unverified
evidence_level: unverified
last_checked: 
next_review: 
notes: []
crops:
{crops_yml}
aliases: []
aliases_ru: []
---

# {code} — {name_en}

> ⚠️ Черновик из CSV. Статус: `unverified`. Валидация по культурам (томат/огурец/клубника) — впереди.

## Идентичность
<!-- CAS, формула, класс — проверить через PubChem -->

## Механизм действия
{moa if moa != '—' else '<!-- пусто в CSV -->'}

## ⚠️ Валидация CSV-заявок
| CSV-заявка | Вердикт | Уточнение | Условия | Severity | Источники |
|---|---|---|---|---|---|
{claims}

## Научные данные по культурам
<!-- После валидации: методы применения, дозировки и эффекты по каждой культуре с PMID/DOI -->

### 🍅 Томат (Solanum lycopersicum)
<!-- нет данных по культуре -->

### 🥒 Огурец (Cucumis sativus)
<!-- нет данных по культуре -->

### 🍓 Клубника (Fragaria × ananassa)
<!-- нет данных по культуре -->

## ⚠️ Toxicity Window
<!-- ED50/TD50/therapeutic index/стойкость в почве — только из литературы -->

## 📅 PHI и MRL
<!-- PHI, MRL EU/USA/Codex; отсутствуют → «Нет данных.» -->

## Источники
<!-- PMID / DOI / URL -->
"""
        card_path = os.path.join(subst_dir, f'{sanitize(code)}.md')
        if code in MERGED_CODES:
            print(f'SKIP (MERGED_CODES): {code}')
            continue
        if os.path.exists(card_path) and not args.force:
            existing = open(card_path, encoding='utf-8').read()
            if re.search(r'^validation_status:\s*(?!unverified)\S', existing, re.M):
                print(f'SKIP (статус != unverified): {code}')
                continue
        if args.dry_run:
            action = 'REWRITE' if os.path.exists(card_path) else 'CREATE'
            print(f'[{action}] {code}')
            continue
        with open(card_path, 'w', encoding='utf-8') as f:
            f.write(page)

    # bootstrap не пишет class_family/mechanism — их добавляет gen_taxonomy;
    # запускать после каждой генерации черновиков, иначе таксономия теряется
    if not args.dry_run:
        gt = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_taxonomy.py')
        subprocess.run([sys.executable, gt], check=False)

    if not args.full:
        print(f'DONE (cards only, default): substances={len(codes)}')
        return
    if not args.yes:
        ans = input('WARNING: полный запуск перезапишет index.md, task_queue.md, validation.md, '
                    'log.md, README.md и страницы культур (ручные правки будут потеряны). Продолжить? [y/N] ')
        if ans.strip().lower() != 'y':
            print('Отменено.')
            return

    # ---- crop hubs ----
    crops_dir = os.path.join(VAULT, 'wiki', 'crops')
    os.makedirs(crops_dir, exist_ok=True)
    for crop in ('tomato', 'cucumber', 'strawberry'):
        explicit = []
        for c in codes:
            ms = set()
            for r in groups[c]:
                ms |= crop_mentions(r['Target_Crops'])
            if crop in ms:
                explicit.append(c)
        links = '\n'.join(f'- [[{c}]]' for c in explicit)
        page = f"""---
type: crop
name: {CROP_RU[crop]}
name_latin: {CROP_LATIN[crop]}
substances: [{', '.join(explicit)}]
---

# {CROP_RU[crop]} ({CROP_LATIN[crop]})

> Культура-хаб. Поиск литературы для этой вики ограничен 3 культурами: томат, огурец, клубника.

## Вещества по CSV (явное упоминание) — {len(explicit)}
{links if links else '_нет явных упоминаний в CSV_'}
<!-- Под-индекс через Dataview:
```dataview
LIST
FROM "wiki/substances"
WHERE contains(crops.{crop}, "found_verified") OR contains(crops.{crop}, "found_unverified")
```
-->

## Вещества с общими формулировками (all crops / fruit crops / vegetables)
<!-- Требуют ручной проверки: уточнить, применима ли культура -->

## Валидированные дозировки
<!-- Заполняется после Фазы 3: Dataview-выборка карточек со статусом verified/corrected по культуре -->

## Синтезы
<!-- ссылки на wiki/syntheses/ -->
"""
        with open(os.path.join(crops_dir, f'{CROP_RU[crop]}.md'), 'w', encoding='utf-8') as f:
            f.write(page)

    # ---- index.md ----
    index = f"""# Index — Агрономическая вики

База валидированных агрономических веществ ({len(codes)} веществ, 3 фокусные культуры).
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
"""
    with open(os.path.join(VAULT, 'index.md'), 'w', encoding='utf-8') as f:
        f.write(index)

    # ---- task_queue.md ----
    lines = {'HIGH': [], 'MEDIUM': [], 'LOW': []}
    for c in codes:
        p = code_priority(groups, c)
        key = {0: 'HIGH', 1: 'MEDIUM', 2: 'LOW'}.get(p, 'LOW')
        lines[key].append(f'- [ ] VALIDATE: {c} × 3 культуры')
    queue = f"""---
type: task_queue
last_updated: {__import__('datetime').date.today().isoformat()}
---

# Task Queue

## 🔴 HIGH PRIORITY ({len(lines['HIGH'])})
{chr(10).join(lines['HIGH'])}

## 🟡 MEDIUM PRIORITY ({len(lines['MEDIUM'])})
{chr(10).join(lines['MEDIUM'])}

## 🟢 LOW PRIORITY ({len(lines['LOW'])})
{chr(10).join(lines['LOW'])}

## ✅ COMPLETED
- [x] INGEST: CSV → {len(codes)} черновиков карточек
"""
    with open(os.path.join(VAULT, 'task_queue.md'), 'w', encoding='utf-8') as f:
        f.write(queue)

    # ---- validation.md ----
    validation = f"""# Дашборд валидации

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
"""
    with open(os.path.join(VAULT, 'validation.md'), 'w', encoding='utf-8') as f:
        f.write(validation)

    # ---- log.md ----
    today = __import__('datetime').date.today().isoformat()
    log = f"""# Log

## [{today}] ingest | CSV | {len(rows)} строк → raw/
## [{today}] bootstrap | {len(codes)} черновиков карточек создан
"""
    with open(os.path.join(VAULT, 'log.md'), 'w', encoding='utf-8') as f:
        f.write(log)

    # ---- README.md ----
    readme = f"""# Агрономическая вики (Obsidian «второй мозг»)

- **Источник данных:** raw/Complete_Action_Oriented_Agronomic_Substances_CLEANED_v6.csv ({len(rows)} строк, {len(codes)} веществ)
- **Метод:** Karpathy LLM Wiki — raw (иммутабельно) → wiki (пишет LLM) → AGENTS.md (схема)
- **Фокус валидации:** 3 культуры — томат, огурец, клубника
- **Правила для LLM:** [[AGENTS.md]] · **Каталог:** [[index]] · **Журнал:** [[log]] · **Очередь:** [[task_queue]] · **Дашборд:** [[validation]]
"""
    with open(os.path.join(VAULT, 'README.md'), 'w', encoding='utf-8') as f:
        f.write(readme)

    print(f'DONE: substances={len(codes)}, crops=3, index/log/task_queue/validation/README written')


if __name__ == '__main__':
    main()
