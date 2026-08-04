---
type: substance
code: Paclobutrazol
name_en: Paclobutrazol
cas: "76738-62-0"
formula: C15H20ClN3O
class: Triazole
class_family: synthetic_growth_regulators
mechanism: gibberellin_action
action_category: GROWTH_REGULATION
application_csv: Apply 0.25-2 g/L soil drench, 75-300mg/l sprayed 35 days after planting.
efficacy_csv: HIGH
validation_status: partial
evidence_level: strong
last_checked: 2026-08-04
next_review: 2026-09-04
sources: ["PMID:41225862", "PMID:35161406", "PMID:41834248", "PMID:37895095", "PMID:31884369", "PMID:27936707", "PMID:37084381", "PMID:40780106", "PMID:33890635", "PMID:22791823", "PMID:31755653", "PMID:36466575"]
notes:
  - "Taxonomy correction (v1.4): class_family изменён 'fungicides' → 'synthetic_growth_regulators' (триазольный ретардант, ингибитор биосинтеза GA; применение — регуляция роста, не фунгицидное); mechanism gibberellin_action подтверждён"
  - "CSV-дозировки (soil drench 0.25-2 г/л; 75-300 мг/л на 35-й день) для фокусных культур не верифицированы; верхняя граница 300 мг/л превышает подтверждённый диапазон 25-200 мг/л"
  - "Остаточность в почве 'до 3 лет' источниками не подтверждена; T1/2 изомеров 9.24/16.6 сут (огурец, засолка, PMID 31884369)"
crops:
  tomato: found_verified
  cucumber: found_verified
  strawberry: found_verified
aliases: ["PBZ", "Paclobutrazol", "(2RS,3RS)-1-(4-chlorophenyl)-4,4-dimethyl-2-(1H-1,2,4-triazol-1-yl)pentan-3-ol"]
aliases_ru: ["паклобутразол"]
eppo_code: null
regulatory_status: null
consensus_score: null
toxicity_window:
  soil_persistence: "T1/2 изомеров PBZ 9.24 и 16.6 сут при засолке огурцов (PMID 31884369); остатки PBZ обнаруживаются в плодах (PMID 31755653, 27936707)"
phi_mrl: {}
---

# Paclobutrazol — Паклобутразол

> ✅ Валидировано 2026-08-04 (Фаза 3, контракт v1.4). Статус: `partial` / evidence: `strong`.
> ⚠️ Механизм подтверждён; **CSV-дозировки не верифицированы**, верхняя граница 300 мг/л рискованна.

## Идентичность
- **CAS:** 76738-62-0 · **Формула:** C15H20ClN3O · **Молярная масса:** 293.79 г/моль
- **Класс:** Triazole (триазольный ретардант; **не** фунгицид по применению — correction taxonomy v1.4)

## Механизм действия
Ингибитор биосинтеза гиббереллинов: блокирует энт-кауреноксидазу (цитохром P450) → снижение GA → компактный рост, подавление вытягивания. Действие через GA-путь подтверждено: подавление биосинтеза GA (PMID 41834248, 37084381, 33890635, 41225862). Снижает вытягивание эпикотиля и размеры, усиливает хлорофилл.

## Применение (CSV)
| Категория | Действие | Дозировка/Способ | Ожидаемый результат | Эффективность | Культуры |
|---|---|---|---|---|---|
| GROWTH_REGULATION | Height control | Apply 0.25-2 g/L soil drench, 75-300mg/l sprayed 35 days after planting | Retardant, delay flower development, reduce flower size, reduce vegetative growth, reducing runner development, enhance photosynthetic capability of strawberry | HIGH | Cereals, ornamentals, fruit trees |

## crop_evidence

### 🍅 Томат (Solanum lycopersicum) — `found_verified`
- **200 мг/л (200 ppm) фолиарно** на стадии двух настоящих листьев: значимое уменьшение длины эпикотиля и размера растений (PMID 41225862)
- **25–100 мг/л фолиарно (теплица):** улучшение качества рассады, устойчивость к Alternaria solani, рост хлорофилла (PMID 35161406)
- **Регенерация побегов (cut-budding)** усилена (PMID 41834248); снижение уровня салициловой кислоты в опытах по индукции устойчивости (PMID 37895095)
- **Gap:** полива в почву (soil drench 0.25–2 г/л) и применения на 35-й день после посадки для томата не найдено

### 🥒 Огурец (Cucumis sativus) — `found_verified`
- **Остатки PBZ при засолке:** энантиоселективная деградация, T1/2 изомеров 9.24/16.6 сут, влияние на микробное сообщество засолки (PMID 31884369)
- **Мобильность:** основная часть остатков концентрируется в кожуре (отношение пульпа/кожура < 0.8) (PMID 27936707)
- **Молекулярный механизм:** ген CsPRE4 (PACLOBUTRAZOL-RESISTANCE4) регулирует растяжение клеток и удлинение усиков; GA действует ниже по каскаду (PMID 37084381)
- **Gap:** агрономических дозировок PBZ для огурца (ретардантный эффект, схемы) в выборке нет

