#!/usr/bin/env python3
"""Regression guards for the v3.96.2 stabilization sweep."""
from pathlib import Path
import re
from tamapoke_version import require_semver

root = Path(__file__).resolve().parents[1]
fw = require_semver(root, '3.96.2')
ino = (root/'TamaPoke.ino').read_text(encoding='utf-8')
cpp = (root/'digimon.cpp').read_text(encoding='utf-8')
pet = (root/'pet.cpp').read_text(encoding='utf-8')
pet_h = (root/'pet.h').read_text(encoding='utf-8')
workflow = (root/'.github/workflows/main.yml').read_text(encoding='utf-8')

# Evolution potential must distinguish normal routes from Jogress routes.
for token in [
    'digimonHasNormalEvolutionPotential', 'digimonHasJogressPotential',
    'digimonJogressLevel',
    'return digimonHasNormalEvolutionPotential(i)||digimonHasJogressPotential(i);'
]:
    assert token in cpp, token

m = re.search(r'bool digimonHasEvolutionPotential\(uint16_t i\)\{(.*?)\n\}', cpp, re.S)
assert m and 'version>=10' not in m.group(1) and 'version<=15' not in m.group(1), 'blanket Pendulum Ultimate potential returned'

# Known true final forms must not be advertised as generic normal/Jogress sources.
pend = re.search(r'static bool pendulumJogressSource\(uint16_t i\)\{(.*?)\n\}', cpp, re.S)
normal = re.search(r'static bool dmulUltimateNormalSource\(const char\*n\)\{(.*?)\n\}', cpp, re.S)
assert pend and normal
for name in ['Diarbbitmon','HerakleKabuterimon','Blastmon','Holydramon','Amphimon','Vikemon','Rosemon','Ragnamon','Quantumon']:
    assert f'"{name}"' not in pend.group(1), f'{name} incorrectly flagged as Jogress source'
    assert f'"{name}"' not in normal.group(1), f'{name} incorrectly flagged as normal-special source'

# Progress card communicates Digimon-specific rules instead of Pokemon care text.
for text in [
    '일반 진화 / 조그레스 가능', '조그레스 상대 육성 기록 필요',
    '돌봄 실수 %u · 진화 무관'
]:
    assert text in ino, text

# Declining evolution is immediately checkpointed.
dec = re.search(r'void Pet::declineEvolve\(\)\s*\{(.*?)\n\}', pet, re.S)
assert dec and 'evoDeclinedLv = level();' in dec.group(1) and 'save();' in dec.group(1)
assert 'void declineEvolve();' in pet_h

# Confirmation dialogs are modal against both swipe directions.
for fn in ['onSwipeV', 'onSwipe']:
    mm = re.search(rf'(?:static\s+)?void\s+{fn}\([^)]*\)\s*\{{(.*?)\n\}}', ino, re.S)
    assert mm and 'if (choiceKind) return;' in mm.group(1)[:300], f'{fn} modal guard missing'

# Missing/corrupt DGI must have a common visible placeholder in major scenes.
assert 'static void drawDigiMissingGlyph' in ino
assert ino.count('drawDigiMissingGlyph(') >= 7, ino.count('drawDigiMissingGlyph(')
for area_hint in ['SD 도트 없음', 'loadBattleDigi', 'drawDigiEvolutionForm']:
    assert area_hint in ino, area_hint

# GitHub CI already compiles the ESP32-S3 firmware; guard against accidentally losing it.
assert 'arduino-cli compile' in workflow
assert 'esp32:esp32:esp32s3:' in workflow
assert 'TamaPoke.ino' in workflow

# Version-sensitive verifiers should use the shared semantic helper instead of matching one current literal.
verifiers = list((root/'tools').glob('verify_*.py'))
for p in verifiers:
    if p.name == Path(__file__).name:
        continue
    s = p.read_text(encoding='utf-8')
    assert '#define FW_VERSION \"3.96.1\"' not in s, p.name
    assert '#define FW_VERSION \"3.96.2\"' not in s, p.name

print(f'v{fw} runtime stabilization OK: evolution status, persistence, modal input, DGI fallback, compile-CI guard')
