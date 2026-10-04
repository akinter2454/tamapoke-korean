#!/usr/bin/env python3
import re
from pathlib import Path
from tamapoke_version import require_semver
r=Path(__file__).resolve().parents[1]
ino=(r/'TamaPoke.ino').read_text(encoding='utf-8'); cpp=(r/'digimon.cpp').read_text(encoding='utf-8')
h=(r/'digimon.h').read_text(encoding='utf-8'); pet=(r/'pet.cpp').read_text(encoding='utf-8'); party=(r/'party.cpp').read_text(encoding='utf-8')
rows=re.findall(r'D\("([^"]+)",(\d+),(\d+),(\d+),(\d+)\)',cpp)
ko_block=cpp.split('static const char *const DIGI_NAMES_KO[] = {',1)[1].split('};',1)[0]
ko_names=re.findall(r'"([^"]+)"',ko_block)
FW_VERSION = require_semver(r)
assert len(rows)==458
assert len(ko_names)>=90 and all(re.search(r'[가-힣]',name) for name in ko_names[:90])
assert '#include "pendulum_species.inc"' not in cpp
assert '#include "pendulum_names_ko.inc"' not in cpp
assert len(rows)==458 and len(ko_names)==458
assert rows[457][0]=='Imperialdramon OmegaX' and ko_names[457]=='황제드라몬 오메가X'
assert 'return digimonNameKoShort(digimonIndex(id));' in cpp
assert 'DIGI_SPECIES[id].name:"???"' not in ino
assert 'DIGI_CREATURE_BASE = 2000' in h and 'isCreatureId' in h and 'DIGI_DEVICE_SLOT_COUNT = 18' in h and 'isDmulVersion' in h
assert 'setDigimonVersion' in pet and 'eggSource' in pet and 'eggShiny = (random(shinyBase) == 0);' in pet
assert 'digimonEvolutionTarget' in pet and 'trAtk,trDef,trSpe,trHp' in pet
assert 'creatureBaseAtk' in party and 'isCreatureId(m.dex)' in party
assert 'creatureHasArt(pet.speciesId)' in ino
assert 'else if (i == 5) { digiDexOpen = true' in ino
assert 'digiPet.begin();' not in ino and 'digiPet.update(now);' not in ino
assert 'pet.digiRegisteredCount()' in ino and 'D%02u-%02u' in ino
assert '"/digimon/d%03u.dgi"' in ino and 'dgi3=!memcmp(h,"DGI3",4)' in ino
assert 'digimonDefaultMoves' in cpp and 'digimonMovesNeedRefresh' in cpp
assert 'if (isDigimonId(dex)) return digimonLearnableMoves' in ino
assert 'moves[0]=MV_TACKLE; moves[1]=(uint8_t)(MV_DIGI_PULSE' not in pet
assert 'digimonDefaultMoves(next,level()' in pet
assert 'digimonMovesNeedRefresh(m.moves)' in party
print('unified Digimon system OK: 458 species, shared Pet/party/box/battle IDs, DMC/Pendulum + 7 DMUL DigiTama, separate dex')
