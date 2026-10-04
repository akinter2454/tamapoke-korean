#!/usr/bin/env python3
from pathlib import Path
import re
from tamapoke_version import require_semver
r=Path(__file__).resolve().parents[1]
cpp=(r/'digimon.cpp').read_text(encoding='utf-8')
h=(r/'digimon.h').read_text(encoding='utf-8')
pet=(r/'pet.cpp').read_text(encoding='utf-8')
ino=(r/'TamaPoke.ino').read_text(encoding='utf-8')
FW_VERSION = require_semver(r, "3.94.2")
# Digimon routing API must not receive or inspect the care-mistake counter.
assert 'careMistakes' not in cpp, 'digimon.cpp still depends on careMistakes'
assert 'careMistakes' not in h, 'digimon.h still exposes careMistakes in Digimon evolution API'
assert 'digimonEvolutionTarget(i,level(),trAtk,trDef,trSpe,trHp,digiBest)!=i;' in pet
assert 'digimonEvolutionTarget(old,level(),trAtk,trDef,trSpe,trHp,digiBest);' in pet
assert '돌봄실수' not in ino[ino.index('static const char*digiDexRule'):ino.index('if(isDmulVersion',ino.index('static const char*digiDexRule'))], 'Digimon dex rule still advertises care-mistake evolution conditions'
# Positive conditions retained after removing care gates.
for token in [
 'lv>=60&&a+s>=80',
 'lv>=60&&a+s>=90',
 'lv>=45&&(a+d+s+h)>=70',
 'lv>=60&&a+h>=90',
 'lv>=70&&a+s>=100',
]:
    assert token in cpp, token
print(f'v{FW_VERSION} no-care-mistake Digimon evolution OK')
