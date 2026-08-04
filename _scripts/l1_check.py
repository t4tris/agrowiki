# -*- coding: utf-8 -*-
"""L1 autocheck: schema + PMID esummary + DOI Crossref for a contract v1.2 report."""
import json
import sys
import time
import urllib.request
import urllib.parse

REQUIRED_TOP = ['contract_version', 'substance', 'searches', 'identity', 'mode_of_action',
                'crops', 'toxicity_window', 'phi_mrl', 'contraindications', 'conflicts',
                'verdict', 'sources_index']
STATUSES = {'found_verified', 'found_unverified', 'no_data'}
CLAIM_TYPES = {'dosage', 'effect', 'method', 'efficacy'}
RELEVANCE = {'directly_supports', 'directly_contradicts', 'partially_relevant', 'irrelevant'}
EQ = {'direct_abstract', 'title_only', 'inferred'}


def fetch(url, timeout=30):
    req = urllib.request.Request(url, headers={'User-Agent': 'agro-wiki-l1/1.0'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode('utf-8', 'replace')


def main(path):
    d = json.load(open(path, encoding='utf-8'))
    errors = []

    # --- schema ---
    if d.get('contract_version') != '1.2':
        errors.append(f'contract_version != 1.2: {d.get("contract_version")}')
    for k in REQUIRED_TOP:
        if k not in d:
            errors.append(f'отсутствует поле: {k}')
    for crop, cv in d.get('crops', {}).items():
        if cv.get('status') not in STATUSES:
            errors.append(f'crops.{crop}.status невалиден: {cv.get("status")}')
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
