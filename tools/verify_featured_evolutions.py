#!/usr/bin/env python3
"""Verify the six user-approved permanent powered evolutions.

This check is deliberately independent of presentation/form naming heuristics.
The form IDs are append-only catalog_lock identities, all six must be Lv.70
permanent evolutions, and all six must have dedicated normal+shiny PMDCollab
behaviour sprites with strict action validation enabled.
"""
from __future__ import annotations
import json,re
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
LOCK=json.loads((ROOT/'tools/catalog_lock.json').read_text(encoding='utf-8'))
SYNC=(ROOT/'tools/sync_pmd_catalog.py').read_text(encoding='utf-8')
CAT_PATH=ROOT/'tools/pmd_catalog.json'
OUT=ROOT/'tools/featured_evolutions_report.txt'

EXPECTED={
    '0359/0001': {'id':1531,'natdex':359,'path':'0359/0001','name':'m.앱솔','base':359,'reason':'approved Mega evolution'},
    '0382/0001': {'id':1532,'natdex':382,'path':'0382/0001','name':'원시가이오가','base':382,'reason':'approved special evolution'},
    '0383/0001': {'id':1533,'natdex':383,'path':'0383/0001','name':'원시그란돈','base':383,'reason':'approved special evolution'},
    '0800/0003': {'id':1439,'natdex':800,'path':'0800/0003','name':'울트라네크로즈마','base':800,'reason':'approved special evolution'},
    '0888/0001': {'id':1534,'natdex':888,'path':'0888/0001','name':'자시안 왕의 검','base':906,'reason':'approved special evolution'},
    '0889/0001': {'id':1535,'natdex':889,'path':'0889/0001','name':'자마젠타 왕의 방패','base':907,'reason':'approved special evolution'},
}
errors=[]; lines=['TamaPoke featured evolution-6 audit','']
forms=LOCK.get('forms',{})
ids={}
for key,spec in EXPECTED.items():
    rec=forms.get(key)
    if not rec:
        errors.append(f'missing catalog_lock record: {key}')
        continue
    if int(rec.get('id',-1))!=spec['id'] or int(rec.get('natdex',-1))!=spec['natdex']:
        errors.append(f'catalog_lock identity changed: {key} -> {rec}')
    ids[int(rec['id'])]=key
if len(ids)!=len(EXPECTED): errors.append('featured evolution IDs are not unique')
if int(LOCK.get('next_form_id',0)) < 1536: errors.append('next_form_id must remain >=1536')

for token in ('APPROVED_MEGA_COUNT = 37','SPECIAL_EVOLVE_LEVEL = 70','FEATURED_EVOLUTION_NATDEX = {359, 382, 383, 800, 888, 889}'):
    if token not in SYNC: errors.append('sync policy missing: '+token)
if '359' not in re.search(r'APPROVED_MEGA_NATDEX\s*=\s*\{(.*?)\}',SYNC,re.S).group(1):
    errors.append('Mega Absol nat#359 not in curated Mega whitelist')

if CAT_PATH.is_file():
    cat=json.loads(CAT_PATH.read_text(encoding='utf-8'))
    byid={int(e['id']):e for e in cat.get('entries',[])}
    edges=cat.get('extra_edges',[])
    for key,spec in EXPECTED.items():
        e=byid.get(spec['id'])
        if not e:
            errors.append(f'catalog entry missing id {spec["id"]} {key}')
            continue
        if not e.get('enabled'): errors.append(f'featured evolution disabled: {e}')
        if int(e.get('natdex',0))!=spec['natdex']: errors.append(f'natdex mismatch: {e}')
        if e.get('pmd_path')!=spec['path']: errors.append(f'PMD path mismatch: id {spec["id"]} -> {e.get("pmd_path")}')
        if e.get('name')!=spec['name']: errors.append(f'KO display mismatch: id {spec["id"]} -> {e.get("name")}')
        if not e.get('featured_evo'): errors.append(f'featured_evo flag missing: id {spec["id"]}')
        if not e.get('shiny_required') or not e.get('strict_behavior'):
            errors.append(f'strict shiny/behavior flags missing: id {spec["id"]}')
        if not e.get('shiny_path'): errors.append(f'dedicated shiny path missing: id {spec["id"]}')
        hits=[x for x in edges if int(x.get('base',-1))==spec['base'] and int(x.get('target',-1))==spec['id'] and int(x.get('level',-1))==70 and x.get('reason')==spec['reason']]
        if len(hits)!=1: errors.append(f'Lv.70 evolution edge missing/duplicated: base {spec["base"]} -> {spec["id"]}: {hits}')
        lines.append(f"OK {spec['base']} -> {spec['id']} {spec['name']} Lv.70 / {spec['path']} / shiny={e.get('shiny_path')}")
    featured=[e for e in cat.get('entries',[]) if e.get('featured_evo') and e.get('enabled')]
    if {int(e['id']) for e in featured}!={v['id'] for v in EXPECTED.values()}:
        errors.append('featured_evo active set differs from approved six: '+repr([(e.get('id'),e.get('name')) for e in featured]))
else:
    lines.append('NOTE pmd_catalog.json not present; static lock/policy checks only (full check runs after catalog sync in Actions).')

if errors:
    lines += ['','ERRORS:']+['- '+x for x in errors]
else:
    lines += ['','featured evolution-6 audit OK']
OUT.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(OUT.read_text(encoding='utf-8'))
if errors: raise SystemExit('featured evolution-6 audit failed')
