# -*- coding: utf-8 -*-
"""Phase 2: build taxonomy — 8 categories, ~29 class families, ~15 mechanisms.
- Updates substance cards: adds `class_family` and `mechanism` fields to frontmatter.
- Generates wiki/categories/*.md, wiki/classes/*.md, wiki/mechanisms/*.md pages.
Idempotent: pages are created only if missing; cards are patched in place (regex insert).
"""
import csv
import os
import re

CSV = r'f:\agrowiki\raw\Complete_Action_Oriented_Agronomic_Substances_CLEANED_v6.csv'
SUBST_DIR = r'f:\agrowiki\Vault\wiki\substances'
CAT_DIR = r'f:\agrowiki\Vault\wiki\categories'
CLS_DIR = r'f:\agrowiki\Vault\wiki\classes'
MEC_DIR = r'f:\agrowiki\Vault\wiki\mechanisms'

# Коды CSV, объединённые в карточки-каноны (см. dedup/merge в log.md) — карточек не имеют
MERGED_CODES = {'MeJA (Methyl Jasmonate)', 'Triacontanol (TRIA)'}

# ---- 89 CSV classes -> 29 families ----
CLASS_FAMILY = {
    'Amino Acid': 'amino_acids_polyamines', 'Amino acid': 'amino_acids_polyamines',
    'Polyamine': 'amino_acids_polyamines', 'Osmoprotectant': 'amino_acids_polyamines',
    'Biostimulant': 'biostimulants_extracts', 'Marine biostimulant': 'biostimulants_extracts',
    'Natural biostimulant': 'biostimulants_extracts', 'Organic extract': 'biostimulants_extracts',
    'Organic byproduct': 'biostimulants_extracts', 'Fungicide/Biostimulant': 'biostimulants_extracts',
    'Phenolic': 'phenolics_polyphenols', 'Polyphenol': 'phenolics_polyphenols',
    'Vitamin': 'vitamins_cofactors', 'Vitamin-like': 'vitamins_cofactors',
    'Organic Acid': 'organic_acids',
    'Peptide': 'peptides_proteins', 'Peptide hormone': 'peptides_proteins',
    'Tripeptide': 'peptides_proteins', 'Enzyme': 'peptides_proteins', 'RNA': 'peptides_proteins',
    'Auxin': 'auxins', 'Synthetic auxin': 'auxins', 'Auxin transport inhibitor': 'auxins',
    'Auxin-like': 'auxins', 'Aryloxy acid': 'auxins',
    'Brassinosteroid': 'brassinosteroids',
    'Cytokinin': 'cytokinins', 'Synthetic cytokinin': 'cytokinins',
    'Phenylurea cytokinin': 'cytokinins', 'Cytokinin analog': 'cytokinins',
    'Neonicotinoid': 'insecticides',
    'VOC': 'voc_volatiles', 'Volatile compounds': 'voc_volatiles',
    'Beneficial element': 'elements_minerals', 'Chelated nutrient': 'elements_minerals',
    'Metal / metal-oxide nanoparticles': 'elements_minerals',
    'Strigolactone': 'aba_strigolactones_karrikins', 'Karrikin': 'aba_strigolactones_karrikins',
    'ABA': 'aba_strigolactones_karrikins',
    'Triazole fungicide': 'fungicides', 'Triazole': 'fungicides',
    'Benzimidazole fungicide': 'fungicides', 'Strobilurin fungicide': 'fungicides',
    'Anilinopyrimidine fungicide': 'fungicides', 'Multi-site fungicide': 'fungicides',
    'Phenylpyrrole fungicide': 'fungicides', 'Phosphonate fungicide/biostimulant': 'fungicides',
    'Gibberellin': 'gibberellins', 'GA inhibitor': 'gibberellins',
    'Jasmonate': 'jasmonates', 'Synthetic jasmonate': 'jasmonates',
    'SAR Signal': 'sar_signals_elicitors', 'Plant hormone + disaccharide': 'sar_signals_elicitors',
    'Nitrophenolate': 'synthetic_growth_regulators', 'Growth inhibitor': 'synthetic_growth_regulators',
    'Acylcyclohexanedione': 'synthetic_growth_regulators', 'Quaternary ammonium': 'synthetic_growth_regulators',
    'Synthetic tertiary amine': 'synthetic_growth_regulators', 'Defoliant/regulator': 'synthetic_growth_regulators',
    'Pyrimidine': 'synthetic_growth_regulators', 'Diazine': 'synthetic_growth_regulators',
    'Synthetic polymer': 'synthetic_growth_regulators', 'Halogenated pyruvate': 'synthetic_growth_regulators',
    'Alkylating agent': 'synthetic_growth_regulators', 'Nucleoside analog': 'synthetic_growth_regulators',
    'Polymeric guanidine': 'antibacterials', 'Nitrile': 'synthetic_growth_regulators',
    'Ethylene inhibitor': 'ethylene', 'Ethylene releaser': 'ethylene', 'Ethylene': 'ethylene',
    'Indolamine derivative': 'indolamines', 'Indolamine': 'indolamines', 'Indoleamine': 'indolamines',
    'Gasotransmitter': 'gasotransmitters', 'Iron nitrosyl complex': 'gasotransmitters',
    'Sulfide salt': 'gasotransmitters',
    'Related': 'other', 'Oxidant': 'antibacterials', 'Solvent': 'other', 'Surfactant': 'other',
    'Disaccharide': 'carbohydrates', 'Polysaccharide': 'carbohydrates',
    'Monosaccharide': 'carbohydrates', 'Carbohydrate source': 'carbohydrates',
    'Saponin': 'terpenoids_saponins_lipids', 'Sesquiterpene lactone': 'terpenoids_saponins_lipids',
    'Phospholipid': 'terpenoids_saponins_lipids', 'Long-chain alcohol': 'terpenoids_saponins_lipids',
    'Aldehyde': 'terpenoids_saponins_lipids',
}

