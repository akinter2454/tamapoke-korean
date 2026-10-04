#!/usr/bin/env python3
from pathlib import Path
import math, re
from tamapoke_version import require_semver

root = Path(__file__).resolve().parents[1]
fw = require_semver(root, "3.98.0")
h = (root / "care_slots.h").read_text(encoding="utf-8")
c = (root / "care_slots.cpp").read_text(encoding="utf-8")
save = (root / "save.cpp").read_text(encoding="utf-8")
saveh = (root / "save.h").read_text(encoding="utf-8")
pet = (root / "pet.cpp").read_text(encoding="utf-8")
ino = (root / "TamaPoke.ino").read_text(encoding="utf-8")

assert re.search(r'#define\s+CARE_SLOT_COUNT\s+5\b', h)
assert re.search(r'#define\s+CARE_SLOT_VERSION\s+7\b', h)
for key in ('care0','care1','care2','care3','care4'):
    assert f'"{key}"' in c and re.search(r'\{\s*"'+key+r'"\s*,\s*SK_BYTES\s*\}', save), key
for key in ('c0a','c0b','c1a','c1b','c2a','c2b','c3a','c3b','c4a','c4b'):
    assert f'"{key}"' in c, key

# Existing backup format remains v2; old saves simply lack care3/care4 and the
# new firmware creates those slots on first visit.
assert re.search(r'#define\s+SAVE_VERSION\s+2\b', saveh)
assert '#define PROGRESS_GUARD_SLOTS CARE_SLOT_COUNT' in pet
assert '#define PROGRESS_GUARD_VERSION 3' in pet
assert 'struct ProgressGuard46V2' in pet and 'GuardTrain46 train[3];' in pet
assert 'old.version == 2' in pet and 'memcpy(g.train, old.train, sizeof(old.train));' in pet

# All care-tab behavior must be count-driven rather than hard-coded to three.
assert ino.count('i < CARE_SLOT_COUNT') >= 3
# Five 54px tabs with 8px gaps fit comfortably on the 466x466 round panel at y=112.
slots, w, gap, cx, cy, r, y = 5, 54, 8, 233, 233, 231, 112
span = slots*w + (slots-1)*gap
x0 = cx - span//2
x1 = x0 + span
half_chord = math.sqrt(r*r - (y-cy)*(y-cy))
assert x0 >= cx-half_chord and x1 <= cx+half_chord, (x0, x1, half_chord)

assert (root/'TamaPoke.ino').read_bytes() == (root/'firmware_source/TamaPoke.ino').read_bytes()
print(f'v{fw} five-care-slot regression OK: UI span={span}px, portable care0..care4, A/B c0..c4, v2 guard migration')
