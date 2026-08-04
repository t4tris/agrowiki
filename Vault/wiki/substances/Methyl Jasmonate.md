---
type: substance
code: Methyl Jasmonate
name_en: MeJA
cas: "1211-29-6"
formula: C13H20O3
class: Jasmonate
class_family: jasmonates
mechanism: jasmonate_sar_defense
action_category: FOLIAR_APPLICATION
application_csv: Apply 100-500 ppm foliar spray; Fruit spray 230 µM
efficacy_csv: HIGH
validation_status: corrected
evidence_level: strong
last_checked: 2026-08-04
next_review: 2026-09-04
sources: ["PMID:31117506", "PMID:35887486", "PMID:42537888", "PMID:41404138", "PMID:41770901", "PMID:40545701", "PMID:41136943", "PMID:39859190", "PMID:35574100", "PMID:28981785", "PMID:32033119", "PMID:33879022", "PMID:41876383", "PMID:32457779", "PMID:28671619", "PMID:26212995", "PMID:32252456", "PMID:35691062", "PMID:35325290", "PMID:41136892", "PMID:41388739", "PMID:11158538", "PMID:35325290", "PMID:35293128", "PMID:29899259", "PMID:25046752", "PMID:32033119", "PMID:31117506"]
notes:
  - "Механизм подтверждён (JA-сигналинг MYC2/JAZ, прайминг защитных генов); название 'jasmonate_sar_defense' условно — путь JA-зависимый, строго не SAR (SA-зависимый)"
  - "CSV-доза 100-500 ppm выше литературных эффективных 5.6-112 ppm (25-500 µM); верхняя граница 500 ppm рискованна (подавление ассимиляции, длительное закрытие устьиц)"
  - "Контраиндикация (high): MeJA ПОВЫШАЕТ восприимчивость клубники к антракнозу Colletotrichum (гемибиотроф) — PMID 41388739"
  - "Летучесть: обработки вечером при T<25°C; плоды томата обрабатывать на свету (ликопин, PMID 41770901)"
  - "На 'Camarosa' фенотипического снижения серой гнили не отмечено (PMID 32252456) — сорт-зависимость"
  - "CSV-строка MeJA (Methyl Jasmonate) (FRUIT_MANAGEMENT, Fruit spray 230 µM ≈ 51.6 ppm) объединена в эту карточку 2026-08-04: доза входит в верифицированный диапазон 5.6-112 ppm; «shelf life» частично согласуется с постхарвест-эффектами (PMID 35691062) и снижением серой гнили (PMID 28671619)"
crops:
  tomato: found_verified
  cucumber: found_verified
  strawberry: found_verified
aliases: ["Methyl jasmonate", "Jasmonic acid methyl ester", "Methyl cis-jasmonate", "(-)-Methyl jasmonate", "MeJA", "MeJA (Methyl Jasmonate)"]
aliases_ru: ["метилжасмонат", "метиловый эфир жасмоновой кислоты"]
eppo_code: null
regulatory_status: null
consensus_score: null
toxicity_window: {}
phi_mrl: {}
---

# Methyl Jasmonate — Метилжасмонат (MeJA)

> ✅ Валидировано 2026-08-04 (Фаза 3, контракт v1.4). Статус: `corrected` / evidence: `strong`.
> ⚠️ CSV-дозы 100–500 ppm выше эффективных литературных (5.6–112 ppm); риск фитотоксичности на верхней границе.

## Идентичность
- **CAS:** 1211-29-6 (PubChem CID 5281929) · **Формула:** C13H20O3 · **Молярная масса:** 224.3 г/моль
- **Класс:** Jasmonate (летучий метиловый эфир жасмоновой кислоты); конверсия: 1 мМ ≈ 224 ppm

## Механизм действия
Летучий сигнальный эфир JA: проникает через устьица (PMID 32033119), индуцирует JA-сигналинг (MYC2/JAZ), H2O2 как вторичный мессенджер (PMID 11158538), прайминг защитных генов (хитиназы, β-1,3-глюканазы, PGIP — PMID 28671619, 32252456), фенольный метаболизм/PAL (PMID 31117506), терпенсинтазы FaTPS1/SlJIG (PMID 35325290, 35293128), антоцианы (PMID 29899259). Усиливает устойчивость к некротрофам (Botrytis) и насекомым, повышает холодо- и жаростойкость.

## Применение (CSV)
| Категория | Действие | Дозировка/Способ | Ожидаемый результат | Эффективность | Культуры |
|---|---|---|---|---|---|
| FOLIAR_APPLICATION | Defense signaling | Apply 100-500 ppm foliar spray | Enhanced herbivore and pathogen resistance; reduce gray mold after harvest; Promotes strawberry fruit maturation; Increase stress tolerance, reduces chilling injury | HIGH | All crops prone to pest damage |
| FRUIT_MANAGEMENT | Ripening & shelf-life | Fruit spray 230 µM | Prolonged strawberry shelf life; promotes maturation and stress tolerance | MEDIUM | Strawberry, fruits |

## crop_evidence

### 🍅 Томат (Solanum lycopersicum) — `found_verified` (9 claims)
- **Постхарвест плодов:** устойчивость к Botrytis cinerea через синергизм JA-этилен + фенольный метаболизм (PMID 31117506); Se в почву + фолиарный MeJA: серая гниль листьев 42.19% → 25.00%, витамин C +22.14% (PMID 35887486)
- **0.25 мМ (≈56 ppm)** снижает вес личинок Helicoverpa armigera; эффективнее 0.5 мМ BTH (PMID 42537888)
- **Ликопин:** на свету MeJA усиливает синтез (SlMYC2→SlPSY1); в темноте подавляет накопление (SlPIF1a) — обработка на свету (PMID 41770901); на breaker-стадии снижает эндогенные JA-Ile (−13%) и этилен (−33%) (PMID 41404138)
- **Холодостойкость:** SlMYB13→SlHSP17.7 через SlMYC2 (PMID 40545701)
- **Gap:** полевых испытаний доз в ppm (как в CSV 100–500 ppm) для томата не найдено