DEFAULT_MECHANISM = {
    'auxins': 'auxin_signaling', 'cytokinins': 'cytokinin_signaling',
    'gibberellins': 'gibberellin_action', 'brassinosteroids': 'brassinosteroid_signaling',
    'ethylene': 'ethylene_signaling', 'jasmonates': 'jasmonate_sar_defense',
    'aba_strigolactones_karrikins': 'aba_stress_signaling',
    'amino_acids_polyamines': 'nutrition_metabolism', 'peptides_proteins': 'growth_regulation',
    'vitamins_cofactors': 'nutrition_metabolism', 'phenolics_polyphenols': 'antioxidant_defense',
    'organic_acids': 'nutrition_metabolism', 'carbohydrates': 'nutrition_metabolism',
    'terpenoids_saponins_lipids': 'growth_regulation', 'indolamines': 'growth_regulation',
    'gasotransmitters': 'gas_signaling', 'voc_volatiles': 'jasmonate_sar_defense',
    'sar_signals_elicitors': 'jasmonate_sar_defense', 'fungicides': 'pesticide_action',
    'insecticides': 'pesticide_action', 'herbicides': 'pesticide_action',
    'nematicides': 'pesticide_action', 'acaricides': 'pesticide_action',
    'antibacterials': 'pesticide_action', 'antivirals': 'pesticide_action',
    'biostimulants_extracts': 'elicitor_immunity',
    'elements_minerals': 'nutrition_metabolism',
    'synthetic_growth_regulators': 'growth_regulation', 'other': 'growth_regulation',
}

