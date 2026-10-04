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
 'firmware 3.103.0+': version_at_least(3,103,0),
 'embedded sprite pack': (('#define UI_SPR_BYTES 64' in ui) or ('#define UI_SPR_BYTES 288' in ui)) and 'TRAIN_SACK_IDLE' in ui and 'EGG_SHELL' in ui,
 'run-length sprite renderer':('static void drawUiSprite2bpp' in src or 'static void drawUiSprite4bpp' in src) and 'canvasFillRectFast' in src,
 'attack training sprite':'TRAIN_SACK_IDLE' in src and 'TRAIN_SACK_CRIT' in ui,
 'defence training sprite':'TRAIN_SHIELD_IDLE' in src and 'TRAIN_SHIELD_PERFECT' in src,
 'speed training sprite':('TRAIN_BOLT' in src or 'TRAIN_BOLT_A' in src) and ('drawUiSprite2bpp' in src or 'drawUiSprite4bpp' in src),
 'vitality training sprite':'TRAIN_HEART_PERFECT' in src and 'TRAIN_HEART_PULSE' in src,
 'wild pokemon real PMD preview':'galleryPmd.load(wildCandidate, false)' in src and 'drawPmdActM(galleryPmd, PMD_IDLE' in src,
 'wild preview frees PSRAM':'galleryPmd.unload();' in src and 'startWildBattle' in src,
 'eight event sprite routing':all(k in src for k in ['EVENT_CHEST','EVENT_GIFT','EVENT_STAR','EVENT_BERRY','EVENT_TOOL','EVENT_MACHINE','EVENT_MAP','EVENT_KIT']),
 'treasure closed/open sprites':('CHEST_CLOSED' in src or 'CHEST_GROWTH' in src) and 'CHEST_OPEN' in src,
 'six compact item icons':all(k in src for k in ['ITEM_TRAIN','ITEM_CARE','ITEM_IV','ITEM_CROWN','ITEM_CHARM','ITEM_SHINY_BERRY']),
 'egg crack sprites':'EGG_BASE' in src and 'EGG_CRACK1' in src and 'EGG_CRACK2' in src,
 'hatch flash and shell':'uiHatchFxUntil' in src and 'EGG_GLOW' in src and 'EGG_SHELL' in src,
 'save schema unchanged':'#define SAVE_VERSION 2' in (ROOT/'save.h').read_text(encoding='utf-8'),
 'source mirror exact':src==mir,
 'preview exists':(ROOT/'TamaPoke-v3.103.0-SpriteUpgrade-Preview.png').exists() or (ROOT/'TamaPoke-v3.104.0-SpriteUpgrade-Preview.png').exists(),
}
bad=[]
for name,ok in checks.items():
    print(('PASS' if ok else 'FAIL')+': '+name)
    if not ok: bad.append(name)
if bad:
    print(f'FAILED {len(bad)} checks',file=sys.stderr);sys.exit(1)
print(f'OK: {len(checks)} sprite upgrade checks')
