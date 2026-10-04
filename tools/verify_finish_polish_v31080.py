#!/usr/bin/env python3
from pathlib import Path
import re, sys
ROOT=Path(__file__).resolve().parents[1]
ino=(ROOT/'TamaPoke.ino').read_text(encoding='utf-8')
mir=(ROOT/'firmware_source/TamaPoke.ino').read_text(encoding='utf-8')
ac=(ROOT/'audio.cpp').read_text(encoding='utf-8')
ah=(ROOT/'audio.h').read_text(encoding='utf-8')
saveh=(ROOT/'save.h').read_text(encoding='utf-8')
wf=(ROOT/'.github/workflows/main.yml').read_text(encoding='utf-8')
inst=(ROOT/'TamaPoke-KO-OneClick-Installer.html').read_text(encoding='utf-8')
checks=[]
def ck(name, ok): checks.append((name,bool(ok)))

m=re.search(r'#define\s+FW_VERSION\s+"(\d+)\.(\d+)\.(\d+)"', ino)
ck('FW 3.108.0+', bool(m) and tuple(map(int,m.groups())) >= (3,108,0))
ck('SAVE_VERSION remains 2', re.search(r'#define\s+SAVE_VERSION\s+2\b', saveh) is not None)
# Macro declaration order: first real invocation after define, not macro line itself.
def_pos=ino.find('#define C565')
use_pos=ino.find('C565(', def_pos+1)
ck('C565 declared before use', def_pos >= 0 and use_pos > def_pos)

for sym in ['uiGamePageBase','uiGameCard','uiGameButton','uiGameBackHint']:
    ck(f'shared UI chrome {sym}', sym in ino)
ck('battle hub uses shared chrome', 'renderBattleHub()' in ino and 'uiGamePageBase("배틀 허브"' in ino)
ck('wild encounter uses shared chrome', 'renderWildEncounter()' in ino and 'uiGamePageBase("야생 대면"' in ino)
ck('party/box detail uses shared chrome', 'renderMonSheet' in ino and 'uiGamePageBase(head, nullptr' in ino)
ck('collection page uses shared cards', 'renderCollectionProgress' in ino and 'uiGameCard(' in ino)
ck('adventure/explore use shared chrome', 'uiGamePageBase("탐험·보물"' in ino and 'uiGamePageBase("타입 탐험"' in ino)
ck('boss/tower use shared chrome', 'uiGamePageBase("3마리 타입 보스"' in ino and 'uiGamePageBase("배틀 타워"' in ino)
ck('treasure/rival use shared chrome', 'uiGamePageBase("보물지도"' in ino and 'uiGamePageBase("라이벌 트레이너"' in ino)
ck('bag/missions use shared chrome', 'uiGamePageBase(title, nullptr' in ino and 'uiGamePageBase("오늘의 미션"' in ino)

ck('wild reveal timing state', all(x in ino for x in ['wildRevealStarted','wildRevealUntil','+1250UL']))
ck('wild reveal silhouette and scan', 'silhouette' in ino and 'revealAge' in ino and 'drawCircle' in ino)
ck('wild reveal hides identity', '"???"' in ino and '"분석 중…"' in ino)
ck('wild battle disabled during reveal', 'revealing?"등장 중…":"대전 시작"' in ino and 'wildRevealUntil && (int32_t)(wildRevealUntil-millis())>0' in ino)
ck('wild repeated frame uses partial present', 'canvasPresentBand(82, 326)' in ino)

ck('evolution result transient state', all(x in ino for x in ['evolveResultUntil','evolveResultFromDex','evolveResultToDex','evolveResultJogress']))
ck('evolution result armed on falling edge', '!transforming && wasTransforming' in ino and 'evolveResultUntil = now + 3000UL' in ino)
ck('evolution result card exists', 'drawEvolutionResultCard()' in ino and 'EVOLUTION COMPLETE' in ino and 'JOGRESS COMPLETE' in ino)
ck('evolution result tap dismiss', 'evolveResultUntil = 0;' in ino and 'uiCurrentScreen() == SCR_MAIN' in ino)
ck('evolution result forces safe home present', 'homeCrossBandActive' in ino and 'evolveResultUntil' in ino)

ck('SFX definitions have per-effect mix', re.search(r'struct\s+SfxDef\s*\{[^}]*mix', ac, re.S) is not None)
ck('mixedVolume helper exists', 'static uint8_t mixedVolume' in ac)
ck('music mixed below SFX', 'pump(step, mixedVolume(gVol, 8));' in ac)
ck('UI press is async queue-first', 'xQueueSendToFront(gQ, &id, 0)' in ac and 'v3.108 async' in ah)

# v3.108.1 intentionally removes the second-poll release debounce because it
# added visible latency on the physical CST9217.  The historical verifier keeps
# checking that the touch handler and fast training paths still exist, rather
# than pinning the superseded debounce implementation.
ck('touch gesture handler remains', 'void handleTouch()' in ino and 'else if (wasPressed)' in ino)
ck('training press-down fast paths remain', 'if (gameOpen)' in ino and 'if (sackOpen)' in ino)
ck('animated scheduler includes wild reveal', 'wildOpen && isCreatureId(wildCandidate)' in ino and 'wildRevealUntil' in ino)
ck('animated scheduler includes evolution', 'pet.evolving()' in ino)

ck('root and firmware mirror exact', ino == mir)
ck('workflow runs v3.108 verifier', 'verify_finish_polish_v31080.py' in wf)
m2=re.search(r'const\s+FW_VERSION\s*=\s*"(\d+)\.(\d+)\.(\d+)(?:-[^"]*)?"', inst)
ck('installer marker 3.108+', bool(m2) and tuple(map(int,m2.groups())) >= (3,108,0))

bad=[n for n,v in checks if not v]
for n,v in checks: print(('PASS' if v else 'FAIL')+': '+n)
print(f'\n{len(checks)-len(bad)}/{len(checks)} checks passed')
if bad: sys.exit(1)
