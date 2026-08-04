---
type: substance
code: GA3
name_en: Gibberellic Acid
cas: 77-06-5
formula: C19H22O6
class: Gibberellin
action_category: GROWTH_REGULATION
application_csv: Apply 25-200 ppm foliar; 100 mg/L best vegetative; 1.0 mM weekly ~13 runners; 200 mg/L + long photoperiod → flower abortion; 0.5 mM in citric buffer/DMSO to fruit
efficacy_csv: MEDIUM
validation_status: partial
evidence_level: moderate
last_checked: 2026-08-04
next_review: 2026-09-04
sources: ["PMID:40780106", "PMID:29288326", "PMID:33890635", "PMID:38337908", "PMID:41225064", "PMID:39260050", "PMID:28482334", "PMID:24470243", "PMID:11539775", "PMID:40866815", "PMID:36774421", "PMID:17503074", "PMID:33274492", "PMID:39119498", "PMID:29146357", "PMID:40957257", "PMID:41769268", "PMID:36092914", "PMID:37201922"]
notes:
  - "Механизм (усы/рост клубники через путь GA/DELLA) подтверждён 4 аннотациями (PMID 40780106, 29288326, 33890635, 38337908)"
  - "ВСЕ конкретные дозировки CSV (25-200 ppm, 100 mg/L, 1.0 mM ~13 усов, 200 mg/L + длинный день → абортация цветков, 0.5 mM цитратный буфер/DMSO) не найдены в PubMed/OpenAlex — unverified/inferred"
  - "Томат и огурец отсутствуют в Target_Crops CSV — данные по ним добавлены как расширение, не как валидация CSV"
  - "Europe PMC был недоступен в среде сабагента — рекомендован повторный поиск оркестратором"
crops:
  tomato: found_verified
  cucumber: found_verified
  strawberry: found_verified
aliases: ["Gibberellic Acid", "Gibberellin A3", "GA3"]
aliases_ru: ["Гибберелловая кислота", "Гиббереллин A3", "Гиббереллин X"]
eppo_code: null
regulatory_status: null
consensus_score: null
toxicity_window: {}
phi_mrl: {}
---

# GA3 — Gibberellic Acid

> ✅ Валидировано 2026-08-04 (пилот, контракт v1.2). Статус: `partial` / evidence: `moderate`.
> ⚠️ Механизм подтверждён, **дозировки CSV не подтверждены** ни одним источником.

## Идентичность
- **CAS:** 77-06-5 (подтверждён PubChem RegistryID, CID 6466)
- **Формула:** C19H22O6 · **Молярная масса:** 346.4 г/моль
- **Класс:** Gibberellin (дитерпеноидный фитогормон) — подтверждён

## Механизм действия
Гиббереллин A3 действует через GA-сигнальный путь: связывание GA → деградация DELLA-репрессоров (напр., FveRGA1 у клубники) → запуск ростовых программ; индуцирует гены биосинтеза GA (GA20ox). Ключевой гормон образования усов у земляники (PMID 40780106, 29288326, 33890635). У томата регулирует завязывание плодов (GA20ox1 при опылении, PMID 17503074) и удлинение клеток (гипокотиль огурца, PMID 37201922).

## Применение (CSV)
| Категория | Действие | Дозировка/Способ | Ожидаемый результат | Эффективность | Культуры |
|---|---|---|---|---|---|
| GROWTH_REGULATION | Vegetative growth | Apply 25-200 ppm foliar | Promoted vegetative growth and runner production; 100 mg/L best — 200 mg/L GA3 + long photoperiod: flower abortion, malformed fruits; 0.5 mM GA3 in citric buffer pH 4.5 + 2% DMSO to fruit; 1.0 mM GA3 weekly, 3rd week after transplanting → ~13 runners/plant | MEDIUM | Strawberry, fruit crops |

## crop_evidence

### 🍅 Томат (Solanum lycopersicum) — `found_verified` (расширение, не в CSV)
- **Фолиарно 25/50/75 мг/л при 14, 28 и 42 днях после высадки (до цветения):** 75 мг/л — лучший рост/урожай, тепличный жёлтый черри-томат (PMID 41225064, 2025)
- **1e-6 M (1 µM) фолиарно:** рост, особенно при засолении 100 мМ NaCl (PMID 39260050, 28482334)
- **Корневая аппликация 1.4 µM:** +40–50% фотосинтеза за 5 ч; 15 µM в питательном растворе — рост листовой площади (PMID 24470243, 11539775)
- **100 мг/л прайминг семян** — смягчение Hg-стресса (PMID 40866815); GA3 — лучший элиситор роста среди GA3/сорбиновая/6-BAP/IBA (PMID 36774421)
- **Завязывание плодов** — эндогенный GA через GA20ox1; партенокарпия связана с GA (PMID 17503074, 33274492, 39119498) — без экзогенных доз для полевого применения

