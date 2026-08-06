# -*- coding: utf-8 -*-
"""Компактный дайджест отчёта v1.2 для оркестратора (при написании карточек)."""
import json
import sys

d = json.load(open(sys.argv[1], encoding='utf-8'))
print(f"# {d['substance']['code']} — {d['substance']['csv_name']}")
print(f"identity: CAS={d['identity'].get('cas')} CID={d['identity'].get('cid')} "
      f"formula={d['identity'].get('formula')} MW={d['identity'].get('molar_mass_g_mol')} "
      f"class_confirmed={d['identity'].get('class_confirmed')}")
print(f"  synonyms_ru: {d['identity'].get('synonyms_ru')}")
print(f"  notes: {d['identity'].get('notes')}")
print(f"MoA: {d['mode_of_action']['summary'][:300]}")
print(f"  confirmed={d['mode_of_action'].get('confirmed')}, evidence={d['mode_of_action'].get('evidence', [])[:5]}")
for crop, cv in d['crops'].items():
    print(f"\n## {crop}: {cv['status']}  stats={cv.get('search_stats')}")
    print(f"  gap: {cv.get('gap')}")
    for c in cv.get('claims', []):
        srcs = ','.join(f"{s.get('pmid') or s.get('doi')}[{s.get('year')},{s.get('verified')}]"
                        for s in c.get('sources', []))
        dn = c.get('dosage_normalized')
        dns = f" | норм: {dn['original']}→{dn.get('ppm_equivalent')}ppm" if dn and dn.get('original') else ''
        print(f"  - [{c.get('evidence_quality')}/{c.get('relevance')}] {c.get('type')}: {c.get('value')[:160]}{dns}")
        print(f"      ctx: {c.get('context','')[:120]} | cond: {json.dumps(c.get('conditions',{}), ensure_ascii=False)[:150]}")
        print(f"      srcs: {srcs} | quote: {c.get('quote','')[:100]}")
print(f"\n## toxicity_window: {json.dumps(d.get('toxicity_window'), ensure_ascii=False)}")
print(f"## phi_mrl: {json.dumps(d.get('phi_mrl'), ensure_ascii=False)}")
print(f"\n## contraindications ({len(d.get('contraindications', []))}):")
for c in d.get('contraindications', []):
    if isinstance(c, dict):
        print(f"  - {c.get('condition')} → {c.get('effect')} [{c.get('severity')}] {c.get('sources')}")
    else:
        print(f"  - {c}")
print(f"\n## conflicts ({len(d.get('conflicts', []))}):")
for c in d.get('conflicts', []):
    if isinstance(c, dict):
        print(f"  - {c.get('csv_field')}: «{str(c.get('csv_value',''))[:60]}» vs {str(c.get('literature_summary',''))[:120]} [{c.get('severity')}] {c.get('sources')}")
    else:
        print(f"  - {str(c)[:200]}")
print(f"\n## verdict: {d['verdict']}")
print(f"sources_index ({len(d.get('sources_index', []))}): {d.get('sources_index', [])[:20]}")
