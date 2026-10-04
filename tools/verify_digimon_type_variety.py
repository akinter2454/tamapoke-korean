#!/usr/bin/env python3
"""Guard the explicit Digimon type source and Jogress type policy."""
from pathlib import Path
import json, re, subprocess, sys

root=Path(__file__).resolve().parents[1]
doc=json.loads((root/'data/digimon/types.json').read_text(encoding='utf-8'))
entries=doc['entries']
cpp=(root/'digimon.cpp').read_text(encoding='utf-8')
species=[(m.group(1),int(m.group(2)),int(m.group(3))) for m in re.finditer(r'D\("([^"]+)",(\d+),(\d+),(\d+),(\d+)\)',cpp)]
assert len(entries)==len(species)==458, (len(entries),len(species))

valid={'NORMAL','FIRE','WATER','ELECTRIC','GRASS','ICE','FIGHTING','POISON','GROUND','FLYING','PSYCHIC','BUG','ROCK','GHOST','DRAGON','DARK','STEEL','FAIRY'}
seen_types=set(); by={}; names={}
dual=0
for i,(e,(name,ver,stage)) in enumerate(zip(entries,species)):
    assert e['index']==i and e['name']==name and e['version']==ver and e['stage']==stage, (i,e,(name,ver,stage))
    t1,t2=e['type1'],e['type2']
    assert t1 in valid and (t2=='NONE' or t2 in valid) and t1!=t2
    seen_types.add(t1)
    if t2!='NONE': seen_types.add(t2); dual+=1
    if stage>=2: assert t2!='NONE', f'Child+ Digimon must be dual typed: {i} {name}'
    if name in names: assert names[name]==(t1,t2), f'inconsistent duplicate {name}: {names[name]} vs {(t1,t2)}'
    names[name]=(t1,t2); by[(ver,name)]=(t1,t2)
assert seen_types==valid, f'missing types: {sorted(valid-seen_types)}'
assert dual>=290, f'dual type coverage regressed: {dual}/458'
assert 'digiThemeType' not in cpp and 'hasWord(n,' not in cpp, 'runtime name/version typing must stay removed'
assert 'DIGI_TYPE_PROFILE[i].type1' in cpp and 'DIGI_TYPE_PROFILE[i].type2' in cpp

# Jogress/fusion result pairs are deliberately chosen from material identities.
def union(*keys):
    s=set()
    for k in keys:
        p=by[k]
        s.update(x for x in p if x!='NONE')
    return s
def check(result, parents):
    rp=by[result]
    u=union(*parents)
    assert rp[0] in u and rp[1] in u, f'{result}={rp} does not mix parents {parents} -> {u}'

check((15,'Omegamon'), ((15,'WarGreymon'),(15,'MetalGarurumon')))
check((10,'Omegamon'), ((10,'WarGreymon'),(10,'MetalGarurumon')))
check((11,'Mastemon'), ((11,'Angewomon'),(13,'LadyDevimon')))
check((13,'Mastemon'), ((11,'Angewomon'),(13,'LadyDevimon')))
check((10,'Mastemon'), ((10,'Angewomon'),(13,'LadyDevimon')))
check((12,'Aegisdramon'), ((12,'Plesiomon'),(12,'MetalSeadramon')))
check((12,'Mitamamon'), ((12,'MarinAngemon'),(14,'Hououmon')))
check((14,'Mitamamon'), ((12,'MarinAngemon'),(14,'Hououmon')))
check((13,'Voltobautamon'), ((13,'Vamdemon'),(13,'Piemon')))
check((14,'Cernumon'), ((14,'Griffomon'),(14,'Pinochimon')))
check((10,'Proximamon'), ((10,'Siriusmon'),(10,'Arcturusmon')))
# DMC fusion-only entries use their stable v0 identities.
byidx={e['index']:(e['type1'],e['type2']) for e in entries}
def check_idx(result,*parents):
    u=set(x for p in parents for x in byidx[p] if x!='NONE')
    assert all(x in u for x in byidx[result] if x!='NONE'), (result,byidx[result],parents,u)
check_idx(86,14,32) # Alter-S = BlitzGreymon + CresGarurumon
check_idx(87,51,66) # Chaosmon = BanchoLeomon + Darkdramon
check_idx(88,48,83) # Millenniummon = Chimairamon + Mugendramon
check((15,'Chaosdramon'), ((15,'Mugendramon'),(15,'HiAndromon')))

print(f'Digimon explicit typing OK: {dual}/458 dual typed, all 18 types covered, Jogress material mixing guarded')
