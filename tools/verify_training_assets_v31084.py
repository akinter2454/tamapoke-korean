#!/usr/bin/env python3
from pathlib import Path
import re, sys
ROOT=Path(__file__).resolve().parents[1]
ino=(ROOT/'TamaPoke.ino').read_text(encoding='utf-8')
mir=(ROOT/'firmware_source/TamaPoke.ino').read_text(encoding='utf-8')
ui=(ROOT/'ui_sprites.h').read_text(encoding='utf-8')
inst=(ROOT/'TamaPoke-KO-OneClick-Installer.html').read_text(encoding='utf-8')
wf=(ROOT/'.github/workflows/main.yml').read_text(encoding='utf-8')
checks=[]
def ck(n,v): checks.append((n,bool(v)))

m=re.search(r'^#define\s+FW_VERSION\s+"(\d+)\.(\d+)\.(\d+)"',ino,re.M)
ck('FW v3.108.4+', bool(m) and tuple(map(int,m.groups())) >= (3,108,4))
ck('root/mirror exact', ino==mir)

# Training overlay must be fully inert.
start=re.search(r'static void startTrainingFx\([^)]*\) \{(.*?)\n\}',ino,re.S)
draw=re.search(r'static void drawTrainingFx\(\) \{(.*?)\n\}',ino,re.S)
st=start.group(1) if start else ''
dr=draw.group(1) if draw else ''
ck('training start does not arm overlay timer', 'millis() +' not in st and 'trainFxUntil = 0' in st)
ck('training draw has no sprite overlay', 'drawUiSprite4bpp' not in dr and 'FX_IMPACT' not in dr and 'FX_SUCCESS' not in dr)

# Embedded sprite arrays are exactly 24x24x4bpp = 288 bytes.
arrs=['TRAIN_SACK_IDLE_PX','TRAIN_SACK_HIT_L_PX','TRAIN_SACK_HIT_R_PX','TRAIN_SACK_CRIT_PX',
      'TRAIN_SHIELD_IDLE_PX','TRAIN_SHIELD_BLOCK_PX','TRAIN_SHIELD_GOOD_PX','TRAIN_SHIELD_PERFECT_PX',
      'TRAIN_BOLT_A_PX','TRAIN_BOLT_B_PX','TRAIN_HEART_IDLE_PX','TRAIN_HEART_PULSE_PX','TRAIN_HEART_PERFECT_PX']
parsed={}
for name in arrs:
    mm=re.search(rf'static const uint8_t {name}\[UI_SPR_BYTES\] = \{{(.*?)\n\}};',ui,re.S)
    vals=re.findall(r'0x[0-9A-Fa-f]{2}',mm.group(1)) if mm else []
    parsed[name]=[int(v,16) for v in vals]
    ck(f'{name} 288 bytes', len(vals)==288)

# Stable category frames: no visual flash during fast training input.
def same(*names):
    return all(parsed.get(n)==parsed.get(names[0]) for n in names[1:])
ck('sandbag state frames stable', same('TRAIN_SACK_IDLE_PX','TRAIN_SACK_HIT_L_PX','TRAIN_SACK_HIT_R_PX','TRAIN_SACK_CRIT_PX'))
ck('shield state frames stable', same('TRAIN_SHIELD_IDLE_PX','TRAIN_SHIELD_BLOCK_PX','TRAIN_SHIELD_GOOD_PX','TRAIN_SHIELD_PERFECT_PX'))
ck('bolt animation frames stable', same('TRAIN_BOLT_A_PX','TRAIN_BOLT_B_PX'))
ck('heart feedback frames stable', same('TRAIN_HEART_IDLE_PX','TRAIN_HEART_PULSE_PX','TRAIN_HEART_PERFECT_PX'))

# Check nonzero bbox dimensions inside packed 24x24 array.
def bbox(vals):
    px=[]
    for b in vals:
        px.extend([b&0x0F,(b>>4)&0x0F])
    xs=[]; ys=[]
    for i,v in enumerate(px[:576]):
        if v:
            xs.append(i%24); ys.append(i//24)
    return (min(xs),min(ys),max(xs),max(ys)) if xs else None
b=bbox(parsed['TRAIN_SACK_IDLE_PX'])
ck('sandbag is elongated', bool(b) and (b[3]-b[1]+1)>=22 and (b[2]-b[0]+1)<=12)
for n in ['TRAIN_SHIELD_IDLE_PX','TRAIN_BOLT_A_PX','TRAIN_HEART_IDLE_PX']:
    b2=bbox(parsed[n]); ck(f'{n} readable bbox', bool(b2) and (b2[2]-b2[0]+1)>=16 and (b2[3]-b2[1]+1)>=16)

# Runtime geometry.
ck('sack supplied frame in bounded 144px area', 'drawTrainingArt(sackArt, sx - 72, 48, 3);' in ino)
ck('defense supplied shield stays 96px', '? ART_SHIELD_SUCCESS : ART_SHIELD_IDLE, CX - 48, 106, 2);' in ino)
ck('speed target keeps adaptive scale', 'int boltScale = r >= 34 ? 2 : 1;' in ino)
ck('heart supplied art stays 96px', 'drawTrainingArt(ART_HEART, CX - 48, CY - 48, 2);' in ino)
ck('training menu uses same four icons', 'const UiSprite4bpp *trainIcon[4]' in ino and 'drawUiSprite4bpp(trainIcon[i], TRAIN_X + 24, y + 4, 2);' in ino)
ck('training menu text/bar shifted for icons', 'uiSetCursor(TRAIN_X + 78, y + 9);' in ino and 'int bx = TRAIN_X + 78, bw = TRAIN_W - 112' in ino)

for f in ['attack_sandbag.png','defense_shield.png','speed_bolt.png','vitality_heart.png']:
    ck('source asset '+f, (ROOT/'assets/training/source'/f).is_file())
    ck('runtime asset '+f.replace('.png','_24.png'), (ROOT/'assets/training/runtime24'/f.replace('.png','_24.png')).is_file())
ck('training sprite generator bundled', (ROOT/'tools/generate_training_sprites_v31084.py').is_file())
mi=re.search(r'const\s+FW_VERSION\s*=\s*"([^"]+)"',inst)
fwver='.'.join(m.groups()) if m else ''
ck('installer version matches firmware', bool(mi) and bool(fwver) and mi.group(1).startswith(fwver+'-'))
ck('workflow runs training verifier twice', wf.count('verify_training_assets_v31084.py')>=2)

bad=[n for n,v in checks if not v]
for n,v in checks: print(('PASS' if v else 'FAIL')+': '+n)
print(f'\n{len(checks)-len(bad)}/{len(checks)} checks passed')
if bad: sys.exit(1)
