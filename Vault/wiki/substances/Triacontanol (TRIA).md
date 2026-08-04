---
type: substance
code: Triacontanol (TRIA)
name_en: Triacontanol
cas: 593-50-0
formula: C30H62O
class: Long-chain alcohol
action_category: GROWTH_REGULATION
application_csv: Foliar spray 1-150 ppm; 50 µM for fruit coloration
efficacy_csv: MEDIUM
validation_status: partial
evidence_level: moderate
last_checked: 2026-08-04
next_review: 2026-09-04
sources: ["PMID:32290080", "PMID:35893617", "PMID:34969963", "PMID:24226183", "PMID:36466575"]
notes:
  - "Дубликат кода Triacontanol (строка 266 CSV) — та же субстанция, карточка-спутник [[Triacontanol]]"
  - "Подтверждено: 50 µM обработка плодов клубники ускоряет созревание, рост сахаров/антоцианов (PMID 32290080); 0.5-1 ppm фолиарно → +12.7% урожая (PMID 35893617)"
  - "НЕ верифицировано: 1-150 ppm, 5 ppm задержка цветения, 100 ppm макс. размер плода, серебряная бумага, 3 обработки через день (title_only в HortScience 1985 / препринт Research Square 2025)"
  - "См. полную карточку: [[Triacontanol]]"
crops:
  tomato: no_data
  cucumber: no_data
  strawberry: found_verified
aliases: ["1-Triacontanol", "Melissyl alcohol", "TRIA"]
aliases_ru: ["1-триаконтапол", "триаконтановый спирт", "мелиссиловый спирт"]
eppo_code: null
regulatory_status: null
consensus_score: null
toxicity_window: {}
phi_mrl: {}
---

# Triacontanol (TRIA) — Triacontanol

> ✅ Валидировано 2026-08-04 (пилот). Статус: `partial` / evidence: `moderate`.
> ⚠️ Эта карточка — вторая CSV-строка (266) того же вещества, что и [[Triacontanol]]. Полные данные — там.

## Идентичность
- **CAS:** 593-50-0 · **Формула:** C30H62O · **Молярная масса:** 438.8 г/моль (см. [[Triacontanol]])

## Применение (CSV)
| Категория | Действие | Дозировка/Способ | Ожидаемый результат | Эффективность | Культуры |
|---|---|---|---|---|---|
| GROWTH_REGULATION | Growth & ripening | Foliar 1-150 ppm; 50 µM на плоды; серебряная бумага; 3 обработки через день | Рост, размер/вес плодов, окраска/созревание; ABA↑, этилен↑, IAA↓ | MEDIUM | Strawberry, fruit crops |

## crop_evidence

### 🍓 Клубника (Fragaria × ananassa) — `found_verified`
- **50 µM на плоды (Sweet Charlie):** ускорение развития/созревания плодов, рост сахаров и антоцианов, активность стресс-связанных ферментов (PMID 32290080)
- **0.5 и 1 ppm фолиарно** (5 обработок, с 30-го дня): урожай +12.7% при 1 ppm (PMID 35893617)
- **Не верифицировано:** 5 ppm → задержка цветения/бутонизации; 100 ppm → макс. размер плода; серебряная бумага; 3 обработки через день (только title_only: HortScience 1985; препринт Research Square 2025)

### 🍅 Томат / 🥒 Огурец — `no_data`
Строка CSV 266 нацелена только на клубнику; данные по томату/огурцу — в карточке [[Triacontanol]] (расширение).

## ⚠️ Corrected Dosages (vs CSV)
| CSV Claim | Corrected | Condition | Source |
|-----------|-----------|-----------|--------|
| 50 µM для окраски плодов | ✅ Подтверждено | Плоды клубники, сорт Sweet Charlie | PMID 32290080 |
| 5 ppm → задержка цветения | Не верифицировано | — | — |
| 100 ppm → макс. размер плода | Не верифицировано | — | — |
| 1-150 ppm вегетативный рост | Частично: рабочие дозы 0.5-1 ppm | Полевые опыты | PMID 35893617 |

## ⚠️ Toxicity Window
ED50/TD50 — нет данных. PMID 32290080: «non-toxic, pollution-free, low-cost». Сверхвысокие дозы (5–100 ppm) могут давать фенологические сдвиги — не верифицировано.

## 📅 PHI и MRL
**Нет данных** (см. [[Triacontanol]]).

## Противоречия
1. Конкретные дозы строки 266 (1–150 ppm, 5/100 ppm эффекты, серебряная бумага) не подтверждены абстрактами (high)
2. «Promoted auxin and ABA, inhibited ethylene» — противоречит утверждению «ABA и этилен↑, IAA↓» в той же строке; в литературе: TRIA подавляет JA-индуцированную защиту (medium, PMID 15128037)

## Источники
- [PMID 32290080](https://pubmed.ncbi.nlm.nih.gov/32290080/) — 50 µM на плоды клубники (2020)
- [PMID 35893617](https://pubmed.ncbi.nlm.nih.gov/35893617/) — 0.5/1 ppm, +12.7% урожая (2022)
- Артефакт: [search_Triacontanol_2026-08-04.json](../../../raw/evidence/T/Triacontanol/search_Triacontanol_2026-08-04.json)