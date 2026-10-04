#!/usr/bin/env python3
"""Regression guard for the global casual energy balance."""
from pathlib import Path
import re
from tamapoke_version import require_semver

root = Path(__file__).resolve().parents[1]
ino = (root / 'TamaPoke.ino').read_text(encoding='utf-8')
h = (root / 'pet.h').read_text(encoding='utf-8')
cpp = (root / 'pet.cpp').read_text(encoding='utf-8')

FW_VERSION = require_semver(root)
expected = {
    'ENERGY_SLEEP_RECOVERY': 10,
    'ENERGY_AWAKE_DECAY_MINUTES': 15,
    'ENERGY_OVERWEIGHT_DECAY_MINUTES': 30,
    'ENERGY_DEF_BASE_COST': 1,
    'ENERGY_DEF_SCORE_DIVISOR': 24,
    'ENERGY_DEF_MAX_COST': 4,
    'ENERGY_ATK_COST': 2,
    'ENERGY_SPE_COST': 1,
    'ENERGY_HP_COST': 1,
    'ENERGY_PLAY_COST': 1,
}
for name, value in expected.items():
    assert re.search(rf'^#define {name} {value}$', h, re.M), (name, value)

# Live sleep, power-off catch-up and inactive care-slot catch-up must all use
# the same fast recovery. Awake drain is deliberately much slower, while the
# overweight surcharge has its own still-slower cadence.
assert cpp.count('energy = clamp100(energy + ENERGY_SLEEP_RECOVERY);') == 3
assert cpp.count('ageMinutes % ENERGY_AWAKE_DECAY_MINUTES == 0') == 3
assert cpp.count('ageMinutes % ENERGY_OVERWEIGHT_DECAY_MINUTES == 0') == 2
assert 'energy = clamp100(energy + 6);' not in cpp

assert 'min<uint16_t>(ENERGY_DEF_MAX_COST, ENERGY_DEF_BASE_COST + score / ENERGY_DEF_SCORE_DIVISOR)' in cpp
assert 'dropTo(energy, ENERGY_ATK_COST, 8)' in cpp
assert 'dropTo(energy, ENERGY_SPE_COST, 8)' in cpp
assert 'dropTo(energy, ENERGY_HP_COST, 8)' in cpp
assert 'clamp100(energy - ENERGY_PLAY_COST)' in cpp
extras = (root / 'game_extras.cpp').read_text(encoding='utf-8')
assert 'pet.energy + 70' in extras
assert 'pet.energy > 2) pet.energy -= 2' in extras
assert 'pet.energy > 3 ? pet.energy - 3 : 0' in extras
assert 'pet.energy = pet.energy > 2 ? pet.energy - 2 : 0' in extras

print('casual energy OK: 15-min awake drain, 30-min overweight surcharge, lower activity/event costs, 10/min sleep recovery')
