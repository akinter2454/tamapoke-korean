#!/usr/bin/env python3
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
ino=(ROOT/'TamaPoke.ino').read_text(encoding='utf-8')
h=(ROOT/'game_extras.h').read_text(encoding='utf-8')
cpp=(ROOT/'game_extras.cpp').read_text(encoding='utf-8')
save=(ROOT/'save.cpp').read_text(encoding='utf-8')

def need(ok,msg):
    if not ok: raise SystemExit('FAIL: '+msg)
enum=h[h.index('enum ExtraItemId'):h.index('enum MissionKind')]
order=['XITEM_GOLD_CROWN','XITEM_SHINY_BERRY','XITEM_TRAIN','XITEM_CARE','XITEM_IV','XITEM_COUNT']
pos=[re.search(r'\b'+re.escape(x)+r'\b', enum).start() for x in order]
need(pos == sorted(pos) and len(set(pos)) == len(pos), 'compact items are not append-only after legacy IDs')
need('migrateCompactItems = itemStored > 0 && itemStored < sizeof(_items)' in cpp, 'one-time blob-length migration missing')
for tok in ['_items[XITEM_TRAIN]', '_items[XITEM_CARE]', '_items[XITEM_IV]']:
    need(tok in cpp, 'migration missing '+tok)
need('case XITEM_TRAIN:' in cpp and 'case XITEM_CARE:' in cpp and 'case XITEM_IV:' in cpp, 'compact item effects missing')
need('const uint8_t page0[4] = { XITEM_TRAIN, XITEM_CARE, XITEM_IV, XITEM_GOLD_CROWN }' in ino,
     'compact bag page 1 mapping missing')
need('const uint8_t page1[4] = { XITEM_SHINY, XITEM_SHINY_BERRY, XITEM_COUNT, XITEM_COUNT }' in ino,
     'compact bag page 2 mapping missing')
need('bagCompactChoice==1?XITEM_TRAIN:XITEM_IV' in ino, 'stat selector does not use consolidated items')
need('uint8_t pages = bagTab == 0 ? 2 : 5;' in ino, 'earned item bag was not reduced to two pages')
need('uint8_t id = XITEM_IV;' in ino and 'count = random(100) < 30 ? 9 : 5;' in ino,
     'training does not award compact IV berries')
need('{ "xitem", SK_BYTES }' in save, 'inventory blob missing from backup whitelist')
# New reward pools should no longer create legacy growth/IV items.
reward_tail=cpp[cpp.index('void GameExtras::rollMissions'):]
for old in ['COMMON[5] = { XITEM_ATK', 'GROWTH[5] = { XITEM_ATK', '(uint8_t)(XITEM_IV_ATK + random(4))']:
    need(old not in reward_tail, 'legacy item still generated: '+old)
print('PASS: compact six-item inventory, one-time migration, selectable training/IV items')
