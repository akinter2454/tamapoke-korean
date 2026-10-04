#!/usr/bin/env python3
from pathlib import Path
import re

R=Path(__file__).resolve().parents[1]
ino=(R/'TamaPoke.ino').read_text(encoding='utf-8')
pet_h=(R/'pet.h').read_text(encoding='utf-8')
pet=(R/'pet.cpp').read_text(encoding='utf-8')
dh=(R/'digimon.h').read_text(encoding='utf-8')
dc=(R/'digimon.cpp').read_text(encoding='utf-8')
save=(R/'save.cpp').read_text(encoding='utf-8')
saveh=(R/'save.h').read_text(encoding='utf-8')

m=re.search(r'^#define\s+FW_VERSION\s+"(\d+)\.(\d+)\.(\d+)"',ino,re.M)
assert m and tuple(map(int,m.groups())) >= (3,101,0), 'FW_VERSION must be >= 3.101.0'
assert re.search(r'#define\s+SAVE_VERSION\s+2\b',saveh), 'SAVE_VERSION changed'

# UI/menu and encounter rules.
for token in ['bool wildOpen = false;', '"야생 대면"', 'renderWildEncounter()', 'wildEncounterTap', 'startWildBattle']:
    assert token in ino, f'missing wild UI token: {token}'
assert 'speciesHasArt(d) && !pet.isRegistered(d)' in ino, 'Pokemon pool must be unregistered + drawable only'
assert '!pet.isDigiRegistered(d)' in ino, 'Digimon pool must be unregistered only'
assert 'openLocalBattlePicker(PICK_WILD,3)' in ino, 'wild battle must enter the common team picker'
assert 'buildLocalSquad(0,3,squadMask)' in ino, 'wild battle should keep a selected compact 3-member player cap'
assert 'pet.registerWildVictory(btlWildDex)' in ino, 'wild win must register discovery'
assert 'wildCandidate = 0;' in ino and 'wildMode = 0;' in ino, 'victory should clear the encounter and return to chooser'

# Player-wide discovery/material state. It is a distinct bitset, not fake best-level data.
assert 'uint8_t digiWildMaterial[(DIGI_SPECIES_CAP + 7) / 8]' in pet_h
assert 'bool isDigiWildMaterial(uint16_t id) const' in pet_h
assert 'bool Pet::registerWildVictory(int16_t dex)' in pet
method=pet[pet.index('bool Pet::registerWildVictory'):pet.index('\n}',pet.index('bool Pet::registerWildVictory'))+2]
assert 'digiReg[i >> 3] |= mask;' in method
assert 'digiWildMaterial[i >> 3] |= mask;' in method
assert 'digiBest[' not in method, 'wild registration must not falsify highest raised level'
assert 'prefs.putBytes("digmat"' in pet and 'loadBlob(prefs, "digmat"' in pet
assert '{ "digmat", SK_BYTES }' in save, 'digmat missing from portable backup fields'

# Jogress partner qualification accepts the wild-material registry, while normal evolution does not.
assert 'const uint8_t *wildMaterials = nullptr' in dh
assert 'digiWildMaterial(uint16_t material,const uint8_t*wildMat)' in dc
assert 'digiQualified' in dc and 'digiWildMaterial(material,wildMat)' in dc
assert 'digimonJogressTarget(i,level(),trAtk,trDef,trSpe,trHp,digiBest,digiWildMaterial)' in pet
assert 'digimonEvolutionTarget(i,level(),trAtk,trDef,trSpe,trHp,digiBest)' in pet, 'normal evolution history must remain unchanged'

# Firmware mirror invariant.
assert (R/'TamaPoke.ino').read_bytes()==(R/'firmware_source/TamaPoke.ino').read_bytes(), 'firmware source mirror differs'
print('v3.101.0 wild encounter OK: unregistered-only pools, victory discovery, Digimon Jogress material unlock, SAVE_VERSION 2')
