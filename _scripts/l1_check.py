# -*- coding: utf-8 -*-
"""L1 autocheck: schema + type-check + источник-верификация для контракта v1.5.

Контракт v1.5 (ревью 2026-08-06 part 3): добавлена поддержка источников БЕЗ PMID/DOI —
source_type: pmid | doi | openalex | isbn | url_verified | label.
Обратная совместимость: source со старыми полями pmid/doi обрабатывается как v1.4.

Верификация:
- pmid  -> esummary (title не пуст)
- doi   -> Crossref (title не пуст)
- openalex -> OpenAlex API (work резолвится)
- url_verified -> HTTP 200
- isbn  -> контрольная цифра ISBN-10/ISBN-13
- label -> допустим только с verified:true и verification_method: manual_read
"""
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
# v1.5: типы источников и методы верификации
SOURCE_TYPES = {'pmid', 'doi', 'openalex', 'isbn', 'url_verified', 'label'}
VERIF_METHODS = {'esummary', 'crossref', 'openalex_api', 'manual_read'}
PAPER_TYPES = {'review', 'trial', 'trial_in_vitro', 'mechanistic', 'preprint',
               'conference', 'regional_journal'}
VERSIONS = {'1.4', '1.5'}


def fetch(url, timeout=30):
    req = urllib.request.Request(url, headers={'User-Agent': 'agro-wiki-l1/1.5'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode('utf-8', 'replace')


def isbn_check_digit(isbn):
    """Проверка контрольной цифры ISBN-10/ISBN-13. Возвращает True/False."""
    isbn = isbn.replace('-', '').replace(' ', '').upper()
    if len(isbn) == 10:
        s = 0
        for i, ch in enumerate(isbn[:9]):
            if not ch.isdigit():
                return False
            s += int(ch) * (10 - i)
        last = isbn[9]
        check = 'X' if (11 - s % 11) == 10 else str((11 - s % 11) % 11)
        return last == check
    if len(isbn) == 13:
        if not isbn.isdigit():
            return False
        s = sum(int(ch) * (1 if i % 2 == 0 else 3) for i, ch in enumerate(isbn[:12]))
        check = (10 - s % 10) % 10
        return int(isbn[12]) == check
    return False


def iter_sources(d):
    """Итерация по всем source в claims всех культур."""
    for crop, cv in d.get('crops', {}).items():
        for c in cv.get('claims', []):
            for s in c.get('sources', []):
                yield s


def source_id(s):
    """Нормализованный идентификатор source (v1.5) или из старых полей pmid/doi."""
    if s.get('source_type'):
        return s.get('source_type'), s.get('id', '')
    if s.get('pmid'):
        return 'pmid', s['pmid']
    if s.get('doi'):
        return 'doi', s['doi']
    return None, None


def main(path):
    d = json.load(open(path, encoding='utf-8'))
    errors = []

    # --- schema ---
    ver = d.get('contract_version')
    if ver not in VERSIONS:
        errors.append(f'contract_version невалиден: {ver} (ожидается 1.4 или 1.5)')
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
                stype, sid = source_id(s)
                if stype is None:
                    errors.append(f'crops.{crop}.claims source без идентификатора (нужен pmid/doi или source_type+id)')
                    continue
                if stype in ('pmid', 'doi') and s.get('source_type'):
                    errors.append(f'crops.{crop}.claims source: source_type={stype}, но заполнены старые поля pmid/doi — используйте одно представление')
                if stype not in SOURCE_TYPES:
                    errors.append(f'crops.{crop}.claims source_type невалиден: {stype}')
                if not sid:
                    errors.append(f'crops.{crop}.claims source: пустой id для source_type={stype}')
                vm = s.get('verification_method')
                if vm is not None and vm not in VERIF_METHODS:
                    errors.append(f'crops.{crop}.claims source verification_method невалиден: {vm}')
                if s.get('paper_type') is not None and s.get('paper_type') not in PAPER_TYPES:
                    errors.append(f'crops.{crop}.claims source paper_type невалиден: {s.get("paper_type")}')
                # label — самое слабое: только с verified:true и manual_read
                if stype == 'label' and not (s.get('verified') and vm == 'manual_read'):
                    errors.append(f'crops.{crop}.claims source label: допустим только с verified:true и verification_method:manual_read')
    if d.get('verdict', {}).get('evidence_level') not in {'strong', 'moderate', 'weak', 'unverified'}:
        errors.append('verdict.evidence_level невалиден')
    if d.get('verdict', {}).get('status_suggested') not in {'verified', 'corrected', 'partial',
                                                            'insufficient_data', 'conflicting'}:
        errors.append('verdict.status_suggested невалиден')

    # --- Источник-верификация (v1.5): pmid→esummary, doi→crossref, openalex→API, url→HTTP, isbn→check digit, label→manual ---
    pmids, dois, oalex, urls, isbns, labels = [], [], [], [], [], []
    for s in iter_sources(d):
        stype, sid = source_id(s)
        if stype == 'pmid':
            pmids.append(sid)
        elif stype == 'doi':
            dois.append(sid)
        elif stype == 'openalex':
            oalex.append(sid)
        elif stype == 'url_verified':
            urls.append(sid)
        elif stype == 'isbn':
            isbns.append(sid)
        elif stype == 'label':
            labels.append(sid)
    pmids = sorted(set(pmids))

    print(f'--- L1: PMID: {len(pmids)}, DOI: {len(set(dois))}, OpenAlex: {len(set(oalex))}, URL: {len(set(urls))}, ISBN: {len(set(isbns))}, label: {len(set(labels))}')

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
                pmid_ok[pid] = r['title'] if (r and r.get('title')) else None
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

    doi_ok = {}
    for doi in sorted(set(dois)):
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

    # v1.5: OpenAlex — work резолвится (всегда возвращает JSON, проверяем title)
    oalex_ok = {}
    for wid in sorted(set(oalex)):
        wid_clean = wid.replace('OpenAlex:', '').replace('https://openalex.org/', '')
        try:
            js = json.loads(fetch(f'https://api.openalex.org/works/{urllib.parse.quote(wid_clean)}'))
            title = js.get('title')
            oalex_ok[wid] = title if title else 'NO_TITLE'
        except Exception as e:
            oalex_ok[wid] = f'OPENALEX_ERROR: {e}'
        time.sleep(0.3)
    bad_oa = [x for x, t in oalex_ok.items() if isinstance(t, str) and t.startswith(('OPENALEX_ERROR', 'NO_TITLE'))]
    if bad_oa:
        errors.append(f'OpenAlex ID не подтверждены: {bad_oa}')
    else:
        print('Все OpenAlex ID подтверждены ✅')
        for k in list(oalex_ok)[:5]:
            print(f'  {k}: {oalex_ok[k][:90]}')

    # v1.5: URL — HTTP 200
    bad_url = []
    for u in sorted(set(urls)):
        u_clean = u.replace('URL:', '')
        try:
            req = urllib.request.Request(u_clean, method='HEAD',
                                         headers={'User-Agent': 'agro-wiki-l1/1.5'})
            with urllib.request.urlopen(req, timeout=20) as r:
                if r.status >= 400:
                    bad_url.append(u)
        except Exception:
            bad_url.append(u)
    if bad_url:
        errors.append(f'URL недоступны (не HTTP 200): {bad_url}')
    else:
        print('Все URL подтверждены ✅')

    # v1.5: ISBN — контрольная цифра
    bad_isbn = [i for i in sorted(set(isbns)) if not isbn_check_digit(i.replace('ISBN:', ''))]
    if bad_isbn:
        errors.append(f'ISBN невалидны (контрольная цифра): {bad_isbn}')
    else:
        print('Все ISBN подтверждены ✅')

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