# MoA keyword rules (priority over class default), order matters
MOA_RULES = [
    ('osmoprotect', 'osmoprotection'),
    ('antioxidant', 'antioxidant_defense'),
    ('photosynthesis', 'photosynthesis_enhancement'),
    ('chlorophyll', 'photosynthesis_enhancement'),
    ('CO2 fixation', 'photosynthesis_enhancement'),
    ('carboxylation', 'photosynthesis_enhancement'),
    ('electron transport', 'photosynthesis_enhancement'),
    ('nitric oxide', 'gas_signaling'), ('NO donor', 'gas_signaling'),
    ('hydrogen sulfide', 'gas_signaling'), ('H2S donor', 'gas_signaling'),
    ('brassinosteroid', 'brassinosteroid_signaling'),
    ('cytokinin', 'cytokinin_signaling'),
    ('cell division', 'cytokinin_signaling'),
    ('ethylene', 'ethylene_signaling'), ('ripening', 'ethylene_signaling'),
    ('anti-ripening', 'ethylene_signaling'), ('abscission', 'ethylene_signaling'),
    ('gibberellin', 'gibberellin_action'), ('GA inhibitor', 'gibberellin_action'),
    ('dwarfing', 'gibberellin_action'), ('lodging', 'gibberellin_action'),
    ('cell elongation', 'gibberellin_action'),
    ('auxin', 'auxin_signaling'),
    ('rooting', 'auxin_signaling'), ('root growth', 'auxin_signaling'),
    ('root development', 'auxin_signaling'),
    ('jasmonate', 'jasmonate_sar_defense'), ('airborne signaling', 'jasmonate_sar_defense'),
    ('elicitor', 'elicitor_immunity'), ('SAR inducer', 'elicitor_immunity'),
    ('immune', 'elicitor_immunity'), ('defense', 'elicitor_immunity'),
    ('stress', 'aba_stress_signaling'), ('ABA', 'aba_stress_signaling'),
    ('nAChR', 'pesticide_action'), ('sterol', 'pesticide_action'),
    ('antimicrobial', 'pesticide_action'), ('nematicid', 'pesticide_action'),
    ('herbicid', 'pesticide_action'), ('weed control', 'pesticide_action'),
    ('antibacteri', 'pesticide_action'), ('bactericid', 'pesticide_action'),
    ('antivir', 'pesticide_action'), ('viruc', 'pesticide_action'),
    ('acar', 'pesticide_action'), ('miticid', 'pesticide_action'),
    ('disinfect', 'pesticide_action'), ('sanitizer', 'pesticide_action'),
    ('glycolysis inhibitor', 'pesticide_action'), ('metabolic inhibitor', 'pesticide_action'),
    ('seed sanitizer', 'pesticide_action'),
    ('chelat', 'nutrition_metabolism'), ('nitrogen', 'nutrition_metabolism'),
    ('protein synthesis', 'nutrition_metabolism'), ('protein building', 'nutrition_metabolism'),
    ('enzyme cofactor', 'nutrition_metabolism'), ('microbial', 'nutrition_metabolism'),
    ('carbon source', 'nutrition_metabolism'), ('soil conditioner', 'nutrition_metabolism'),
    ('pH modifier', 'nutrition_metabolism'), ('cofactor', 'nutrition_metabolism'),
    ('precursor', 'nutrition_metabolism'), ('metabolic', 'nutrition_metabolism'),
    ('nano-priming', 'nutrition_metabolism'),
    ('growth', 'growth_regulation'), ('flowering', 'growth_regulation'),
    ('fruit set', 'growth_regulation'), ('fruit size', 'growth_regulation'),
    ('branching', 'growth_regulation'), ('dormancy', 'growth_regulation'),
    ('germination', 'growth_regulation'), ('sprouting inhibitor', 'growth_regulation'),
    ('thinning', 'growth_regulation'), ('dwarfing', 'gibberellin_action'),
]

