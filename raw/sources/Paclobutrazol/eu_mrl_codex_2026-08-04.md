# EU MRL & Codex — Paclobutrazol (источник-клип)

Дата сбора: 2026-08-04 (браузер Playwright, EU Pesticides Database v3.4 + Codex Pesticide DB)

## Статус одобрения ЕС (EUPD → Active substances)
- **Paclobutrazol — Approved** (одобрено)
- **Expiry of Approval: 31/01/2029**
- URL: https://ec.europa.eu/food/plant/pesticides/eu-pesticides-database/start/screen/active-substances

## MRL EU (EUPD → MRLs → Paclobutrazol (sum of constituent isomers))
URL: https://ec.europa.eu/food/plant/pesticides/eu-pesticides-database/start/screen/mrls/details?lg_code=EN&pest_res_id_list=349&product_id_list=

Фокусные культуры (mg/kg; `*` = предел определения LOD):

| Продукт | Действующий Annex II Reg. (EU) 2023/1719 | Предыдущий Reg. (EU) 2019/89 | Старый Reg. (EC) 149/2008 |
|---|---|---|---|
| Tomatoes (0231010) | **0.01*** | 0.01* | 0.02* |
| Cucumbers (0232010) | **0.01*** | 0.01* | 0.02* |
| Strawberries (0152000) | **0.01*** | 0.01* | 0.5 |
| Pome fruits (0130000) / Apples | 0.05 | 0.05 | 0.5 |
| Peaches | 0.15 | 0.15 | 0.5 |
| Citrus fruits | 0.01* | 0.01* | 0.5 |
| Grapes | 0.01* | 0.01* | 0.05 |

Примечание: звёздочка (`*`) в EUPD означает «предел определения» (LOD) — фактически MRL на уровне
обнаружения; применение с остатками выше LOD на этих культурах не предусмотрено.

## Codex (FAO/WHO Codex Pesticide Database)
- **Paclobutrazol отсутствует в списке пестицидов Codex (240 записей)** → **Codex MRL не установлены**
- API-источник: https://www.fao.org/jsoncodexpest/jsonrequest/pesticides/index.html (ID не найден)
- URL: https://www.fao.org/fao-who-codexalimentarius/codex-texts/dbs/pestres/pesticides/en/

## PHI (Pre-Harvest Interval)
- На уровне ЕС PHI не устанавливается централизованно (национальные авторизации государств-членов)
- Для практики: уточнять в национальном реестре СЗР страны применения

## Вывод для карточки
- MRL_EU (томат/огурец/клубника): **0.01 mg/kg (LOD)**, Reg. (EU) 2023/1719
- MRL_Codex: **не установлен**
- Статус ЕС: Approved до 31.01.2029
- PHI: не установлен на уровне ЕС (национальные авторизации)
