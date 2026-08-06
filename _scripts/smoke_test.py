# -*- coding: utf-8 -*-
"""Smoke-test целостности карточек (защита от регрессий, аудит 2026-08-06).

Запуск: python _scripts/smoke_test.py   (exit 0 = всё ок, 1 = есть проблемы)

Проверяет:
1. Нет карточек-дублей по коду (MERGED_CODES не должны существовать).
2. Все карточки имеют class_family и mechanism (таксономия не стёрта).
3. Frontmatter не содержит запрещённых полей-зеркал/null-заглушек
   (application_csv, sources, toxicity_window, phi_mrl, eppo_code, ...).
4. Валидированные карточки (validation_status != unverified) не содержат
   старых секций (Применение (CSV), Corrected Dosages, Противоречия, crop_evidence)
   и баннеров «Валидировано ...» / статусных цитат.
5. Старые секции отсутствуют в теле ВСЕХ карточек (включая черновики).
6. У валидированных карточек нет хвостов бутстрапа: HTML-комментарии-заглушки
   (<!-- нет данных по культуре -->, <!-- ED50/TD50... -->, <!-- PMID / DOI / URL -->),
   дублей секций ## и служебной обвязки в секции «📅 PHI и MRL»
   (задача PHI_REI, «в открытых БД», «этикеткой препарата» — вместо лаконичного
   «Нет данных.»).
"""
import glob
import os
import re
import sys

SUBST_DIR = r'f:\agrowiki\Vault\wiki\substances'

BANNED_FIELDS = ['application_csv', 'sources:', 'eppo_code', 'regulatory_status',
                 'consensus_score', 'toxicity_window', 'phi_mrl']
OLD_SECTIONS = ['## Применение (CSV)', '## Corrected Dosages', '## Противоречия',
                '## crop_evidence']
BANNER_PATTERNS = [r'Валидировано 20\d\d', r'Статус:\s*`(verified|corrected|partial)',
                   r'Черновик из CSV']
MERGED_CODES = {'MeJA (Methyl Jasmonate)', 'Triacontanol (TRIA)'}

problems = []


def check(cond, msg):
    if not cond:
        problems.append(msg)


def main():
    files = glob.glob(os.path.join(SUBST_DIR, '*.md'))
    check(len(files) == 265, f'ожидается 265 карточек, найдено {len(files)}')

    codes = []
    for path in files:
        txt = open(path, encoding='utf-8').read()
        fm, body = txt.split('---', 2)[1], txt.split('---', 2)[2]
        name = os.path.basename(path)

        m = re.search(r'^code:\s*(.+)$', fm, re.M)
        code = m.group(1).strip() if m else '?'
        codes.append(code)
        check(code not in MERGED_CODES, f'дубль-карточка объединённого кода: {name}')

        for field in BANNED_FIELDS:
            check(not re.search(r'^' + field, fm, re.M),
                  f'запрещённое поле в frontmatter: {name} ({field})')

        check(bool(re.search(r'^class_family:', fm, re.M)),
              f'нет class_family: {name}')
        check(bool(re.search(r'^mechanism:', fm, re.M)),
              f'нет mechanism: {name}')

        for sec in OLD_SECTIONS:
            check(sec not in body, f'старая секция в теле: {name} ({sec})')

        m = re.search(r'^validation_status:\s*(\w+)', fm, re.M)
        validated = m and m.group(1) != 'unverified'
        if validated:
            for pat in BANNER_PATTERNS:
                check(not re.search(pat, body, re.M),
                      f'баннер/статус-цитата у валидированной карточки: {name} ({pat})')
            for pat in [r'\bGap\b', r'title_only', r'PubMed: 0', r'по правилам честности']:
                check(not re.search(pat, body),
                      f'процессная пометка у валидированной карточки: {name} ({pat})')
            # хвосты от бутстрапа: HTML-комментарии-заглушки в теле
            comments = re.findall(r'<!--[^>]*-->', body)
            check(not comments,
                  f'комментарии-заглушки (хвост бутстрапа) у валидированной карточки: {name} ({comments})')
            # дубли секций в теле
            h2 = re.findall(r'^##\s+.+$', body, re.M)
            dups = {h for h in h2 if h2.count(h) > 1}
            check(not dups,
                  f'дубли секций ## у валидированной карточки: {name} ({sorted(dups)})')
            # служебная обвязка в секции PHI и MRL (процессная, не факты)
            phi_mrl = re.search(r'## 📅 PHI и MRL\n(.*?)(?=\n## |\Z)', body, re.S)
            if phi_mrl:
                phi_txt = phi_mrl.group(1)
                for pat in [r'задача PHI_REI', r'в открытых БД', r'этикеткой препарата',
                            r'национальной авторизацией', r'EUPD', r'PPDB']:
                    check(not re.search(pat, phi_txt),
                          f'служебная обвязка в PHI/MRL у валидированной карточки: {name} ({pat})')

    check(len(codes) == len(set(codes)), 'дубликаты кодов в карточках')

    if problems:
        print(f'FAIL: {len(problems)} проблем:')
        for p in problems:
            print(' -', p)
        sys.exit(1)
    print(f'OK: {len(files)} карточек, все проверки пройдены')


if __name__ == '__main__':
    main()
