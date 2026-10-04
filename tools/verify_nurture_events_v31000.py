#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ino=(ROOT/'TamaPoke.ino').read_text(encoding='utf-8')
h=(ROOT/'game_extras.h').read_text(encoding='utf-8')
cpp=(ROOT/'game_extras.cpp').read_text(encoding='utf-8')

def need(ok,msg):
    if not ok: raise SystemExit('FAIL: '+msg)
need('eventChoiceKo(uint8_t choice)' in h, 'event choice API missing')
need('resolveEvent(uint8_t choice, Pet &pet' in h, 'event resolution API missing')
need('const char *GameExtras::eventChoiceKo' in cpp and 'bool GameExtras::resolveEvent' in cpp, 'event choice implementation missing')
for token in ['pet.joy', 'pet.energy', 'pet.bond', 'pet.trAtk', 'pet.trHp']:
    need(token in cpp[cpp.index('bool GameExtras::resolveEvent'):cpp.index('void GameExtras::claimEvent')], f'nurture consequence missing: {token}')
need('extras.resolveEvent(choice, pet, eventResultText' in ino, 'touch does not resolve chosen event')
need('extras.eventChoiceKo(0)' in ino and 'extras.eventChoiceKo(1)' in ino, 'two event choices not rendered')
need('eventResultUntil = millis() + 3200' in ino, 'event outcome feedback banner missing')
need('_lastEventMinute + 20' in cpp and 'pers == PERS_LUCKY ? 50 : 35' in cpp, 'existing event cadence changed unexpectedly')
print('PASS: choice-based random nurture events with persistent cadence and feedback')
