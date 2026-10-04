from pathlib import Path
import re, sys
ROOT=Path(__file__).resolve().parents[1]
src=(ROOT/'TamaPoke.ino').read_text(encoding='utf-8')
def version_at_least(a,b,c):
    m=re.search(r'#define\s+FW_VERSION\s+"(\d+)\.(\d+)\.(\d+)"',src)
    return bool(m) and tuple(map(int,m.groups())) >= (a,b,c)
mir=(ROOT/'firmware_source'/'TamaPoke.ino').read_text(encoding='utf-8')
ui=(ROOT/'ui_sprites.h').read_text(encoding='utf-8')
wf=(ROOT/'.github/workflows/main.yml').read_text(encoding='utf-8')
checks={
 'firmware v3.105.0+':version_at_least(3,105,0),
 'fx sprites packed':all(k in ui for k in ['FX_IMPACT_A','FX_IMPACT_B','FX_SUCCESS_A','FX_SUCCESS_B','FX_SHINY_A','FX_SHINY_B','FX_ITEM_RING_A','FX_ITEM_RING_B']),
 'training fx state':all(k in src for k in ['trainFxUntil','startTrainingFx','drawTrainingFx']),
 'defense fx hookup':'startTrainingFx(nx, DEF_GAUGE_Y + DEF_GAUGE_H / 2, defFeedback)' in src,
 'sack fx hookup':'startTrainingFx(CX + ((sackHits & 1U) ? 28 : -28), 164' in src,
 'speed fx hookup':'startTrainingFx(spdX, spdY, spdGold ? 3 : 2)' in src,
 'vitality fx hookup':'startTrainingFx(CX, CY, hpFeedback)' in src,
 'training fx renders':src.count('drawTrainingFx();') >= 4,
 'item use fx state':all(k in src for k in ['itemFxUntil','startItemFx','drawItemUseFx']),
 'compact edible item fx removed':('startItemFx(id,(uint8_t)i)' not in src and 'itemFxUntil = 0; itemFxId = XITEM_COUNT;' in src),
 'shiny charm item fx retained':('if(id==XITEM_SHINY)' in src and 'startItemFx(id,0)' in src),
 'item fx home':'drawItemUseFx(CX, PET_CY - 10)' in src,
 'item fx bag':src.count('drawItemUseFx(CX,') >= 3,
 'treasure reveal fx':all(k in src for k in ['treasureFxUntil','startTreasureFx(i)','drawTreasureRevealFx(CX,166)']),
 'shiny hatch fx':'if (pet.shiny) drawShinyFxAt(CX, PET_CY - 12, uiHatchFxUntil);' in src,
 'shiny battle fx':all(k in src for k in ['btlShinyFxUntil','btlShinyFxKey','drawShinyFxAt(348, 106','drawShinyFxAt(124, 224']),
 'battle session reset':src.count('btlResetVisualFx();') >= 6,
 'save schema unchanged':'#define SAVE_VERSION 2' in (ROOT/'save.h').read_text(encoding='utf-8'),
 'source mirror exact':src==mir,
 'generator present':(ROOT/'tools'/'generate_ui_sprites_v31050.py').exists(),
 'preview present':(ROOT/'TamaPoke-v3.105.0-FXSprite-Preview.png').exists(),
 'workflow runs verifier':'verify_motion_fx_v31050.py' in wf,
}
# 46 sprites expected after adding eight FX frames to the 38 v3.104 frames.
arrs=re.findall(r'static const uint8_t ([A-Z0-9_]+)_PX\[UI_SPR_BYTES\] = \{(.*?)\};',ui,re.S)
array_ok=len(arrs)>=46
for name,body in arrs:
    if len(re.findall(r'0x[0-9A-Fa-f]{2}',body))!=288:
        array_ok=False; print('bad array',name,file=sys.stderr)
checks['all packed arrays 288 bytes']=array_ok
bad=[]
for name,ok in checks.items():
    print(('PASS' if ok else 'FAIL')+': '+name)
    if not ok: bad.append(name)
if bad:
    print('FAILED',bad,file=sys.stderr);sys.exit(1)
print(f'OK: {len(checks)} motion-FX checks; arrays={len(arrs)}')
