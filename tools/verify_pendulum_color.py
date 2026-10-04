from pathlib import Path
import re
from tamapoke_version import require_semver

root=Path(__file__).resolve().parents[1]
cpp=(root/'digimon.cpp').read_text()
inc=(root/'pendulum_species.inc').read_text()
ko=(root/'pendulum_names_ko.inc').read_text()
h=(root/'digimon.h').read_text()
pet=(root/'pet.cpp').read_text()
ino=(root/'TamaPoke.ino').read_text()
html=(root/'tools/Digimon-SD-Pack-Maker.html').read_text()

rows=re.findall(r'D\("([^"]+)",(\d+),(\d+),(\d+),(\d+)\)',inc)
assert len(rows)==193, len(rows)
versions={int(r[1]) for r in rows}
assert versions=={10,11,12,13,14,15}, versions
assert len(re.findall(r'^\s*"[^"]+",?$',ko,re.M))==193
assert 'const uint16_t DIGI_SPECIES_COUNT' in cpp
assert 'DIGI_SPECIES_CAP = 2048' in h
assert 'uint8_t digiBest[DIGI_SPECIES_CAP]' in (root/'pet.h').read_text()
assert 'REGION_COUNT + DIGI_DEVICE_SLOT_COUNT' in pet and 'GAL_REGIONS+DIGI_DEVICE_SLOT_COUNT' in ino
assert 'P%u-%02u' in ino and 'digimonDeviceLabel' in ino
for name in ('Omegamon','Mastemon','Proximamon','Mitamamon','Cernumon','Chaosdramon'):
    assert name in cpp
assert 'pendulumFusionTarget' in cpp and 'best[material]' in cpp
assert 'data[4]!==(id&255)' in html and 'folderVersion' in html
assert 'dmc1~5, p0~p5, DMUL' in html
FW_VERSION = require_semver(root)
print('Pendulum COLOR OK: P0-P5 preserved; device picker extended safely for seven DMUL DigiTama')
