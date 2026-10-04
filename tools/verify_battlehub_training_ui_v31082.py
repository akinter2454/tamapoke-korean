#!/usr/bin/env python3
from pathlib import Path
import re, sys
ROOT=Path(__file__).resolve().parents[1]
ino=(ROOT/'TamaPoke.ino').read_text(encoding='utf-8')
mir=(ROOT/'firmware_source/TamaPoke.ino').read_text(encoding='utf-8')
inst=(ROOT/'TamaPoke-KO-OneClick-Installer.html').read_text(encoding='utf-8')
wf=(ROOT/'.github/workflows/main.yml').read_text(encoding='utf-8')
checks=[]
def ck(n,v): checks.append((n,bool(v)))

m=re.search(r'^#define\s+FW_VERSION\s+"(\d+)\.(\d+)\.(\d+)"',ino,re.M)
ck('FW v3.108.2+', bool(m) and tuple(map(int,m.groups())) >= (3,108,2))
ck('root/mirror exact', ino == mir)

hub=re.search(r'void renderBattleHub\(\) \{(.*?)\n\}',ino,re.S)
tap=re.search(r'void battleHubTap\(int16_t x, int16_t y\) \{(.*?)\n\}',ino,re.S)
h=hub.group(1) if hub else ''
t=tap.group(1) if tap else ''
ck('battle hub keeps five entries', 'N[5]' in h and 'i < 5' in h)
ck('battle hub cards enlarged to 44px', 'HUB_H = 44' in h)
ck('battle hub cards widened to 346px', 'HUB_W = 346' in h)
ck('battle hub uses 49px row pitch', 'HUB_STEP = 49' in h)
ck('battle hub starts at safe y90', 'HUB_Y0 = 90' in h)
ck('battle hub touch geometry matches render', all(x in t for x in ['HUB_X = 60','HUB_W = 346','HUB_Y0 = 90','HUB_H = 44','HUB_STEP = 49']))
ck('explore button resized and touch matched', 'uiGameButton(116, 346, 234, 44' in h and 'x >= 116 && x <= 350 && y >= 346 && y <= 390' in t)
ck('LAN remains absent from hub', 'LAN 배틀' not in h and 'lanOpen = true' not in t)

fx=re.search(r'static void drawTrainingFx\(\) \{(.*?)\n\}',ino,re.S)
f=fx.group(1) if fx else ''
ck('training feedback no longer uses success ring/check sprites', 'FX_SUCCESS_A' not in f and 'FX_SUCCESS_B' not in f)
ck('training overlay feedback is disabled or compact', (not f.strip()) or ('FX_IMPACT_A' in f and 'FX_IMPACT_B' in f) or ('Intentionally empty' in f))
ck('training success scoring unchanged', 'startTrainingFx' in ino and 'defFeedback < 4' in ino and 'hpFeedback < 4' in ino)

mi=re.search(r'const\s+FW_VERSION\s*=\s*"([^"]+)"',inst)
ck('installer v3.108.2+ marker', bool(mi) and tuple(map(int, mi.group(1).split('-',1)[0].split('.'))) >= (3,108,2))
ck('workflow runs v3.108.2 verifier twice', wf.count('verify_battlehub_training_ui_v31082.py') >= 2)

bad=[n for n,v in checks if not v]
for n,v in checks: print(('PASS' if v else 'FAIL')+': '+n)
print(f'\n{len(checks)-len(bad)}/{len(checks)} checks passed')
if bad: sys.exit(1)
