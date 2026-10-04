#!/usr/bin/env python3
from pathlib import Path
import re, sys
ROOT=Path(__file__).resolve().parents[1]
ino=(ROOT/'TamaPoke.ino').read_text(encoding='utf-8')
mir=(ROOT/'firmware_source/TamaPoke.ino').read_text(encoding='utf-8')
extras=(ROOT/'game_extras.cpp').read_text(encoding='utf-8')
inst=(ROOT/'TamaPoke-KO-OneClick-Installer.html').read_text(encoding='utf-8')
wf=(ROOT/'.github/workflows/main.yml').read_text(encoding='utf-8')
checks=[]
def ck(n,v): checks.append((n,bool(v)))

m=re.search(r'#define\s+FW_VERSION\s+"(\d+)\.(\d+)\.(\d+)"',ino)
ck('FW v3.108.1+', bool(m) and tuple(map(int,m.groups())) >= (3,108,1))
ck('root/mirror exact', ino == mir)

# Rival cooldown: 30-minute maximum, validates both clocks, invalid future values unlock.
ck('rival cooldown constant 30', 'RIVAL_COOLDOWN_MIN = 30UL' in extras)
ck('rival age remainder bounded', '_rivalNextMinute - pet.ageMinutes' in extras and 'm <= RIVAL_COOLDOWN_MIN' in extras)
ck('rival epoch remainder bounded', '_rivalNextEpoch - pet.lastSeenEpoch' in extras and '(sec + 59UL) / 60UL' in extras)
ck('rival stale future unlocks', 'best == 0xFFFFFFFFUL ? 0' in extras)
# Equivalent behavioral model for the reported 6625-minute regression.
def left(age, next_age, seen, next_epoch):
    INF=0xFFFFFFFF
    best=INF
    if next_age:
        if age >= next_age: return 0
        m=next_age-age
        if m <= 30: best=m
    if next_epoch and seen:
        if seen >= next_epoch: return 0
        m=(next_epoch-seen+59)//60
        if m <= 30 and m < best: best=m
    return 0 if best==INF else best
ck('reported 6625-min skew falls back to sane age clock', left(100,125,1000,1000+6625*60) == 25)
ck('both stale clocks cannot lock player', left(100,7000,1000,1000+6625*60) == 0)
ck('normal fresh cooldown remains 30', left(100,130,1000,2800) == 30)

# LAN removed from user-facing battle hub and no hub route opens it.
hub=re.search(r'void renderBattleHub\(\) \{(.*?)\n\}',ino,re.S)
tap=re.search(r'void battleHubTap\(int16_t x, int16_t y\) \{(.*?)\n\}',ino,re.S)
hubtxt=hub.group(1) if hub else ''
taptxt=tap.group(1) if tap else ''
ck('LAN label removed from battle hub', 'LAN 배틀' not in hubtxt and '근거리 통신' not in hubtxt)
ck('battle hub has five entries', 'N[5]' in hubtxt and 'i < 5' in hubtxt)
ck('battle hub cannot open LAN', 'lanOpen = true' not in taptxt and 'LINK_OFF' not in taptxt)

# Touch latency hotfix.
ck('touch active poll <=12ms', 'lastPoll < 12' in ino)
ck('latency releaseCandidate removed', 'releaseCandidateAt' not in ino)
ck('18ms second-release wait removed', 'releaseCandidateAt < 18UL' not in ino and 'rn - releaseCandidateAt' not in ino)
ck('tap still resolves on release for gestures', 'else if (wasPressed)' in ino and 'onTap(tX0, tY0)' in ino)
ck('training remains immediate press-down', 'if (gameOpen)' in ino and 'if (pressed && !wasPressed)' in ino)

m2=re.search(r'const\s+FW_VERSION\s*=\s*"([^"]+)"',inst)
ck('installer v3.108.1+ marker', bool(m2) and (lambda g: tuple(map(int,g)) >= (3,108,1))(re.match(r'(\d+)\.(\d+)\.(\d+)',m2.group(1)).groups()) if re.match(r'(\d+)\.(\d+)\.(\d+)',m2.group(1)) else False)
ck('workflow runs hotfix verifier twice', wf.count('verify_hotfix_v31081.py') >= 2)

bad=[n for n,v in checks if not v]
for n,v in checks: print(('PASS' if v else 'FAIL')+': '+n)
print(f'\n{len(checks)-len(bad)}/{len(checks)} checks passed')
if bad: sys.exit(1)
