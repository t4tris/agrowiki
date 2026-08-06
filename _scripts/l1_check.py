# -*- coding: utf-8 -*-
"""L1 autocheck: schema + type-check + PMID esummary + DOI Crossref for contract v1.4 report."""
import json
import os
import sys
import time
import urllib.request
import urllib.parse

REQUIRED_TOP = ['contract_version', 'substance', 'searches', 'identity', 'mode_of_action',
                'crops', 'toxicity_window', 'phi_mrl', 'contraindications', 'conflicts',
                'verdict', 'taxonomy_check', 'sources_index']
STATUSES = {'found_verified', 'found_unverified', 'no_data'}
CLAIM_TYPES = {'dosage', 'effect', 'method', 'efficacy'}
RELEVANCE = {'directly_supports', 'directly_contradicts', 'partially_relevant', 'irrelevant'}
EQ = {'direct_abstract', 'title_only', 'inferred'}
SEVERITY = {'high', 'medium', 'low'}


def fetch(url, timeout=30):
    req = urllib.request.Request(url, headers={'User-Agent': 'agro-wiki-l1/1.0'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode('utf-8', 'replace')


def main(path):
    d = json.load(open(path, encoding='utf-8'))
    errors = []

    # --- schema ---
    if d.get('contract_version') != '1.4':
        errors.append(f'contract_version != 1.4: {d.get("contract_version")}')
    for k in REQUIRED_TOP:
        if k not in d:
            errors.append(f'отсутствует поле: {k}')

    # --- v1.4 supersedes: новый артефакт вместо правки иммутабельного ---
    sup = d.get('supersedes')
    if sup:
        sup_path = os.path.join(os.path.dirname(os.path.abspath(path)), sup)
        if not os.path.exists(sup_path):
            errors.append(f'supersedes: файл не найден рядом: {sup}')

    # --- v1.4 taxonomy_check: сабагент подтверждает/исправляет class_family/mechanism ---
    tc = d.get('taxonomy_check')
    if tc is not None:
        if not isinstance(tc, dict):
            errors.append(f'taxonomy_check: должен быть объектом, получено {type(tc).__name__}')
        else:
            for fld in ('class_family_confirmed', 'mechanism_confirmed'):
                if not isinstance(tc.get(fld), bool):
                    errors.append(f'taxonomy_check.{fld} должен быть bool')
            corr = tc.get('corrections', [])
            if not isinstance(corr, list):
                errors.append('taxonomy_check.corrections должен быть массивом')
            else:
                for i, c in enumerate(corr):
                    if not isinstance(c, dict):
                        errors.append(f'taxonomy_check.corrections[{i}]: элемент не объект')
                        continue
                    for req in ('field', 'from', 'to', 'reason'):
                        if req not in c:
                            errors.append(f'taxonomy_check.corrections[{i}]: отсутствует "{req}"')

    # --- searches.failed: retry_by_orchestrator (v1.3) ---
    for i, f in enumerate(d.get('searches', {}).get('failed', [])):
        if not isinstance(f, dict):
            errors.append(f'searches.failed[{i}]: элемент не объект')
            continue
        if f.get('retry_by_orchestrator', False) is not False and not isinstance(f.get('retry_by_orchestrator'), bool):
            errors.append(f'searches.failed[{i}].retry_by_orchestrator должен быть bool')

    # --- v1.3 type-check: conflicts/contraindications = массивы объектов, без null-заглушек ---
    # Дефект 1/2: строки вместо dict и null-заглушки L1 отклоняет.
    conflicts_req = ('csv_field', 'csv_value', 'literature_summary', 'severity', 'sources')
    for field in ('conflicts', 'contraindications'):
        val = d.get(field)
        if val is None:
            errors.append(f'{field}: null — должен быть пустым массивом []')
            continue
        if not isinstance(val, list):
            errors.append(f'{field}: должен быть массивом, получено {type(val).__name__}')
            continue
        for i, item in enumerate(val):
            if not isinstance(item, dict):
                errors.append(f'{field}[{i}]: элемент не объект (строка вместо dict?)')
                continue
            if any(v is None for v in item.values()):
                errors.append(f'{field}[{i}]: содержит null-заглушку — заменить на пустой массив/убрать')
            if field == 'conflicts':
                for req in conflicts_req:
                    if req not in item:
                        errors.append(f'conflicts[{i}]: отсутствует обязательное поле "{req}"')
                if item.get('severity') not in SEVERITY:
                    errors.append(f'conflicts[{i}].severity невалиден: {item.get("severity")}')
                if not isinstance(item.get('sources', []), list):
                    errors.append(f'conflicts[{i}].sources должен быть массивом')
            elif field == 'contraindications':
                if item.get('severity') not in SEVERITY:
                    errors.append(f'contraindications[{i}].severity невалиден: {item.get("severity")}')

    for crop, cv in d.get('crops', {}).items():
        if cv.get('status') not in STATUSES:
            errors.append(f'crops.{crop}.status невалиден: {cv.get("status")}')
        # v1.3: no_data-культуры должны иметь related_evidence
        if cv.get('status') == 'no_data' and not cv.get('related_evidence'):
            errors.append(f'crops.{crop}: status=no_data, но related_evidence пуст/отсутствует')
        for c in cv.get('claims', []):
            if c.get('type') not in CLAIM_TYPES:
                errors.append(f'crops.{crop}.claims type невалиден: {c.get("type")}')
            if c.get('relevance') not in RELEVANCE:
                errors.append(f'crops.{crop}.claims relevance невалиден: {c.get("relevance")}')
            if c.get('evidence_quality') not in EQ:
                errors.append(f'crops.{crop}.claims evidence_quality невалиден: {c.get("evidence_quality")}')
            for s in c.get('sources', []):
                if not s.get('pmid') and not s.get('doi'):
                    errors.append('source без pmid и doi')
    if d.get('verdict', {}).get('evidence_level') not in {'strong', 'moderate', 'weak', 'unverified'}:
        errors.append('verdict.evidence_level невалиден')
    if d.get('verdict', {}).get('status_suggested') not in {'verified', 'corrected', 'partial',
                                                            'insufficient_data', 'conflicting'}:
        errors.append('verdict.status_suggested невалиден')

    # --- PMID esummary batch ---
    pmids = []
    for crop, cv in d.get('crops', {}).items():
        for c in cv.get('claims', []):
            for s in c.get('sources', []):
                if s.get('pmid'):
                    pmids.append(s['pmid'])
    pmids = sorted(set(pmids))
    print(f'--- L1: уникальных PMID: {len(pmids)}')
    pmid_ok = {}
    for i in range(0, len(pmids), 50):
        batch = pmids[i:i + 50]
        try:
            url = ('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?'
                   + urllib.parse.urlencode({'db': 'pubmed', 'id': ','.join(batch), 'retmode': 'json'}))
            js = json.loads(fetch(url))
            res = js.get('result', {})
            for pid in batch:
                r = res.get(pid)
                if r and r.get('title'):
                    pmid_ok[pid] = r['title']
                else:
                    pmid_ok[pid] = None
        except Exception as e:
            for pid in batch:
                pmid_ok[pid] = f'ESUMMARY_ERROR: {e}'
        time.sleep(0.5)

    bad = [p for p, t in pmid_ok.items() if not t]
    if bad:
        errors.append(f'PMID не подтверждены esummary: {bad}')
    else:
        print('Все PMID подтверждены ✅')
        for p in list(pmid_ok)[:5]:
            print(f'  {p}: {pmid_ok[p][:90]}')

    # --- DOI Crossref ---
    dois = []
    for crop, cv in d.get('crops', {}).items():
        for c in cv.get('claims', []):
            for s in c.get('sources', []):
                if s.get('doi'):
                    dois.append(s['doi'])
    dois = sorted(set(dois))
    print(f'--- L1: уникальных DOI: {len(dois)}')
    doi_ok = {}
    for doi in dois:
        try:
            js = json.loads(fetch(f'https://api.crossref.org/works/{urllib.parse.quote(doi)}'))
            title = js.get('message', {}).get('title', [''])
            doi_ok[doi] = title[0] if title else 'NO_TITLE'
        except Exception as e:
            doi_ok[doi] = f'CROSSREF_ERROR: {e}'
        time.sleep(0.3)
    bad_doi = [x for x, t in doi_ok.items() if isinstance(t, str) and t.startswith(('CROSSREF_ERROR', 'NO_TITLE'))]
    if bad_doi:
        errors.append(f'DOI не подтверждены Crossref: {bad_doi}')
    else:
        print('Все DOI подтверждены ✅')

    # --- Вывод ---
    print()
    if errors:
        print('L1: ОШИБКИ:')
        for e in errors:
            print('  -', e)
        sys.exit(1)
    print('L1: ПРОЙДЕН ✅')


if __name__ == '__main__':
    main(sys.argv[1])