### 🥒 Огурец (Cucumis sativus) — `found_verified` (5 claims)
- **0.1/0.25/0.5 мМ (≈22–112 ppm):** слабое влияние на половую экспрессию и урожай (PMID 41136943)
- **Кадмиевый стресс:** MeJA вовлечён в H2S-облегчение: снижение ROS, восстановление роста (PMID 39859190)
- **Жаростойкость:** фолиарный MeJA восстанавливает при подавленном JA-пути (CsNPF4.4, PMID 35574100); CsZAT10 (индуцируется MeJA) — устойчивость к Bemisia tabaci через JA/SA/ROS (PMID 41876383)
- **Высокие дозы (0.2–50 мМ):** дозозависимая эмиссия стрессовых летучих; 50 мМ летален для листьев (PMID 28981785, 32033119, 33879022)
- **Gap:** работ по защите огурца от Botrytis с MeJA нет

### 🍓 Клубника (Fragaria × ananassa) — `found_verified` (9 claims)
- **Прехарвест 250 µM (≈56 ppm)** от цветения: M3-схема (цветение + крупная зелёная ягода) повышает проантоцианидины/фенолы (PMID 32457779)
- **Прехарвест MeJA/хитозан снижают серую гниль (Botrytis cinerea)** у F. chiloensis: ниже заболеваемость при хранении (PMID 28671619, 26212995); прайминг: FaMYC2, FaJAZ1, хитиназы, PGIP (PMID 32252456); FaTPS1 → эмиссия сесквитерпенов (PMID 35325290)
- **Постхарвест (16 ч 20°C, затем 3°C 12 дней):** рост фитохимикатов, антиоксидантов (PMID 35691062)
- **Бор-токсичность (cv. Albion):** 25–100 µM (5.6–22.4 ppm), оптимум 50 µM (PMID 41136892)
- **⚠️ Антракноз (Colletotrichum):** MeJA ПОВЫШАЕТ восприимчивость — гемибиотроф (PMID 41388739)
- **Gap:** доз 100–500 ppm (CSV) на клубнике не испытывали; сорт-зависимость ('Camarosa' — без эффекта на серую гниль)

## ⚠️ Corrected Dosages (vs CSV)
| CSV Claim | Corrected | Condition | Source |
|-----------|-----------|-----------|--------|
| 100-500 ppm foliar | Эффективный диапазон 5.6–112 ppm (25–500 µM); 500 ppm — риск фитотоксичности | Фолиарно, вечером, T<25°C | PMID 32457779, 41136892, 41136943 |
| reduce gray mold after harvest | Подтверждено (клубника прехарвест, F. chiloensis; томат постхарвест) | До уборки/на свету | PMID 28671619, 31117506 |
| Promotes strawberry maturation | Частично: MeJA — неактивное производное JA в ранних этапах созревания; эндогенные JAs снижаются к созреванию | — | PMID 25046752, 32457779 |

## ⚠️ Toxicity Window
ED50/TD50 не опубликованы. Ориентиры: 50 мМ (≈11.2 г/л) летален для листьев огурца (PMID 28981785); высокие дозы подавляют ассимиляцию и вызывают длительное закрытие устьиц (PMID 32033119); 100 µM на клубнике — слабые эффекты при сильном стрессе (PMID 41136892). Летучее соединение (испаряется при T>25°C).

## 📅 PHI и MRL
**Не применимы.** Природный растительный метаболит, не пестицид; MRL/PHI не установлены (регуляторные БД не проверялись — статус не подтверждён).

## Противоречия
1. **Доза 100–500 ppm** vs литература 5.6–112 ppm (medium, PMID 32457779, 41136892)
2. **«Reduce gray mold»** — на сорте 'Camarosa' фенотипического эффекта нет (low, PMID 32252456)
3. **«Promotes maturation»** — эндогенные MeJA/JMT снижаются по мере созревания клубники (low, PMID 25046752)

## Противопоказания
- **Антракноз клубники (Colletotrichum spp.):** MeJA повышает восприимчивость — не применять при гемибиотрофных патогенах (high, PMID 41388739)
- **Высокие дозы (≥100 µM клубника; ≥5 мМ огурец):** слабые/негативные эффекты, подавление ассимиляции (medium, PMID 41136892, 28981785)
- **Тёмное хранение плодов томата:** MeJA подавляет накопление ликопина (low, PMID 41770901)

## Источники
- [PMID 32457779](https://pubmed.ncbi.nlm.nih.gov/32457779/) — прехарвест 250 µM, клубника (2020)
- [PMID 28671619](https://pubmed.ncbi.nlm.nih.gov/28671619/) — MeJA/хитозан, Botrytis F. chiloensis (2017)
- [PMID 31117506](https://pubmed.ncbi.nlm.nih.gov/31117506/) — MeJA и Botrytis томата постхарвест (2019)
- [PMID 41388739](https://pubmed.ncbi.nlm.nih.gov/41388739/) — ⚠️ антракноз, повышенная восприимчивость (2026)
- [PMID 41770901](https://pubmed.ncbi.nlm.nih.gov/41770901/) — ликопин на свету/в темноте (2026)
- Артефакт: [search_MethylJasmonate_2026-08-04.json](../../../raw/evidence/M/Methyl%20Jasmonate/search_MethylJasmonate_2026-08-04.json)

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
