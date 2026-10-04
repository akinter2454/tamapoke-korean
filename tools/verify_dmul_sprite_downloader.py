#!/usr/bin/env python3
"""Static guard for the canonical DMUL expanded sprite downloader."""
from pathlib import Path
import json
import re

root = Path(__file__).resolve().parents[1]
p = root / 'tools' / 'DMC-DMUL-Required-Sprite-Downloader.html'
s = p.read_text(encoding='utf-8')

m = re.search(r'const ROSTER=(\[.*?\]);', s, re.S)
assert m, 'ROSTER table not found'
rows = json.loads(m.group(1))
assert len(rows) == 175, len(rows)
ids = [int(x['id']) for x in rows]
assert ids == list(range(283, 458)), (ids[:3], ids[-3:], len(ids))
assert len(set(ids)) == 175

# Canonical firmware catalog must stay aligned with the downloader IDs/names.
cpp = (root / 'digimon.cpp').read_text(encoding='utf-8')
catalog = [(name, int(v), int(st)) for name, v, st in re.findall(
    r'D\("([^"]+)",(\d+),(\d+),\d+,\d+\)', cpp
)]
assert len(catalog) == 458, len(catalog)
for row in rows:
    i = int(row['id'])
    assert row['name'] == catalog[i][0], (i, row['name'], catalog[i][0])
    assert int(row['v']) == catalog[i][1], (i, row['v'], catalog[i][1])
    assert int(row['s']) == catalog[i][2], (i, row['s'], catalog[i][2])

assert 'Source=DMUL' in s
assert "const RAW_BASE='https://raw.githubusercontent.com/tero0x/dmc-sprites/main/'" in s
assert "const CDN_BASE='https://cdn.jsdelivr.net/gh/tero0x/dmc-sprites@main/'" in s
assert "RAW_BASE+'sprites.json'" in s and "CDN_BASE+'sprites.json'" in s
assert 'function makeZip' in s and 'function normalizeAssetUrl' in s and 'function packFor' in s and 'function analyze' in s
for name in [
    'Guilmon', 'Dukemon Crimson Mode', 'Lilithmon', 'Gazimon', 'Patamon',
    'Imperialdramon Dragon Mode', 'Imperialdramon Paladin Mode', 'Imperialdramon OmegaX'
]:
    assert any(x['name'] == name for x in rows), name

print('DMUL sprite downloader OK: 175 contiguous IDs 283..457, catalog-aligned, online/local fallback and ZIP output')
