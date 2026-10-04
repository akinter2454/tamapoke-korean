#!/usr/bin/env python3
from pathlib import Path
import re
R=Path(__file__).resolve().parents[1]
ino=(R/'TamaPoke.ino').read_text(encoding='utf-8')
mirror=(R/'firmware_source'/'TamaPoke.ino').read_text(encoding='utf-8')
care=(R/'care_slots.h').read_text(encoding='utf-8')
saveh=(R/'save.h').read_text(encoding='utf-8')

def fn(sig):
    i=ino.find(sig)
    assert i>=0, f'missing {sig}'
    b=ino.find('{',i); d=0
    for j in range(b,len(ino)):
        if ino[j]=='{': d+=1
        elif ino[j]=='}':
            d-=1
            if d==0: return ino[b+1:j]
    raise AssertionError(f'unterminated {sig}')

m=re.search(r'^#define\s+FW_VERSION\s+"(\d+)\.(\d+)\.(\d+)"',ino,re.M)
assert m and tuple(map(int,m.groups())) >= (3,109,5)
assert re.search(r'#define\s+CARE_SLOT_COUNT\s+5\b',care)
assert re.search(r'#define\s+SAVE_VERSION\s+2\b',saveh), 'save layout/version changed'
assert ino==mirror, 'firmware mirror differs'

# All five raising slots are direct local candidates, not a 3-entry slice/page cap.
loc=fn('static bool localPickExists(uint8_t n) {')
assert 'n < CARE_SLOT_COUNT' in loc and 'careSlotDex(n)' in loc
render=fn('void renderPick() {')
assert 'const char *tabs[3] = { "육성", "파티", "박스" }' in render
assert '#define PICK_PER_PAGE 6' in ino, 'five care slots must fit one page'
assert 'slice(0, 3)' not in ino

# Fresh entry and retry both reset old cached selection.
op=fn('static void openLocalBattlePicker(uint8_t mode, uint8_t cap) {')
assert 'pickDefault(cap);' in op and 'pickSourceTab = 0' in op
assert 'squadMask = 0;' in fn('void pickDefault(uint8_t cap) {')
retry=fn('static void btlRetryCurrent() {')
assert 'openLocalBattlePicker(PICK_WILD, 3)' in retry
assert 'openLocalBattlePicker(PICK_BOSS, 3)' in retry
assert 'openLocalBattlePicker(PICK_TOWER, TRAINER_TEAM_MAX)' in retry
assert 'pickDefault(squadCapForRegion' in retry

# User-facing local battle modes all enter the same picker.
assert 'openLocalBattlePicker(PICK_WILD,3)' in fn('void wildEncounterTap(int16_t x,int16_t y){')
assert 'openLocalBattlePicker(PICK_BOSS,3)' in fn('void bossTap(int16_t x,int16_t y){')
assert 'openLocalBattlePicker(PICK_TOWER,TRAINER_TEAM_MAX)' in fn('void towerTap(int16_t x, int16_t y) {')
assert 'openLocalBattlePicker(PICK_RIVAL,3)' in fn('void rivalTap(int16_t x,int16_t y){')
assert 'pickDefault(squadCapForRegion' in ino, 'gym picker no longer initializes selection'

# Selected care slots become temporary combatants; storage is never switched/moved.
build=fn('static void buildLocalSquad(uint8_t maxLvl')
assert 'combatantFromCareSlot' in build
assert 'careSlots.switchTo' not in build and 'party.save' not in build
assert 'PICK_PARTY_BASE' in build and 'PICK_BOX_BASE' in build

print('v3.109.5 battle-team picker OK: five care slots visible, all main local battle entries select first, save/party/box layouts untouched')
