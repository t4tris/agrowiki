# -*- coding: utf-8 -*-
"""Orchestrator Europe PMC fallback (AGENTS.md rule 10).
Subagents often lose Europe PMC (IPv6 block). Orchestrator re-runs queries here
and saves an immutable artifact: raw/evidence/{A-Z}/<code>/orchestrator_fallback_<date>.json

Usage:
  python fallback_europepmc.py CODE "csv_name" "query1" "query2" ...

For every query without SRC:PPR, a preprint variant (" AND SRC:PPR") is run too.
Results are saved as one JSON artifact per substance.
"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from datetime import date

BASE = 'https://www.ebi.ac.uk/europepmc/webservices/rest/search'
EVIDENCE = r'f:\agrowiki\raw\evidence'


def fetch(query, page_size=25):
    url = f'{BASE}?query={urllib.parse.quote(query)}&format=json&pageSize={page_size}'
    req = urllib.request.Request(url, headers={'User-Agent': 'agro-wiki-orchestrator/1.0'})
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.load(r)


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    code, csv_name = sys.argv[1], sys.argv[2]
    queries = sys.argv[3:]

    report = {
        'type': 'orchestrator_fallback',
        'created': date.today().isoformat(),
        'orchestrator': 'main agent (VS Code)',
        'reason': 'europepmc blocked in subagent env (IPv6 NAT64)',
        'substance': {'code': code, 'csv_name': csv_name},
        'searches': [],
        'preprints_relevant': [],
        'notes': [],
    }

    seen_ppr = set()
    for q in queries:
        variants = [q]
        if 'SRC:PPR' not in q:
            variants.append(f'{q} AND SRC:PPR')
        for vq in variants:
            is_ppr = 'SRC:PPR' in vq
            entry = {'query': vq, 'engine': 'europepmc', 'preprint_filter': is_ppr}
            try:
                d = fetch(vq)
                results = []
                for hit in d.get('resultList', {}).get('result', [])[:25]:
                    r = {
                        'id': hit.get('id'),
                        'source': hit.get('source'),
                        'title': hit.get('title'),
                        'first_author': (hit.get('authorString') or '').split(',')[0] if hit.get('authorString') else None,
                        'pub_year': hit.get('pubYear'),
                        'doi': hit.get('doi'),
                        'pmid': hit.get('pmid'),
                    }
                    results.append(r)
                    if is_ppr and r['id'] not in seen_ppr:
                        seen_ppr.add(r['id'])
                        report['preprints_relevant'].append(r)
                entry['total'] = d.get('hitCount', len(results))
                entry['results'] = results
                print(f'{code}: {vq} -> {entry["total"]} hits')
            except Exception as e:
                entry['error'] = str(e)
                print(f'{code}: {vq} -> ERROR {e}')
            report['searches'].append(entry)
            time.sleep(0.6)

    letter = code[0].upper() if code[0].isalpha() else '0-9'
    out_dir = os.path.join(EVIDENCE, letter, code)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f'orchestrator_fallback_{date.today().isoformat()}.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f'saved: {out_path} | preprints: {len(report["preprints_relevant"])}')


if __name__ == '__main__':
    main()