OVERRIDES = {
    'GA3': 'gibberellin_action', 'GA1': 'gibberellin_action', 'GA4': 'gibberellin_action',
    'IBA': 'auxin_signaling', 'NAA': 'auxin_signaling', '2,4-D': 'auxin_signaling',
    '4-CPA': 'auxin_signaling', '3-CPA': 'auxin_signaling', '2,4,5-T': 'auxin_signaling',
    'MCPA': 'auxin_signaling', 'Dicamba': 'auxin_signaling', 'MCPB': 'auxin_signaling',
    'Picloram': 'auxin_signaling', 'Triclopyr': 'auxin_signaling', 'BNOA': 'auxin_signaling',
    '6-BA': 'cytokinin_signaling', '6-BAP': 'cytokinin_signaling', 'Kinetin': 'cytokinin_signaling',
    'Zeatin': 'cytokinin_signaling', '2iP': 'cytokinin_signaling', 'CPPU': 'cytokinin_signaling',
    'TDZ': 'cytokinin_signaling', 'Thidiazuron': 'cytokinin_signaling',
    'Ethephon': 'ethylene_signaling', 'Ethylene': 'ethylene_signaling',
    '1-MCP': 'ethylene_signaling', 'STS': 'ethylene_signaling', 'Aviglycine': 'ethylene_signaling',
    'Glycine Betaine': 'osmoprotection', 'Proline': 'osmoprotection', 'Trehalose': 'osmoprotection',
    '5-ALA': 'photosynthesis_enhancement', 'Triacontanol': 'photosynthesis_enhancement',
    'Triacontanol (TRIA)': 'photosynthesis_enhancement',
    'Chitosan': 'elicitor_immunity', 'Chitooligosaccharides': 'elicitor_immunity',
    'BABA': 'elicitor_immunity', 'MeJA': 'jasmonate_sar_defense',
    'Methyl Jasmonate': 'jasmonate_sar_defense', 'Cis-jasmone': 'jasmonate_sar_defense',
    'PDJ': 'jasmonate_sar_defense',
    'Paclobutrazol': 'gibberellin_action', 'Uniconazole': 'gibberellin_action',
    'PIX': 'gibberellin_action', 'Chlormequat Chloride': 'gibberellin_action',
    'Trinexapac-ethyl': 'gibberellin_action', 'Ancymidol': 'gibberellin_action',
    'B9': 'gibberellin_action', 'Brassinazole': 'brassinosteroid_signaling',
    'Melatonin': 'antioxidant_defense', 'Serotonin': 'growth_regulation',
    'Ascorbic Acid': 'antioxidant_defense', 'Alpha-lipoic acid': 'antioxidant_defense',
    'Cobalt': 'nutrition_metabolism',
    'Magnesium': 'nutrition_metabolism', 'DMSO': 'growth_regulation',
    # Правки по итогам аудита AUDIT_TAXONOMY (2026-08-04): дефолты семейств уточнены
    'GSH': 'antioxidant_defense',               # глутатион — главный антиоксидант
    'Methyl Salicylate': 'jasmonate_sar_defense',  # MeSA — летучий сигнал защиты/SAR
    'Carbonic Anhydrase': 'photosynthesis_enhancement',  # карбоангидраза — CO2-фиксация
    'HypSys peptides': 'jasmonate_sar_defense',  # системин-подобные пептиды защиты
    'L-carnitine': 'nutrition_metabolism',      # карнитин — метаболизм/энергетика
    # Коррекции taxonomy_check (контракт v1.4, валидация 2026-08-04)
    'Silicon': 'antioxidant_defense',           # основной механизм — антиоксидантная защита
    'Artemisinin': 'pesticide_action',          # заявка CSV: нематоцид (не подтверждена валидацией)
    'Polyhexamethylene guanidine': 'pesticide_action',  # биоцид широкого спектра, а не PGR
    'HOCl': 'pesticide_action',                 # дезинфектант (активный хлор), а не элиситор
}

# Ручные правки class_family по итогам валидации (taxonomy_check v1.4); применяются до маппинга классов
FAMILY_OVERRIDES = {
    'Paclobutrazol': 'synthetic_growth_regulators',  # триазольный ретардант, НЕ фунгицид по применению
    # Синтетические ауксиновые гербициды (CSV-класс 'Synthetic auxin', MoA указывает на гербицидное применение)
    '2,4-D': 'herbicides', '2,4,5-T': 'herbicides', 'MCPA': 'herbicides', 'MCPB': 'herbicides',
    'Dicamba': 'herbicides', 'Picloram': 'herbicides', 'Triclopyr': 'herbicides',
    # Нематоциды (CSV MoA «Nematicidal agent»)
    'Artemisinin': 'nematicides',
}

# ---------- page metadata ----------
CATS = [
    ('foliar-application', 'Внекорневая обработка', 'FOLIAR_APPLICATION',
     'Обработка растений по листу (опрыскивание): биостимуляторы, регуляторы роста, удобрения. '
     'Самая массовая категория CSV (171 строка).'),
    ('seed-treatment', 'Обработка семян', 'SEED_TREATMENT',
     'Предпосевная обработка: замачивание, инкрустация, прайминг. Цель — прорастание, стартовая '
     'энергия, защита всходов (27 строк).'),
    ('fruit-management', 'Управление плодоношением', 'FRUIT_MANAGEMENT',
     'Завязывание, рост, созревание и качество плодов: фиксаторы завязи, регуляторы созревания, '
     'прореживание (23 строки).'),
    ('growth-regulation', 'Регуляция роста', 'GROWTH_REGULATION',
     'Ретарданты и стимуляторы вегетативного роста, ветвление, высота растения (22 строки).'),
    ('soil-application', 'Внесение в почву', 'SOIL_APPLICATION',
     'Корневые подкормки, полив, капельное орошение, мелиоранты, биостимуляция ризосферы (16 строк).'),
    ('root-development', 'Развитие корневой системы', 'ROOT_DEVELOPMENT',
     'Стимуляция корнеобразования: ауксины, укоренители черенков, ризогенез (10 строк).'),
    ('stress-tolerance', 'Устойчивость к стрессу', 'STRESS_TOLERANCE',
     'Защита от абиотических стрессов: засуха, жара, соль, заморозки (3 строки).'),
    ('photosynthesis-enhancement', 'Усиление фотосинтеза', 'PHOTOSYNTHESIS_ENHANCEMENT',
     'Стимуляция фотосинтетического аппарата, содержание хлорофилла, CO2-фиксация (3 строки).'),
]