### 🥒 Огурец (Cucumis sativus) — `found_verified` (расширение, не в CSV)
- **Партенокарпия:** экзогенный GA индуцирует бессемянные плоды на неопылённых завязях (PMID 40957257); GA4+7 100 мг/л на женские цветки за 1 день до антезиса — плоды как при опылении (**GA4+7, НЕ GA3** — дозу GA3 не подставлять!, PMID 29146357); CsGA20OX1 — позитивный регулятор партенокарпии (PMID 41769268)
- Эндогенный GA выше у партенокарпических генотипов (PMID 36092914)
- **Удлинение клеток** гипокотиля через CsPhyB-CsPIF3-CsGA20ox-2-DELLA (PMID 37201922)
- Полевых испытаний GA3 на огурце в PubMed не найдено

### 🍓 Клубника (Fragaria × ananassa) — `found_verified` (механизм)
- **Образование усов:** экзогенный GA3 индуцирует усы у неусатой Fragaria vesca (PMID 40780106, 33890635); GAs ускоряют деградацию DELLA (FveRGA1) → усы (PMID 29288326); фотопериод vs GA-путь — трейд-офф цветение/усы (PMID 38337908)
- **Дозировки CSV (25-200 ppm, 100 мг/л, 1.0 мМ ~13 усов/растение, 200 мг/л + длинный день → абортация цветков, 0.5 мМ буфер/DMSO) — НЕ подтверждены** ни одним источником (PubMed 0 результатов; классические работы Thompson & Guttridge 1959, HortScience 1996 — только title_only)

## ⚠️ Corrected Dosages (vs CSV)
| CSV Claim | Corrected | Condition | Source |
|-----------|-----------|-----------|--------|
| 25-200 ppm foliar (клубника) | Не подтверждено; ближайшая валидная доза для томата 25-75 мг/л | Вегетация, до цветения, томат | PMID 41225064 |
| 100 mg/L — «best vegetative» | Не подтверждено для клубники; 100 мг/л валидно как прайминг томата при стрессе | — | PMID 40866815 |
| 1.0 mM weekly → ~13 усов/растение | Не найдено в литературе (346 ppm) | — | — |
| 200 mg/L + длинный день → абортация цветков | Не верифицировано (0 результатов PubMed) | длинный фотопериод | — |
| 0.5 mM цитратный буфер pH 4.5 + 2% DMSO на плоды | Не подтверждено; протокол нетипичен для клубники | — | — |

## ⚠️ Toxicity Window
ED50/TD50/терапевтический индекс — **нет данных** в прочитанной литературе (GA3 — PGR, не пестицид; токсикологических дозо-зависимых исследований не найдено). Риск-заявление CSV (200 мг/л + длинный день) не верифицировано.

## 📅 PHI и MRL
**Нет данных.** PHI/MRL не найдены в прочитанной литературе; регуляторная оценка остатков не проводилась (null по правилам честности). Для экспортных культур требуется проверка EU Pesticides Database вне PubMed.

## Противоречия
1. **Target_Crops CSV** = «Strawberry, fruit crops» — томат/огурец не входят; данные по ним — расширение, не валидация CSV (medium)
2. **Механизм CSV «cell elongation/flowering»**: удлинение клеток подтверждено (огурец PMID 37201922, рост томата); «flowering» — лишь косвенно (medium)
3. **100 мг/л «best vegetative»** — подтверждения для клубники нет (medium)
4. **Партенокарпия огурца** подтверждена GA4+7, не GA3 (low — не подставлять дозы)
5. **0.5 мМ буфер/DMSO и 1.0 мМ weekly** — не прослеживаются ни до одной публикации (high, inferred)
6. Europe PMC недоступен (сетевой блок) — рекомендован повторный запуск оркестратором (low)

## Источники
- [PMID 40780106](https://pubmed.ncbi.nlm.nih.gov/40780106/) — GA и усы F. vesca (2025)
- [PMID 29288326](https://pubmed.ncbi.nlm.nih.gov/29288326/) — DELLA FveRGA1 и усы (2018)
- [PMID 33890635](https://pubmed.ncbi.nlm.nih.gov/33890635/) — GA индуцирует усы (2021)
- [PMID 38337908](https://pubmed.ncbi.nlm.nih.gov/38337908/) — фотопериод/GA трейд-офф (2024)
- [PMID 41225064](https://pubmed.ncbi.nlm.nih.gov/41225064/) — GA3 25-75 мг/л томат (2025)
- [PMID 39260050](https://pubmed.ncbi.nlm.nih.gov/39260050/) — GA3 1 µM при засолении (2024)
- [PMID 17503074](https://pubmed.ncbi.nlm.nih.gov/17503074/) — GA20ox1 и завязывание плодов томата (2007)
- [PMID 29146357](https://pubmed.ncbi.nlm.nih.gov/29146357/) — GA4+7 партенокарпия огурца (2018)
- Артефакт: [[raw/evidence/G/GA3/search_GA3_2026-08-04.json]]