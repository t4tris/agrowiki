# -*- coding: utf-8 -*-
"""Generate raw/normalization/synonyms.json from card frontmatter (code, name_en, aliases, aliases_ru).
Also prints a report of 'taxonomy-assigned-by-default' substances (audit target for AUDIT_TAXONOMY).
Idempotent.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
import gen_taxonomy as gt  # noqa: E402

SUBST_DIR = r'f:\agrowiki\Vault\wiki\substances'
OUT = r'f:\agrowiki\raw\normalization\synonyms.json'
CSV = gt.CSV


def read_frontmatter(path):
    with open(path, encoding='utf-8') as f:
        text = f.read()
    m = re.search(r'^---\n(.*?)\n---', text, re.S | re.M)
    fm = {}
    for line in (m.group(1) if m else '').splitlines():
        kv = re.match(r'^([\w]+): (.*)$', line)
        if kv:
            fm[kv.group(1)] = kv.group(2)
    return fm


def parse_list(s):
    if not s or s.strip() == '[]':
        return []
    return [x.strip().strip('"').strip("'") for x in s.strip()[1:-1].split(',')]


def main():
    registry = {}
    with open(CSV, encoding='utf-8-sig') as f:
        import csv
        csv_names = {}
        for r in csv.DictReader(f):
            csv_names.setdefault(r['Active_Substance_Code'].strip(), set()).add(r['Active_Substance_Name'].strip())

    for fn in sorted(os.listdir(SUBST_DIR)):
        if not fn.endswith('.md'):
            continue
        fm = read_frontmatter(os.path.join(SUBST_DIR, fn))
        code = fm.get('code', '')
        if not code:
            continue
        registry[code] = {
            'csv_name': sorted(csv_names.get(code, []))[:1],
            'name_en': fm.get('name_en', ''),
            'aliases': parse_list(fm.get('aliases', '[]')),
            'aliases_ru': parse_list(fm.get('aliases_ru', '[]')),
        }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    payload = {
        'generated': '2026-08-04',
        'source': 'frontmatter карточек Vault/wiki/substances (обновлять после валидации: aliases/aliases_ru)',
        'usage': 'перед поиском литературы: все синонимы в запросы (OR); русские — для fallback',
        'substances': registry,
    }
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f'synonyms.json: {len(registry)} веществ -> {OUT}')

    # ---- taxonomy audit report: substances with mechanism assigned by family default ----
    rows = list(csv.DictReader(open(CSV, encoding='utf-8-sig')))
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

    suspicious = []
    for code, info in sorted(by_code.items()):
        if code in gt.OVERRIDES:
            continue
        family = gt.pick_family(code, info['classes'])
        text = ' '.join(info['moas']).lower()
        matched = any(kw in text for kw, _ in gt.MOA_RULES)
        if not matched:
            mech = gt.DEFAULT_MECHANISM.get(family.split(';')[0].strip(), 'growth_regulation')
            suspicious.append((code, family, mech, '; '.join(info['classes'])))
    print(f'\nAUDIT_TAXONOMY: {len(suspicious)} веществ с механизмом по дефолту семейства (не оверрайд, не MoA-ключ):')
    for code, fam, mech, cls in suspicious:
        print(f'  {code:32s} {fam:28s} -> {mech:26s} | {cls[:60]}')


if __name__ == '__main__':
    main()
