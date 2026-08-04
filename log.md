# Log

## [2026-08-04] ingest | CSV | 275 строк → raw/
## [2026-08-04] bootstrap | 267 черновиков карточек создан
## [2026-08-04] validate | GA3 × tomato/cucumber/strawberry | 19 PMID + 18 DOI, L1 ✅ | verdict: partial/moderate (механизм усов подтверждён 4 аннотациями; все дозировки CSV не верифицированы) → [[wiki/substances/GA3]]
## [2026-08-04] validate | IBA × tomato/cucumber/strawberry | 14 PMID + 14 DOI, L1 ✅ | verdict: corrected/moderate (CSV-доза 100-1000 ppm на 2-3 порядка выше литературы) → [[wiki/substances/IBA]]
## [2026-08-04] validate | Triacontanol × tomato/cucumber/strawberry | 10 PMID + 10 DOI, L1 ✅ | verdict: partial/moderate (CSV 0.05-0.2 ppm ниже литературных 0.5-1 ppm) → [[wiki/substances/Triacontanol]]
## [2026-08-04] validate | Artemisinin × tomato/cucumber/strawberry | 0 PMID (все 3 культуры no_data), L1 ✅ | verdict: insufficient_data/weak (обе CSV-заявки не подтверждены) → [[wiki/substances/Artemisinin]]
## [2026-08-04] validate | Chitosan × tomato/cucumber/strawberry | 22 PMID + 22 DOI, L1 ✅ | verdict: partial/strong (механизм подтверждён 21 аннотацией; CSV-протоколы не верифицированы) → [[wiki/substances/Chitosan]]
## [2026-08-04] pilot | 5 сабагентов завершены | артефакты в raw/evidence/{A,C,G,I,T}/; контракт v1.2 → выявлены дефекты → v1.3 (см. отчёт)
## [2026-08-04] restructure | служебный слой вынесен из vault в корень проекта: AGENTS.md, log.md, task_queue.md, validation.md, _meta/, _scripts/, raw/, .secrets/, .gitignore, .git → f:\agrowiki\; vault = только контент (wiki/, index.md, README.md, _templates/, .obsidian/); вики-ссылки [[...]] на служебные файлы заменены на относительные md-ссылки (../AGENTS.md, ../../../raw/evidence/...); дашборд статусов перенесён в Vault/index.md | Obsidian Graph View и Cmd+O больше не засоряются служебными файлами
## [2026-08-04] git | remote origin = github.com/t4tris/agrowiki, ветка main (upstream настроен); Obsidian Git «Commit and sync» проверен в бою: коммит fa745ca через плагин ✅, пуш 7adb21b (424 объекта) ✅; история GitHub (LICENSE, README.md) слита через merge --allow-unrelated-histories