FAMILIES = [
    ('auxins', 'Ауксины', ['Auxin', 'Synthetic auxin', 'Auxin transport inhibitor', 'Auxin-like', 'Aryloxy acid'],
     'Натуральные и синтетические ауксины: ризогенез, тропизмы, апикальное доминирование, завязь.'),
    ('cytokinins', 'Цитокинины', ['Cytokinin', 'Synthetic cytokinin', 'Phenylurea cytokinin', 'Cytokinin analog'],
     'Деление клеток, побегообразование, задержка старения, выход из покоя.'),
    ('gibberellins', 'Гиббереллины и ингибиторы GA', ['Gibberellin', 'GA inhibitor'],
     'Вытягивание стебля, прорастание, цветение; ингибиторы — ретарданты (Paclobutrazol и др.).'),
    ('brassinosteroids', 'Брассиностероиды', ['Brassinosteroid'],
     'Стероидные гормоны: рост, стрессоустойчивость, фотоморфогенез.'),
    ('ethylene', 'Этилен и регуляторы созревания', ['Ethylene', 'Ethylene inhibitor', 'Ethylene releaser'],
     'Созревание, старение, опадение; ингибиторы (1-MCP) и стимуляторы (Ethephon).'),
    ('jasmonates', 'Жасмонаты', ['Jasmonate', 'Synthetic jasmonate'],
     'Сигнальные липидные гормоны: защита от стресса, аромат, отпугивание вредителей.'),
    ('aba_strigolactones_karrikins', 'АБК, стриголактоны и каррикины', ['ABA', 'Strigolactone', 'Karrikin'],
     'Абсцизовая кислота (стресс, устьица), стриголактоны (симбиоз, ветвление), каррикины (прорастание).'),
    ('amino_acids_polyamines', 'Аминокислоты и полиамины', ['Amino Acid', 'Amino acid', 'Polyamine', 'Osmoprotectant'],
     'Строительные блоки белков, предшественники гормонов, осмопротекторы (Glycine Betaine, Proline).'),
    ('peptides_proteins', 'Пептиды и белки', ['Peptide', 'Peptide hormone', 'Tripeptide', 'Enzyme', 'RNA'],
     'Сигнальные пептиды (CLE, CEP, PSK), ферменты, регуляторные белки.'),
    ('vitamins_cofactors', 'Витамины и кофакторы', ['Vitamin', 'Vitamin-like'],
     'Аскорбиновая кислота, тиамин, ниацин, холин и др. — антиоксиданты и кофакторы метаболизма.'),
    ('phenolics_polyphenols', 'Фенольные соединения', ['Phenolic', 'Polyphenol'],
     'Фенолкислоты, флавоноиды, лигнины: антиоксиданты, сигнальные молекулы, защита от УФ.'),
    ('organic_acids', 'Органические кислоты', ['Organic Acid'],
     'Цитрат, сукцинат, фульвовые кислоты: метаболизм, хелатирование, pH, энергетика.'),
    ('carbohydrates', 'Углеводы', ['Disaccharide', 'Polysaccharide', 'Monosaccharide', 'Carbohydrate source'],
     'Сахара и полисахариды: энергия, осмопротекция, структура клеточной стенки.'),
    ('terpenoids_saponins_lipids', 'Терпеноиды, сапонины, липиды', ['Sesquiterpene lactone', 'Saponin', 'Phospholipid', 'Long-chain alcohol', 'Aldehyde'],
     'Вторичные метаболиты и липиды: Triacontanol, Artemisinin, диосгенин и др.'),
    ('indolamines', 'Индоламины', ['Indolamine', 'Indolamine derivative', 'Indoleamine'],
     'Производные триптофана: серотонин, мелатонин — антиоксиданты и регуляторы развития.'),
    ('gasotransmitters', 'Газотрансмиттеры', ['Gasotransmitter', 'Iron nitrosyl complex', 'Sulfide salt'],
     'NO, H2S, CO — газовые сигнальные молекулы (доноры оксида азота, сульфида).'),
    ('voc_volatiles', 'Летучие органические соединения (VOC)', ['VOC', 'Volatile compounds'],
     'Летучие сигналы растений: защита, коммуникация, ароматы.'),
    ('sar_signals_elicitors', 'Сигналы SAR', ['SAR Signal', 'Plant hormone + disaccharide'],
     'Сигналы системной приобретённой устойчивости: салициловая кислота и её индукторы.'),
    ('fungicides', 'Фунгициды', ['Triazole fungicide', 'Triazole', 'Benzimidazole fungicide', 'Strobilurin fungicide', 'Anilinopyrimidine fungicide', 'Multi-site fungicide', 'Phenylpyrrole fungicide', 'Phosphonate fungicide/biostimulant'],
     'Химические средства защиты от грибных болезней: ингибиторы стеролов, дыхания, микротрубочек.'),
    ('insecticides', 'Инсектициды', ['Neonicotinoid'],
     'Химические средства защиты от насекомых: неоникотиноиды (агонисты nAChR).'),
    ('herbicides', 'Гербициды', ['Synthetic auxin'],
     'Синтетические ауксиновые гербициды (2,4-D, MCPA, дикамба, пиклорам, триклопир): сверхоптимальные '
     'дозы ауксинов вызывают неконтролируемый рост и гибель двудольных сорняков. '
     'В CSV выделены по Mode_of_Action (Auxin herbicide, Weed control at high dose).'),
    ('nematicides', 'Нематоциды', [],
     'Средства против нематод. В CSV: артемизинин (MoA «Nematicidal agent») — заявка не подтверждена '
     'валидацией (insufficient_data).'),
    ('acaricides', 'Акарициды (митициды)', [],
     'Средства против растительноядных клещей (отряд Acari). «Митициды» — англ. синоним (miticide). '
     'В CSV веществ нет — семейство создано для полноты классификации пестицидов.'),
    ('antibacterials', 'Антибактериальные', ['Polymeric guanidine', 'Oxidant'],
     'Бактерициды и дезинфектанты: полимерные гуанидины (PHMG), активный хлор (HOCl, гипохлорит натрия).'),
    ('antivirals', 'Противовирусные', [],
     'Средства против вирусов растений. В CSV веществ нет — семейство создано для полноты '
     'классификации пестицидов.'),
    ('biostimulants_extracts', 'Биостимуляторы и экстракты', ['Biostimulant', 'Marine biostimulant', 'Natural biostimulant', 'Organic extract', 'Organic byproduct', 'Fungicide/Biostimulant'],
     'Экстракты водорослей (Ascophyllum, Ecklonia), гуминовые вещества, микробные биостимуляторы.'),
    ('elements_minerals', 'Элементы и минералы', ['Beneficial element', 'Chelated nutrient', 'Metal / metal-oxide nanoparticles'],
     'Полезные элементы (Si, Co, Se), хелатированные микроудобрения, наночастицы.'),
    ('synthetic_growth_regulators', 'Синтетические регуляторы роста', ['Nitrophenolate', 'Growth inhibitor', 'Acylcyclohexanedione', 'Quaternary ammonium', 'Synthetic tertiary amine', 'Defoliant/regulator', 'Pyrimidine', 'Diazine', 'Synthetic polymer', 'Halogenated pyruvate', 'Alkylating agent', 'Nucleoside analog', 'Nitrile'],
     'Синтетические соединения, регулирующие рост: нитрофеноляты (Atonik), DA-6, дефолианты.'),
    ('other', 'Прочее', ['Related', 'Solvent', 'Surfactant'],
     'Вспомогательные и трудно классифицируемые соединения: DMSO, децилглюкозид, пероксид водорода.'),
]

