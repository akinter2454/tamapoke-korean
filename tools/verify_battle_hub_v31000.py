#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ino=(ROOT/'TamaPoke.ino').read_text(encoding='utf-8')

def need(ok,msg):
    if not ok: raise SystemExit('FAIL: '+msg)

need('bool battleHubOpen = false;' in ino, 'battle hub state missing')
need('void renderBattleHub()' in ino and 'void battleHubTap(int16_t x, int16_t y)' in ino, 'battle hub renderer/touch missing')
need('case 3: snprintf(out, n, "배틀 허브")' in ino, 'main menu does not route to battle hub')
for label in ['체육관','3마리 타입 보스','배틀 타워','라이벌 트레이너']:
    need(label in ino[ino.index('void renderBattleHub() {'):ino.index('void renderAdventure() {')], f'battle hub missing {label}')
need('if (dir < 0) { battleHubOpen = true; }' in ino, 'home left swipe does not open battle hub')
need('bossOpen = false; battleHubOpen = true' in ino, 'boss does not return to battle hub')
need('uiDrawCenteredFit("배틀 허브", CX, 388' in ino, 'gym list still duplicates LAN instead of returning to hub')
region=ino[ino.index('static void renderRegionPick(uint8_t mode) {'):ino.index('// The region pill under a waiting egg') ]
need('gfx->print(T(S_LAN))' not in region, 'gym region chooser still duplicates LAN')
need('towerOpen = false; battleHubOpen = true' in ino, 'tower does not return to battle hub')
need('rivalOpen=false;battleHubOpen=true' in ino or 'rivalOpen = false; battleHubOpen = true' in ino, 'rival does not return to battle hub')
adv=ino[ino.index('void renderAdventure() {'):ino.index('void renderExplore() {')]
need('타입 탐험' in adv and '보물지도' in adv, 'compact adventure sub-hub missing')
need('3마리 타입 보스' not in adv and '배틀 타워' not in adv and '라이벌 트레이너' not in adv,
     'battle entries are still duplicated in adventure screen')
print('PASS: unified battle hub + compact exploration/treasure sub-hub')
