#!/usr/bin/env python3
"""Deep static integrity check for TamaPoke v{FW_VERSION} DMUL 16-22 evolution routes."""
from pathlib import Path
import re
from tamapoke_version import require_semver

root=Path(__file__).resolve().parents[1]
cpp=(root/'digimon.cpp').read_text(encoding='utf-8')
h=(root/'digimon.h').read_text(encoding='utf-8')
ino=(root/'TamaPoke.ino').read_text(encoding='utf-8')

rows=[]
for idx,m in enumerate(re.finditer(r'D\("([^"]+)",(\d+),(\d+),(\d+),(\d+)\)',cpp)):
    rows.append({'id':idx,'name':m.group(1),'version':int(m.group(2)),'stage':int(m.group(3)),'power':int(m.group(4)),'style':int(m.group(5))})
assert len(rows)==458, len(rows)
by_nv={(r['name'],r['version']):r for r in rows}
names={r['name'] for r in rows}

FW_VERSION = require_semver(root, "3.94.0")
assert 'DIGI_DEVICE_SLOT_COUNT = 18' in h
assert 'return v>=16&&v<=22' in h
assert 'return (v>=1&&v<=5)||(v>=10&&v<=22)' in h

start=cpp.index('static uint8_t dmulBranches')
end=cpp.index('static uint8_t dmulRoute',start)
branch=cpp[start:end]
pat=re.compile(r'if\(!strcmp\(n,"([^"]+)"\)\)return set4\("([^"]+)","([^"]+)","([^"]+)","([^"]+)"\);')
route_defs=[]
for m in pat.finditer(branch):
    src=m.group(1); targets=list(m.groups()[1:]); route_defs.append((src,targets))
assert route_defs, 'no DMUL route definitions found'

# Every route target must exist in the same DMUL version and be exactly one stage higher.
route_sources=set()
for src,targets in route_defs:
    matching=[r for r in rows if r['name']==src and 16<=r['version']<=22]
    assert matching, f'route source missing: {src}'
    for sr in matching:
        route_sources.add((sr['version'],sr['name']))
        for target in targets:
            tr=by_nv.get((target,sr['version']))
            assert tr is not None, f'cross-version/missing route: v{sr["version"]} {src} -> {target}'
            assert tr['stage']==sr['stage']+1, f'bad stage jump: v{sr["version"]} {src}({sr["stage"]}) -> {target}({tr["stage"]})'

# All ordinary non-Ultimate DMUL forms need a normal route, except forms deliberately
# evolved only through a special condition.
special_only={(21,'Lucemon'),(22,'Paildramon'),(22,'Dinobeemon')}
missing=[]
for r in rows:
    if 16<=r['version']<=22 and r['stage']<5:
        key=(r['version'],r['name'])
        if key not in route_sources and key not in special_only:
            missing.append((r['id'],r['version'],r['stage'],r['name']))
assert not missing, f'ordinary DMUL forms without routes: {missing}'

# Ensure special targets all exist. Some are cross-version by design (GraceNovamon,
# Omegamon/Gankoomon/Tailmon/Angemon history checks), so don't impose same-version rules here.
sp_start=cpp.index('static uint16_t dmulSpecialEvolutionTarget')
sp_end=cpp.index('uint16_t digimonEvolutionTarget',sp_start)
special=cpp[sp_start:sp_end]
for target in set(re.findall(r'target\("([^"]+)"\)',special)):
    assert target in names, f'special target missing: {target}'
for material in set(re.findall(r'q\("([^"]+)",\d+\)',special)):
    assert material in names, f'Jogress/material missing: {material}'

# Guard key special chains.
required=[
 'Slayerdramon','Breakdramon','Examon','Diablomon','Armagemon','Dianamon','Apollomon','GraceNovamon',
 'MirageGaogamon','MirageGaogamon Burst Mode','Beelzebumon','Beelzebumon Blast Mode',
 'Jesmon','Gankoomon','JESmon GX','Lucemon','Lucemon Falldown Mode','Lucemon Satan Mode',
 'ExVeemon','Snimon','Paildramon','Dinobeemon','Aquilamon','Tailmon','Silphymon',
 'Ankylomon','Angemon','Shakkoumon','Imperialdramon Dragon Mode','Imperialdramon Fighter Mode',
 'Omegamon','Imperialdramon Paladin Mode','Imperialdramon OmegaX'
]
for n in required:
    assert n in names, n

# Existing special routes must still be present.
assert 'Dukemon Crimson Mode' in cpp
assert 'Alphamon Ouryuken' in cpp
assert 'pendulumFusionTarget' in cpp
assert 'DIGI_OMNIMON_ALTER_S' in cpp and 'DIGI_CHAOSMON' in cpp and 'DIGI_MILLENNIUMMON' in cpp

print(f'DMUL route integrity OK: {len(route_defs)} route sources, versions 16-22, 458 species; all normal targets stay in-version and advance one stage')