MECHANISMS = [
    ('auxin_signaling', 'Ауксиновая сигнализация',
     'Ауксины (IAA, IBA, NAA, 2,4-D) регулируют ризогенез, тропизмы, апикальное доминирование и '
     'завязывание плодов через сигнальные пути PIN/ABP1/TIR1.'),
    ('cytokinin_signaling', 'Цитокининовая сигнализация',
     'Цитокинины (зеатин, кинетин, 6-BA, TDZ) стимулируют деление клеток, побегообразование, '
     'задержку старения.'),
    ('gibberellin_action', 'Действие гиббереллинов и их ингибиторов',
     'Гиббереллины (GA3, GA4) удлиняют стебель, запускают прорастание и цветение; ингибиторы '
     'биосинтеза GA (Paclobutrazol, Uniconazole, CCC) — классические ретарданты.'),
    ('ethylene_signaling', 'Этиленовая сигнализация',
     'Этилен и его аналоги (Ethephon) управляют созреванием, старением, опадением; ингибиторы '
     '(1-MCP, STS) блокируют рецептор.'),
    ('brassinosteroid_signaling', 'Брассиностероидная сигнализация',
     'Брассинолид и его аналоги (24-EBL, EBR) повышают урожайность и устойчивость к стрессам; '
     'ингибиторы (Brassinazole) — исследовательский инструмент.'),
    ('aba_stress_signaling', 'АБК и стрессовая сигнализация',
     'Абсцизовая кислота и близкие сигналы (стриголактоны, каррикины) — ответ на засуху, соль, '
     'жару: закрытие устьиц, покой, прорастание.'),
    ('jasmonate_sar_defense', 'Жасмонаты и системная защита',
     'Жасмоновая кислота и MeJA — сигналы защиты от некротрофов и вредителей; VOC-коммуникация '
     'между растениями.'),
    ('elicitor_immunity', 'Элиситоры и индуцированный иммунитет',
     'Хитозан, BABA, гликаны и другие элиситоры запускают PRR-сигналинг и системную '
     'резистентность (SAR/ISR) без прямого токсического действия.'),
    ('antioxidant_defense', 'Антиоксидантная защита',
     'Аскорбиновая кислота, фенольные соединения, мелатонин и др. нейтрализуют АФК, защищают '
     'мембраны и фотосинтетический аппарат от окислительного стресса.'),
    ('osmoprotection', 'Осмопротекция',
     'Совместимые осмолиты (Glycine Betaine, Proline, трегалоза) стабилизируют белки и мембраны '
     'при засухе, засолении и заморозках.'),
    ('photosynthesis_enhancement', 'Усиление фотосинтеза',
     '5-ALA, Triacontanol и микроэлементы повышают содержание хлорофилла, активность Rubisco и '
     'CO2-фиксацию, особенно в стрессовых условиях.'),
    ('nutrition_metabolism', 'Питание и метаболизм',
     'Аминокислоты, витамины, хелаторы и микроэлементы: азотный обмен, энергетика (TCA), '
     'кофакторы ферментов, хелатирование, ризосферные взаимодействия.'),
    ('growth_regulation', 'Общая регуляция роста и развития',
     'Синтетические регуляторы (нитрофеноляты, DA-6, PIX), гормоноподобные соединения: '
     'цветение, ветвление, плодоношение, покой, прорастание.'),
    ('gas_signaling', 'Газовая сигнализация (NO, H2S, CO)',
     'Доноры оксида азота, сероводорода и угарного газа — сигнальные молекулы, модулирующие '
     'укоренение, прорастание и стрессоустойчивость.'),
    ('pesticide_action', 'Пестицидное действие',
     'Средства защиты растений: фунгициды (триазолы, стробилурины, бензимидазолы), инсектициды '
     '(неоникотиноиды), гербициды, нематоциды, акарициды, антибактериальные и противовирусные: '
     'прямое подавление патогенов, вредителей и сорняков.'),
]

