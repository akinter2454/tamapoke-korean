#!/usr/bin/env python3
from pathlib import Path
import re, sys
ROOT=Path(__file__).resolve().parents[1]
src=(ROOT/'TamaPoke.ino').read_text(encoding='utf-8')
mir=(ROOT/'firmware_source'/'TamaPoke.ino').read_text(encoding='utf-8')
ph=(ROOT/'party.h').read_text(encoding='utf-8')
pc=(ROOT/'party.cpp').read_text(encoding='utf-8')
wf=(ROOT/'.github/workflows/main.yml').read_text(encoding='utf-8')
saveh=(ROOT/'save.h').read_text(encoding='utf-8')
checks={
 'firmware v3.106.0+': bool((m:=re.search(r'^#define\s+FW_VERSION\s+"(\d+)\.(\d+)\.(\d+)"',src,re.M))) and tuple(map(int,m.groups())) >= (3,106,0),
 'damage popup uses TurnLog damage':all(k in src for k in ['struct BattleDamagePopup','fx.amount = lg.damage','btlQueueDamageFx(targetWho, lg)','btlDrawDamageFx(1, 348, 126)','btlDrawDamageFx(0, 124, 238)']),
 'critical/effect tags':all(k in src for k in ['"CRIT!"','"SUPER"','"RESIST"']),
 'fresh wild dex card':all(k in src for k in ['btlArmDexNew','"NEW! 도감 등록"','registerWildVictory(btlWildDex)','if (fresh) btlArmDexNew']),
 'digimon material confirmation':'"조그레스 소재도 등록 완료"' in src,
 'party lock append only':re.search(r'uint8_t trHp\s*=\s*0;.*?uint8_t flags\s*=\s*0;',ph,re.S) is not None and 'PMON_LOCKED' in ph,
 'lock sanitization':'m.flags &= PMON_LOCKED;' in pc,
 'legacy lock padding migration':all(k in pc for k in ['pmflgv','migrateProtection','clearProtectionFlags(slots, box)','prefs.putUChar("pmflgv",1)']),
 'lock blocks release':src.count('.locked()') >= 8 and '"잠금됨"' in src,
 'box compact filters':all(k in src for k in ['"전체"','"포켓몬"','"디지몬"','"Shiny"','"잠금"','boxVisibleIndex','boxPageCount']),
 'deposit forces all filter':'static uint8_t boxEffectiveFilter() { return boxSwapFrom ? 0' in src,
 'five slot summary':all(k in src for k in [('#define PLAYER_PAGES (GYM_REGIONS + 2)' if '#define PLAYER_PAGES (GYM_REGIONS + 2)' in src else '#define PLAYER_PAGES (GYM_REGIONS + 3)'),'renderCareSummary','"육성 슬롯 요약"','CARE_SLOT_COUNT']),
 'summary is view only':'자동 돌보기 없이 상태만 확인합니다' in src,
 'jogress visual preview':all(k in src for k in ['drawJogressPreviewPanel','"조그레스 미리보기"','pet.isDigiRegistered(jt)','!seen']),
 'jogress keeps touch boxes':all(k in src for k in ['CONFIRM_B1_Y','CONFIRM_B2_Y','uiConfirmRects']),
 'battle retry helper':all(k in src for k in ['btlCanRetryNow','btlRetryCurrent','drawBattleResultButtons','"재도전"','"허브로"']),
 'wild retry only after loss':'if (btlWild) return !btlWon && isCreatureId(btlWildDex);' in src,
 'shared result hub exit':all(k in src for k in ['btlLeaveResultToHub','audioMusic(MUS_NONE);','bossOpen = true;','towerOpen = true;']),
 'protection marker portable': '{ "pmflgv", SK_U8 }' in (ROOT/'save.cpp').read_text(encoding='utf-8'),
 'save schema unchanged':'#define SAVE_VERSION 2' in saveh,
 'source mirror exact':src==mir,
 'workflow runs verifier':'verify_battle_qol_v31060.py' in wf,
}
bad=[]
for name,ok in checks.items():
    print(('PASS' if ok else 'FAIL')+': '+name)
    if not ok: bad.append(name)
if bad:
    print(f'FAILED {len(bad)} checks: {bad}',file=sys.stderr);sys.exit(1)
print(f'OK: {len(checks)} v3.106.0 battle/QoL checks')
