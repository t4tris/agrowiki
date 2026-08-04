---
type: substance
code: Artemisinin
name_en: Artemisinin
cas: 63968-64-9
formula: C15H22O5
class: Sesquiterpene lactone
class_family: terpenoids_saponins_lipids
mechanism: antioxidant_defense
action_category: FOLIAR_APPLICATION, SOIL_APPLICATION
application_csv: Apply 0.1-1 g/kg soil amendment; 50-200 mg/L foliar spray
efficacy_csv: MEDIUM
validation_status: insufficient_data
evidence_level: weak
last_checked: 2026-08-04
next_review: 2026-09-04
sources: ["PMID:35344268", "PMID:25658194", "PMID:36122740", "PMID:35908798", "PMID:29727708", "PMID:20815879", "PMID:36805532", "PMID:35720574"]
notes:
  - "По всем трём культурам (томат, огурец, клубника) прямых исследований применения артемизинина НЕ найдено: PubMed 0/0/0 по прямым запросам"
  - "CSV-заявка «снижение галлов M. incognita на томате до 70% при 0.1-1 г/кг» НЕ подтверждается: ближайшая работа (PMID 35344268) — нематицидность РОДСТВЕННЫХ кислот A. annua (артемизининовая/дигидроартемизининовая), не самого артемизинина; цифра 70% нигде не встречается"
  - "CSV-заявка «SOD/POD при тепловом стрессе» НЕ подтверждена: в растительной литературе артемизинин — фитотоксичный стрессор (PMID 25658194); рост SOD/POD — только защитный ответ у ржи (PMID 36122740), у ячменя SOD снижалась (PMID 35908798)"
  - "2 нерелевантных PMID по огурцу и 1 ложный по клубнике (вкус таблетки артеметер-люмефантрина)"
  - "Рекомендация: пометить обе CSV-строки как неподтверждённые; верификация невозможна без полевых исследований на целевых культурах"
crops:
  tomato: no_data
  cucumber: no_data
  strawberry: no_data
aliases: ["Artemisinin", "Qinghaosu", "Arteannuin"]
aliases_ru: ["артемизинин", "цинхаосу (Qinghaosu)", "артеаннуин (Arteannuin)"]
eppo_code: null
regulatory_status: null
consensus_score: null
toxicity_window: {}
phi_mrl: {}
---

# Artemisinin — Artemisinin

> ✅ Валидировано 2026-08-04 (пилот, контракт v1.2). Статус: `insufficient_data` / evidence: `weak`.
> ⚠️ **Обе CSV-заявки не подтверждены литературой** ни для одной из трёх культур. Артемизинин в растительном контексте — фитотоксичный аллелохимикат.

## Идентичность
- **CAS:** 63968-64-9 (основной; связанная запись 63968-63-9; UNII 9RMU91N5K2, EC 700-290-5), **CID 68827**
- **Формула:** C15H22O5 · **Молярная масса:** 282.33 г/моль
- **Класс:** Sesquiterpene lactone (сесквитерпеновый лактон с эндопероксидным мостиком 1,2,4-триоксан)

## Механизм действия
Для растений документирован как **фитотоксичный аллелохимикат**: ингибирование роста, ROS-оверпродукция, перекисное окисление липидов, остановка митоза и гибель клеток корневых кончиков (PMID 25658194, салат). Нематицидная активность показана для **родственных кислот** артемизининовой и дигидроартемизининовой (НЕ самого артемизинина): EC50/48ч 0.37/0.76 мМ против J2 Meloidogyne incognita (PMID 35344268). **Не элиситор антиоксидантной системы** в понимании CSV.

## Применение (CSV)
| Категория | Действие | Дозировка/Способ | Ожидаемый результат | Эффективность | Культуры |
|---|---|---|---|---|---|
| SOIL_APPLICATION | — | Apply 0.1-1 g/kg soil amendment | Reduced root-knot nematode galling by up to 70% | MEDIUM | Tomato, root-knot nematode-prone crops |
| FOLIAR_APPLICATION | — | Apply 50-200 mg/L foliar spray | Increased SOD and POD activity under heat stress | MEDIUM | All crops |

## crop_evidence