# ---------- helpers ----------
def pick_family(code, classes):
    if code in FAMILY_OVERRIDES:
        return FAMILY_OVERRIDES[code]
    fams = [CLASS_FAMILY[c] for c in classes if c in CLASS_FAMILY]
    if not fams:
        return 'other'
    # if multiple, join unique
    return '; '.join(dict.fromkeys(fams))


def pick_mechanism(code, moas, family):
    if code in OVERRIDES:
        return OVERRIDES[code]
    text = ' '.join(moas).lower()
    for kw, mech in MOA_RULES:
        if kw in text:
            return mech
    fam = family.split(';')[0].strip()
    return DEFAULT_MECHANISM.get(fam, 'growth_regulation')


def insert_frontmatter(path, family, mechanism, refresh=False):
    with open(path, encoding='utf-8') as f:
        text = f.read()
    if 'class_family:' in text:
        if not refresh:
            return False
        # NB: [^\r\n]* вместо .* — не съедать \r (CRLF) при перезаписи
        new_text = re.sub(r'^(class_family: )[^\r\n]*', rf'\g<1>{family}', text, count=1, flags=re.M)
        new_text = re.sub(r'^(mechanism: )[^\r\n]*', rf'\g<1>{mechanism}', new_text, count=1, flags=re.M)
        if new_text == text:
            return False
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_text)
        return True
    # insert after the `class:` line inside frontmatter
    new_text = re.sub(r'^(class: )[^\r\n]*',
                      rf'\g<0>\nclass_family: {family}\nmechanism: {mechanism}',
                      text, count=1, flags=re.M)
    if new_text == text:
        return False
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_text)
    return True


