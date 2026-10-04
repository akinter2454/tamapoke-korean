#!/usr/bin/env python3
"""Fail CI when a tamapoke NVS key written by firmware is missing from SAVE_FIELDS.

The CRC A/B journals (bankA/bankB and c0a..c4b) are deliberately not exported:
portable legacy mirrors party/box/care0..care4 are exported and rebuild those
journals on the next boot. tamapoke_guard is a derived recovery shadow and is
also deliberately excluded; saveImport clears it before restoring.
"""
from pathlib import Path
import re, sys

ROOT = Path(__file__).resolve().parent.parent
SAVE = (ROOT / 'save.cpp').read_text(encoding='utf-8')
SAVE_KEYS = set(re.findall(r'\{\s*"([^"]+)"\s*,\s*SK_', SAVE))

# Only files that open/write the main `tamapoke` namespace.
FILES = ['audio.cpp', 'care_slots.cpp', 'game_extras.cpp', 'i18n.cpp', 'party.cpp', 'pet.cpp']
PUT = re.compile(r'\bput(?:UChar|Char|Bool|UShort|Short|UInt|Bytes|String)\s*\(\s*"([^"]+)"')
written = set()
for name in FILES:
    text = (ROOT / name).read_text(encoding='utf-8')
    written.update(PUT.findall(text))

# pet.cpp also writes this one literal through a Preferences object opened on
# `tamapoke_guard`, not the normal save namespace.
written.discard('progress')

# Dynamic keys are checked through their portable mirrors instead.
required_portable = {'party', 'box', 'care0', 'care1', 'care2', 'care3', 'care4'}
missing = sorted((written | required_portable) - SAVE_KEYS)

# These high-value fields used to be the silent backup gap that motivated this
# guard. Keep the assertion explicit so refactors cannot accidentally weaken it.
critical = {
    'thp','lvmin','lvslp','egsrc','digreg','digbest','digmat','digmv','digbmv','pmflgv','hunt',
    'caretx','carefrom','careto','btnfix38','btnfix39',
    # legacy read-only keys are needed for a lossless immediate backup after
    # upgrading a very old save, before canonical replacement keys are written.
    'gatk','gdef','gspe','spec','eggT'
}
missing_critical = sorted(critical - SAVE_KEYS)

if missing or missing_critical:
    if missing:
        print('BACKUP VERIFY FAIL: tamapoke write keys missing from SAVE_FIELDS:')
        for k in missing: print(' -', k)
    if missing_critical:
        print('BACKUP VERIFY FAIL: critical backup keys missing:')
        for k in missing_critical: print(' -', k)
    sys.exit(1)

print(f'BACKUP VERIFY OK: {len(SAVE_KEYS)} SAVE_FIELDS cover {len(written)} literal tamapoke writes')
print('Portable mirrors cover party/box and all five care slots; A/B journals rebuild after import.')
