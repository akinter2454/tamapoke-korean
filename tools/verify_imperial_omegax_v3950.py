#!/usr/bin/env python3
from pathlib import Path
import json,re
from tamapoke_version import require_semver
r=Path(__file__).resolve().parents[1]
cpp=(r/'digimon.cpp').read_text(encoding='utf-8')
h=(r/'digimon.h').read_text(encoding='utf-8')
ino=(r/'TamaPoke.ino').read_text(encoding='utf-8')
rows=[m.groups() for m in re.finditer(r'D\("([^"]+)",(\d+),(\d+),(\d+),(\d+)\)',cpp)]
FW_VERSION = require_semver(r, "3.95.0")
assert len(rows)==458
assert rows[456]==('Imperialdramon Paladin Mode','22','5','225','1')
assert rows[457]==('Imperialdramon OmegaX','22','5','255','0')
assert 'if(cur.version==22&&!strcmp(n,"Imperialdramon Paladin Mode")&&lv>=70&&a+s>=100)return target("Imperialdramon OmegaX");' in cpp
assert '!strcmp(n,"Imperialdramon Paladin Mode");' in cpp
assert 'if(!strcmp(n,"Imperialdramon Paladin Mode"))return 70;' in cpp
assert 'Imperialdramon OmegaX' in ino and '공격/스피드 합 100' in ino
types=json.loads((r/'data/digimon/types.json').read_text(encoding='utf-8'))['entries']
assert len(types)==458 and types[457]['name']=='Imperialdramon OmegaX'
assert types[457]['type1']=='DRAGON' and types[457]['type2']=='STEEL'
assert '돌봄실수' not in cpp
print(f'v{FW_VERSION} Imperialdramon OmegaX OK: ID457, Paladin Lv70 + ATK/SPE 100, DRAGON/STEEL, no care gate')