def write_page(path, content):
    if os.path.exists(path):
        return False
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return True


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Build taxonomy (categories/classes/mechanisms pages + card fields)')
    parser.add_argument('--refresh', action='store_true',
                        help='обновить class_family/mechanism в карточках до вычисленных значений '
                             '(по умолчанию существующие поля не перезаписываются — уважать ручные правки)')
    args = parser.parse_args()

    with open(CSV, encoding='utf-8-sig') as f:
        rows = list(csv.DictReader(f))
    by_code = {}
    for r in rows:
        code = r['Active_Substance_Code'].strip()
        by_code.setdefault(code, {'classes': [], 'moas': []})
        cl = r['Chemical_Class'].strip()
        if cl and cl not in by_code[code]['classes']:
            by_code[code]['classes'].append(cl)
        moa = r['Mode_of_Action'].strip()
        if moa and moa not in by_code[code]['moas']:
            by_code[code]['moas'].append(moa)

    patched = 0
    for code, info in sorted(by_code.items()):
        family = pick_family(code, info['classes'])
        mechanism = pick_mechanism(code, info['moas'], family)
        # find card file: name matches code
        for fn in os.listdir(SUBST_DIR):
            if fn.lower().startswith(code.lower() + '.'):
                path = os.path.join(SUBST_DIR, fn)
                if insert_frontmatter(path, family, mechanism, refresh=args.refresh):
                    patched += 1
                break
        else:
            if code not in MERGED_CODES:
                print(f'WARN: card not found for code {code}')

    print(f'cards patched: {patched}/{len(by_code)}')

    os.makedirs(CAT_DIR, exist_ok=True)
    os.makedirs(CLS_DIR, exist_ok=True)
    os.makedirs(MEC_DIR, exist_ok=True)

    created = 0
    for slug, name, ac, desc in CATS:
        content = f"""---
type: category
name: {name}
action_category: {ac}
substances: []
---

# {name} ({ac})

{desc}

## Вещества по CSV
```dataview
TABLE efficacy_csv AS "Эффективность", validation_status AS "Статус", crops.tomato AS "Томат", crops.cucumber AS "Огурец", crops.strawberry AS "Клубника"
FROM "wiki/substances"
WHERE action_category = "{ac}"
SORT validation_status ASC
```
"""
        created += write_page(os.path.join(CAT_DIR, slug + '.md'), content)

    for slug, name, csv_classes, desc in FAMILIES:
        cls_list = ', '.join(f'`{c}`' for c in csv_classes)
        content = f"""---
type: class
name: {name}
class_csv: {csv_classes}
substances: []
---

# Класс: {name}

{desc}

CSV-классы семейства: {cls_list}.

## Вещества
```dataview
TABLE class AS "Класс (CSV)", efficacy_csv AS "Эффективность", validation_status AS "Статус"
FROM "wiki/substances"
WHERE contains(class_family, "{slug}")
SORT validation_status ASC
```
"""
        created += write_page(os.path.join(CLS_DIR, slug + '.md'), content)

    for slug, name, desc in MECHANISMS:
        content = f"""---
type: mechanism
name: {name}
substances: []
---

# Механизм: {name}

{desc}

## Вещества
```dataview
TABLE class_family AS "Семейство", efficacy_csv AS "Эффективность", validation_status AS "Статус"
FROM "wiki/substances"
WHERE mechanism = "{slug}"
SORT validation_status ASC
```
"""
        created += write_page(os.path.join(MEC_DIR, slug + '.md'), content)

    print(f'pages created: {created} (cats={len(CATS)}, fams={len(FAMILIES)}, mechs={len(MECHANISMS)})')


if __name__ == '__main__':
    main()
