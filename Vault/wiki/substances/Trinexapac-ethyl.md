---
type: substance
code: Trinexapac-ethyl
name_en: Trinexapac
cas: "95266-40-3"
formula: C13H16O5
class: Acylcyclohexanedione
class_family: synthetic_growth_regulators
mechanism: gibberellin_action
action_category: GROWTH_REGULATION
efficacy_csv: HIGH
validation_status: partial
evidence_level: weak
last_checked: 2026-08-06
next_review: 2026-11-06
notes: []
crops:
  tomato: found_unverified
  cucumber: no_data
  strawberry: no_data
aliases: ["Trinexapac-ethyl", "Cimectacarb", "Moddus", "Primo", "Primo Maxx", "PALISADE", "CGA-163935"]
aliases_ru: ["Тринексапак-этил"]
---

# Trinexapac-ethyl — Trinexapac

## Идентичность
- **CAS:** 95266-40-3 (CID 92421)
- **Формула:** C13H16O5 · **Молярная масса:** 252.26 г/моль
- **Класс:** Acylcyclohexanedione (синтетический ретардант)

## Механизм действия
Ингибитор биосинтеза гиббереллинов: подавляет 2-оксоглутарат/Fe(II)-зависимые диоксигеназы (GA20-оксидазу и GA3-оксидазу), снижая уровень активных GA и контролируя удлинение междоузлий (PMID 15012200, 34608958).

## Научные данные по культурам

Литература охватывает методы: полевая фолиарная обработка (томат).

### 🍅 Томат (Solanum lycopersicum)
- **Контроль роста:** фолиарная обработка trinexapac-ethyl сокращает размер растения индетерминантного томата (cv. Debora Plus), уменьшая расстояние между узлами и кистями, и увеличивает диаметр стебля (OpenAlex W1790097572, Figueiredo et al. 2015)
- **Обратная сторона дозы:** при возрастании дозы ET снижается продуктивность, средняя масса плода и доля крупных/средних плодов; растёт доля мелких плодов (OpenAlex W1790097572, Figueiredo et al. 2015)
- **Нет данных** о верифицируемых PMID/DOI-работах; единственная полевая работа (Figueiredo 2015) не имеет DOI/PMID, но реально прочитана (`verified: true`)

### 🥒 Огурец (Cucumis sativus)
- **Нет данных** о применении trinexapac-ethyl на огурце; найденные работы по огурцу относятся к другим ПГР (Prohexadione, Ethephon)

### 🍓 Клубника (Fragaria × ananassa)
- **Нет данных** о применении trinexapac-ethyl на клубнике

## ⚠️ Валидация CSV-заявок
| CSV-заявка | Вердикт | Уточнение | Условия | Severity | Источники |
|---|---|---|---|---|---|
| Доза: 100–400 ppm foliar spray | ⚪ Нет данных | Конкретный диапазон 100–400 ppm в работе Figueiredo 2015 не указан (только «возрастающие дозы ET») | — | — | OpenAlex W1790097572 |
| Эффект: controlled internode length | ⚠️ Частично | Подтверждено полевым опытом на томате (cv. Debora Plus): сокращение расстояния между узлами и кистями, увеличение диаметра стебля; при возрастании дозы — снижение продуктивности и массы плодов | Томат, фолиарная обработка | medium | OpenAlex W1790097572 |

## ⚠️ Toxicity Window
**Нет данных.** (Остатки trinexapac acid наблюдались на листьях риса до 15 дней после опрыскивания; в зерне ниже LOQ — PMID 39633074.)

## 📅 PHI и MRL
**Нет данных.** (Регистрация как ПГР подтверждена EFSA peer review — PMID 37389027, 32625868.)

## Источники
- [PMID 15012200](https://pubmed.ncbi.nlm.nih.gov/15012200/) — механизм GA-ингибирования (ретарданты)
- [PMID 34608958](https://pubmed.ncbi.nlm.nih.gov/34608958/) — ингибирование GA-биосинтеза
- [PMID 37389027](https://pubmed.ncbi.nlm.nih.gov/37389027/) — EFSA peer review trinexapac (2023)
- [PMID 39633074](https://pubmed.ncbi.nlm.nih.gov/39633074/) — остатки trinexapac, диссипация (2024)
- Артефакт: [search_Trinexapac-ethyl_2026-08-06_rev2.json](../../../raw/evidence/T/Trinexapac-ethyl/search_Trinexapac-ethyl_2026-08-06_rev2.json)