### 🍓 Клубника (Fragaria × ananassa) — `found_verified`
- **PBZ предотвращает образование усов и увеличивает число коронок** у лесной земляники Fragaria vesca (PMID 40780106, 33890635)
- **PBZ и GA3 не оказали значимого влияния** на созревание земляники (неклим. тип, PMID 22791823)
- **Остатки PGR в плодах:** 15.6% образцов (n=96) содержали PGR, включая паклобутразол (PMID 31755653)
- **Обзор:** PGR (PBZ, GA, NAA, триаконтанол, хлормекват) — ключевая роль в росте и урожайности земляники (PMID 36466575)
- **Gap:** данных о «повышении фотосинтетической способности» именно клубники PBZ нет; дозировки для клубники в проверенных аннотациях не указаны

## ⚠️ Corrected Dosages (vs CSV)
| CSV Claim | Corrected | Condition | Source |
|-----------|-----------|-----------|--------|
| 75–300 мг/л опрыскивание на 35-й день | Подтверждённый рабочий диапазон 25–200 мг/л; 300 мг/л превышает | Томат, вегетация/рассада | PMID 35161406, 41225862 |
| 0.25–2 г/л soil drench | Не верифицировано для томата/огурца/клубники | — | — |
| «Повышение фотосинтеза клубники» | Не подтверждено прямыми исследованиями | — | — |

## ⚠️ Toxicity Window
ED50/TD50/терапевтический индекс — нет данных (не выдумывать). Ориентиры: фитотоксичность при 300 мг/л документально не подтверждена, но выходит за верифицированный диапазон; персистентность: T1/2 9–17 сут (огурец, засолка), остатки в кожуре плодов; «до 3 лет в почве» (CSV) не подтверждено.

## 📅 PHI и MRL
**Нет данных.** PHI/MRL не извлечены (EU Pesticides Database / Codex не опрашивались); отмечено обнаружение остатков PGR в плодах (PMID 31755653).

## Противоречия
1. **Доза 75–300 мг/л** vs литература 25–200 мг/л (medium, PMID 35161406, 41225862)
2. **«Delay flower development / reduce flower size»** — у клубники значимого эффекта на репродуктивные процессы не было (low, PMID 22791823)
3. **Target_Crops CSV** = cereals/ornamentals/fruit trees, но для всех 3 фокусных культур найдена подтверждающая литература; CSV-дозы именно для них не проверены (low)

## Противопоказания
- **Вегетативное размножение клубники усами:** PBZ подавляет образование усов и конвертирует усы в коронки — не применять на маточниках (medium, PMID 40780106, 33890635)
- **Переработка огурцов (ферментация/засолка):** остатки PBZ нарушают микробное сообщество засолки (medium, PMID 31884369)
- **Потребление плодов с остатками:** остатки концентрируются в кожуре; очистка снижает нагрузку (low, PMID 27936707, 31755653)

## Источники
- [PMID 35161406](https://pubmed.ncbi.nlm.nih.gov/35161406/) — 25–100 мг/л, рассада томата, Alternaria (2022)
- [PMID 41225862](https://pubmed.ncbi.nlm.nih.gov/41225862/) — 200 мг/л, эпикотиль томата (2026)
- [PMID 31884369](https://pubmed.ncbi.nlm.nih.gov/31884369/) — T1/2 PBZ при засолке огурцов (2019)
- [PMID 40780106](https://pubmed.ncbi.nlm.nih.gov/40780106/) — PBZ и усы/коронки Fragaria vesca (2025)
- [PMID 33890635](https://pubmed.ncbi.nlm.nih.gov/33890635/) — конверсия усов в коронки (2021)
- Артефакт: [search_Paclobutrazol_2026-08-04.json](../../../raw/evidence/P/Paclobutrazol/search_Paclobutrazol_2026-08-04.json)

# Paclobutrazol — Paclobutrazol

> ⚠️ Черновик из CSV. Статус: `unverified`. Валидация по культурам (томат/огурец/клубника) — впереди.

## Идентичность
<!-- CAS, формула, класс — проверить через PubChem -->

## Механизм действия
GA inhibitor

## Применение (CSV)
| Категория | Действие | Дозировка/Способ | Ожидаемый результат | Эффективность | Культуры |
|---|---|---|---|---|---|
| GROWTH_REGULATION | Height control | Apply 0.25-2 g/L soil drench, 75-300mg/l sprayed 35 days after planting. | retardant delay flower development and reduce flower size and reduces vegetative growth. reducing runner development. enhance the photosynthetic capability of strawberry. | HIGH | Cereals, ornamentals, fruit trees |

## crop_evidence
<!-- После валидации: дозировки и эффекты по каждой культуре с PMID/DOI -->

### 🍅 Томат (Solanum lycopersicum)
<!-- нет данных по культуре -->

### 🥒 Огурец (Cucumis sativus)
<!-- нет данных по культуре -->

### 🍓 Клубника (Fragaria × ananassa)
<!-- нет данных по культуре -->

## ⚠️ Corrected Dosages (vs CSV)
| CSV Claim | Corrected | Condition | Source |
|-----------|-----------|-----------|--------|

## ⚠️ Toxicity Window
<!-- ED50/TD50/therapeutic index/стойкость в почве — только из литературы -->

## 📅 PHI и MRL
<!-- PHI, MRL EU/USA/Codex; для HIGH-efficacy обязательно -->

## Противоречия
<!-- CSV vs литература, severity -->

## Источники
<!-- PMID / DOI / URL -->