### 🍅 Томат (Solanum lycopersicum) — `no_data`
- PubMed: 0 результатов по всем прямым запросам ('artemisinin tomato root-knot nematode', 'artemisinin tomato Meloidogyne', 'artemisinin tomato heat stress SOD POD')
- Fallback 'artemisinin Meloidogyne' → 2 PMID, оба нерелевантны для томата: PMID 35344268 (кислоты A. annua, культура-хозяин не указана), PMID 29727708 (гельминтозы животных, title_only)
- 'artemisinin Solanum' → 8 PMID, все ложные совпадения (гетерологичный биосинтез могрозидов, трихомы, антималярийные Solanum spp.)
- **CSV-заявка (снижение галлов до 70% при 0.1–1 г/кг) — НЕ подтверждена**: цифра 70% отсутствует во всей литературе; 0.1 г/кг = 100 мг/кг ≈ 100 ppm, 1 г/кг = 1000 ppm

### 🥒 Огурец (Cucumis sativus) — `no_data`
- 'artemisinin cucumber' → 2 PMID, оба НЕ про применение артемизинина на огурце: PMID 36805532 (гетерологичный биосинтез могрозидов, артемизинин лишь в аффилиации автора), PMID 35720574 (обзор трихом A. annua)
- Данных о дозировках/эффектах нет; culture_mentioned=true только формально

### 🍓 Клубника (Fragaria × ananassa) — `no_data`
- Единственный PMID (20815879) — **ложное совпадение**: клиническое исследование вкусовой привлекательности таблеток артеметер-люмефантрина (клубничный ароматизатор) у добровольцев
- Fallback 'artemisinin Fragaria' → 0 PMID. Данных нет.

## ⚠️ Corrected Dosages (vs CSV)
| CSV Claim | Corrected | Condition | Source |
|-----------|-----------|-----------|--------|
| 0.1-1 g/kg почва → галлы M. incognita −70% | Не подтверждено; EC50 0.37/0.76 мМ показан для **кислот A. annua**, не артемизинина | J2 M. incognita, in vitro, культура не указана | PMID 35344268 |
| 50-200 mg/L фолиарно → SOD/POD при тепловом стрессе | Не подтверждено; у ячменя при смягчении стресса SOD **снижалась** (20 мг/л, гидропоника, соль+freeze-thaw) | Ячмень, не целевые культуры | PMID 35908798 |

## ⚠️ Toxicity Window
Числовых ED50/TD50 для растений нет. Фоновые ориентиры (НЕ для ED50_ppm): EC50/48ч 0.37 мМ ≈ 87 мг/л артемизининовой кислоты против J2 M. incognita (PMID 35344268); 20 мг/л артемизинина в гидропонике смягчал стресс ячменя (PMID 35908798). Почвенная персистентность не изучена. **Артемизинин фитотоксичен** (ROS, ингибирование роста — PMID 25658194, 36122740).

## 📅 PHI и MRL
**Нет данных.** Артемизинин не зарегистрирован как пестицидное действующее вещество для пищевых культур; PHI/MRL не установлены. Требуется отдельная проверка регуляторных баз (EU Pesticides Database, US EPA, Codex).

## Противоречия
Формальных conflicts = 0, но **обе CSV-заявки неподтверждённые** (insufficient_data):
1. Нематицидная заявка: вещество в литературе — кислоты-предшественники, не артемизинин; цифра 70% отсутствует (high)
2. SOD/POD при тепловом стрессе: противоречит направленности эффекта (фитотоксичность, а у ячменя SOD снижалась) (high)

## Источники
- [PMID 35344268](https://pubmed.ncbi.nlm.nih.gov/35344268/) — нематицидность кислот A. annua против M. incognita (2022)
- [PMID 25658194](https://pubmed.ncbi.nlm.nih.gov/25658194/) — фитотоксичность артемизинина, ROS (2015)
- [PMID 36122740](https://pubmed.ncbi.nlm.nih.gov/36122740/) — стресс ржи, рост SOD/CAT/POD как стресс-ответ (2022)
- [PMID 35908798](https://pubmed.ncbi.nlm.nih.gov/35908798/) — 20 мг/л, ячмень, SOD снижалась (2022)
- [PMID 36805532](https://pubmed.ncbi.nlm.nih.gov/36805532/) — могрозиды в огурце, нерелевантно (2023)
- [PMID 20815879](https://pubmed.ncbi.nlm.nih.gov/20815879/) — ложное совпадение «strawberry» (2010)
- Артефакт: [search_Artemisinin_2026-08-04.json](../../../raw/evidence/A/Artemisinin/search_Artemisinin_2026-08-04.json)