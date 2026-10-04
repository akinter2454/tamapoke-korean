#!/usr/bin/env python3
"""Keep all user-facing Digimon sprite tools aligned with the 458-species firmware catalog."""
from pathlib import Path
import json
import re
from tamapoke_version import require_semver

root = Path(__file__).resolve().parents[1]
fw = require_semver(root, '3.96.2')
tools = root / 'tools'
cpp = (root / 'digimon.cpp').read_text(encoding='utf-8')
catalog = [(name, int(v), int(st)) for name, v, st in re.findall(
    r'D\("([^"]+)",(\d+),(\d+),\d+,\d+\)', cpp
)]
assert len(catalog) == 458, len(catalog)

latest_pack = tools / 'TamaPoke-Digimon-SD-Pack-Maker-v3.96.2-r18-458.html'
canonical_pack = tools / 'Digimon-SD-Pack-Maker.html'
legacy_pack = tools / 'Digimon-Pendulum-DMUL-SD-Pack-Maker-v3.87.0.html'
for p in (latest_pack, canonical_pack, legacy_pack):
    assert p.exists(), p
assert canonical_pack.read_bytes() == latest_pack.read_bytes(), 'canonical pack maker drift'
assert legacy_pack.read_bytes() == latest_pack.read_bytes(), 'legacy pack-maker alias drift'

s = canonical_pack.read_text(encoding='utf-8')
m = re.search(r"let CAT=`(.*?)`\.trim\(\)\.split\('\\n'\)", s, re.S)
assert m, 'CAT table not found in pack maker'
pack_catalog = []
for line in m.group(1).splitlines():
    name, v, st = line.split('|')
    pack_catalog.append((name, int(v), int(st)))
assert pack_catalog == catalog, 'pack maker CAT does not exactly match digimon.cpp'
assert 'CAT.length!==458' in s and "CAT[457]?.name!=='Imperialdramon OmegaX'" in s

latest_down = tools / 'TamaPoke-DMUL-Expanded-Sprite-Downloader-v3.96.2-r14.html'
canonical_down = tools / 'DMC-DMUL-Required-Sprite-Downloader.html'
assert latest_down.exists() and canonical_down.exists()
assert canonical_down.read_bytes() == latest_down.read_bytes(), 'canonical downloader drift'
d = canonical_down.read_text(encoding='utf-8')
m = re.search(r'const ROSTER=(\[.*?\]);', d, re.S)
assert m, 'downloader ROSTER table not found'
rows = json.loads(m.group(1))
assert [int(x['id']) for x in rows] == list(range(283, 458))
for row in rows:
    i = int(row['id'])
    assert (row['name'], int(row['v']), int(row['s'])) == catalog[i], (i, row, catalog[i])

print(f'v{fw} Digimon sprite tools OK: 458-entry pack maker + 175-entry DMUL downloader stay catalog-aligned')
