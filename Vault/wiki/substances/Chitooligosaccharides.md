---
type: substance
code: Chitooligosaccharides
name_en: Chitooligosaccharides (COS/CHOS)
cas: 
formula: 
class: Biostimulant
action_category: FOLIAR_APPLICATION
application_csv: 
efficacy_csv: MEDIUM
validation_status: partial
evidence_level: strong
last_checked: 2026-08-04
next_review: 2026-09-04
sources: ["PMID:37047175", "PMID:24770723", "PMID:27095400", "PMID:32814103", "PMID:32429524"]
notes:
  - "COS/CHOS — олигомеры хитозана (DPn 2-40); данные собраны в рамках пилотной валидации [[Chitosan]] (один отчёт на оба CSV-кода)"
  - "Огурец — подтверждено: 50 мг/л COS лучшая обработка при холодовом стрессе (PMID 37047175); CHOS DPn 15-40 — наибольшая антифунгальная активность против B. cinerea (PMID 24770723)"
  - "Томат — подтверждено: COS-OGA против мучнистой росы Leveillula taurica (PMID 27095400)"
  - "Клубника — прямых исследований COS отдельно не найдено (данные по хитозану в целом: [[Chitosan]])"
  - "CAS не установлен (олигомерная смесь); отдельная PubChem-запись по имени 'Chitosan oligosaccharide' → 404"
crops:
  tomato: found_verified
  cucumber: found_verified
  strawberry: no_data
aliases: ["COS", "CHOS", "Chitooligosaccharides", "Chitosan oligosaccharide"]
aliases_ru: ["хитозан-олигосахариды", "олигомеры хитозана"]
eppo_code: null
regulatory_status: null
consensus_score: null
toxicity_window: {}
phi_mrl: {}
---

# Chitooligosaccharides — Хитозан-олигосахариды (COS/CHOS)

> ✅ Валидировано 2026-08-04 (пилот, в составе отчёта [[Chitosan]]). Статус: `partial` / evidence: `strong`.
> Олигомеры хитозана (степень полимеризации 2–40) — водорастворимая форма хитозана с более высокой биодоступностью.

## Идентичность
- **CAS:** не установлен (олигомерная смесь; запись PubChem «Chitosan oligosaccharide» → 404)
- **Класс:** Biostimulant — олигосахариды (β-1,4-связанные D-глюкозамин), продукты гидролиза хитозана
- Полные данные по полимерной форме: [[Chitosan]]

## Механизм действия
Элиситор/defence priming как и хитозан (SA/JA-пути, PR-белки, каллоза/лигнин); антифунгальная активность зависит от DPn — максимум при DPn 15–40 (PMID 24770723); синергия с низкими дозами синтетических фунгицидов.

## crop_evidence

### 🥒 Огурец (Cucumis sativus) — `found_verified`
- **COS 50 мг/л (50 ppm)** — лучшая обработка против холодового стресса проростков: рост, хлорофилл, фотосинтез, осмолиты, антиоксиданты (сравнение с глицин-бетаином и хитозаном; транскриптомный анализ, JA-биосинтез) (PMID 37047175)
- **CHOS (DPn 15–40)** — наибольшая антифунгальная активность против B. cinerea in vitro и in vivo; синергия с низкими дозами фунгицидов (PMID 24770723)

### 🍅 Томат (Solanum lycopersicum) — `found_verified`
- **COS-OGA** (хитозан-олигомеры + пектин-олигомеры), повторные опрыскивания: защита тепличного томата от мучнистой росы Leveillula taurica; SA-зависимый SAR, кумулятивный эффект (PMID 27095400)

### 🍓 Клубника (Fragaria × ananassa) — `no_data`
Прямых исследований COS на клубнике в пуле пилота не найдено; данные по полимерному хитозану на клубнике — см. [[Chitosan]].

## ⚠️ Corrected Dosages (vs CSV)
| CSV Claim | Corrected | Condition | Source |
|-----------|-----------|-----------|--------|
| (нет явной дозы в CSV) | 50 мг/л COS — оптимум при холодовом стрессе | Огурец, проростки | PMID 37047175 |
| (нет явной дозы в CSV) | CHOS DPn 15–40 — максимум антифунгальной активности | B. cinerea | PMID 24770723 |

## ⚠️ Toxicity Window
ED50/TD50 — нет данных. COS — пищевые олигосахариды; токсикологических порогов в выборке нет.

## 📅 PHI и MRL
**Нет данных** (см. [[Chitosan]]).

## Противоречия
Формальных conflicts = 0. CSV-строка для COS (заделка в почву 1–5 кг/га → микробная активность) не подтверждена аннотациями — см. [[Chitosan]].

## Источники
- [PMID 37047175](https://pubmed.ncbi.nlm.nih.gov/37047175/) — COS 50 мг/л, холодовой стресс огурца (2023)
- [PMID 24770723](https://pubmed.ncbi.nlm.nih.gov/24770723/) — CHOS DPn 15-40 против B. cinerea (2014)
- [PMID 27095400](https://pubmed.ncbi.nlm.nih.gov/27095400/) — COS-OGA, мучнистая роса томата (2016)
- Артефакт: [search_Chitosan_2026-08-04.json](../../../raw/evidence/C/Chitosan/search_Chitosan_2026-08-04.json)