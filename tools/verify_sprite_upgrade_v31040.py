from pathlib import Path
import re, sys
ROOT=Path(__file__).resolve().parents[1]
src=(ROOT/'TamaPoke.ino').read_text(encoding='utf-8')
def version_at_least(a,b,c):
    m=re.search(r'#define\s+FW_VERSION\s+"(\d+)\.(\d+)\.(\d+)"',src)
    return bool(m) and tuple(map(int,m.groups())) >= (a,b,c)
mir=(ROOT/'firmware_source'/'TamaPoke.ino').read_text(encoding='utf-8')
ui=(ROOT/'ui_sprites.h').read_text(encoding='utf-8')
checks={
 'firmware 3.104.0+':version_at_least(3,104,0),
 '24x24 sprite geometry':'#define UI_SPR_W 24' in ui and '#define UI_SPR_H 24' in ui,
 '4bpp frame size':'#define UI_SPR_BYTES 288' in ui,
 'indexed sprite struct':'struct UiSprite4bpp' in ui,
 '8-shade palettes':ui.count('static const uint16_t PAL_') >= 15,
 '4bpp run renderer':'static void drawUiSprite4bpp' in src and 'spr->pal[idx & 7]' in src,
 'attack training detail':'TRAIN_SACK_IDLE' in src and all(k in ui for k in ['TRAIN_SACK_IDLE','TRAIN_SACK_HIT_L','TRAIN_SACK_HIT_R','TRAIN_SACK_CRIT']),
 'defense training detail':(all(k in src for k in ['TRAIN_SHIELD_IDLE','TRAIN_SHIELD_BLOCK','TRAIN_SHIELD_GOOD','TRAIN_SHIELD_PERFECT']) or ('drawTrainingArt(feedbackActive && defFeedback >= 1 && defFeedback <= 3' in src and 'ART_SHIELD_SUCCESS' in src and 'ART_SHIELD_IDLE' in src)),
 'speed two-frame animation':'TRAIN_BOLT_A' in src and 'TRAIN_BOLT_B' in src and 'now / 110' in src,
 'vitality detailed heart':(all(k in src for k in ['TRAIN_HEART_IDLE','TRAIN_HEART_PULSE','TRAIN_HEART_PERFECT']) or 'drawTrainingArt(ART_HEART' in src),
 'event eight props':all(k in src for k in ['EVENT_CHEST','EVENT_GIFT','EVENT_STAR','EVENT_BERRY','EVENT_TOOL','EVENT_MACHINE','EVENT_MAP','EVENT_KIT']),
 'treasure burst animation':'CHEST_BURST' in src and ('millis()/180' in src or 'millis()/150' in src),
 'three themed treasure chests':all(k in src for k in ['CHEST_GROWTH','CHEST_SHINY','CHEST_TECH']),
 'six item icons':all(k in src for k in ['ITEM_TRAIN','ITEM_CARE','ITEM_IV','ITEM_CROWN','ITEM_CHARM','ITEM_SHINY_BERRY']),
 'egg frames':all(k in src for k in ['EGG_BASE','EGG_CRACK1','EGG_CRACK2','EGG_GLOW','EGG_SHELL']),
 'wild PMD preserved':'galleryPmd.load(wildCandidate, false)' in src,
 'save schema unchanged':'#define SAVE_VERSION 2' in (ROOT/'save.h').read_text(encoding='utf-8'),
 'source mirror exact':src==mir,
 'generator present':(ROOT/'tools'/'generate_ui_sprites_v31040.py').exists() or (ROOT/'tools'/'generate_ui_sprites_v31050.py').exists(),
 'preview present':(ROOT/'TamaPoke-v3.104.0-SpriteUpgrade-Preview.png').exists() or (ROOT/'TamaPoke-v3.105.0-FXSprite-Preview.png').exists(),
}
# Verify every packed pixel array is exactly 288 bytes.
arrs=re.findall(r'static const uint8_t ([A-Z0-9_]+)_PX\[UI_SPR_BYTES\] = \{(.*?)\};',ui,re.S)
array_ok=len(arrs)>=38
for name,body in arrs:
    vals=re.findall(r'0x[0-9A-Fa-f]{2}',body)
    if len(vals)!=288:
        print(f'array {name}: {len(vals)} bytes',file=sys.stderr);array_ok=False
checks['all sprite arrays exactly 288 bytes']=array_ok
bad=[]
for name,ok in checks.items():
    print(('PASS' if ok else 'FAIL')+': '+name)
    if not ok: bad.append(name)
if bad:
    print(f'FAILED {len(bad)} checks',file=sys.stderr);sys.exit(1)
print(f'OK: {len(checks)} enhanced sprite checks; arrays={len(arrs)}')
