from pathlib import Path
import re, sys
ROOT=Path(__file__).resolve().parents[1]
src=(ROOT/'TamaPoke.ino').read_text(encoding='utf-8')
def version_at_least(a,b,c):
    m=re.search(r'#define\s+FW_VERSION\s+"(\d+)\.(\d+)\.(\d+)"',src)
    return bool(m) and tuple(map(int,m.groups())) >= (a,b,c)
mirror=(ROOT/'firmware_source'/'TamaPoke.ino').read_text(encoding='utf-8')
checks={
 'firmware keeps v3.102.0+ battle UI':version_at_least(3,102,0),
 'dark battle HUD palette':'#define BTL_HUD_DARK' in src and '#define BTL_HUD_MID' in src,
 'context/weather top tag':'static void btlDrawTopTag()' in src and 'btlContextKo()' in src,
 'battle context includes wild':'if (btlWild) return "야생";' in src,
 'HP bar segmented high contrast':'drawFastVLine(dx, y + 4, 8, BTL_HUD_DARK)' in src,
 'HUD uses type accent':'typeColor(creatureType1(c.dex))' in src,
 'lower command dock dark':'gfx->fillRect(0, 254, 466, 212, BTL_HUD_DARK);' in src,
 'fight command accent':'BTL_CMD_FIGHT' in src and 'gfx->drawLine(BTL_GRID_X + 24' in src,
 'switch/run commands distinct':'BTL_CMD_SWITCH' in src and 'BTL_CMD_RUN' in src,
 'move cells type accented':'typeColor(MOVE_TBL[mv].type)' in src and 'gfx->fillRoundRect(x + 3, y + 3, 5' in src,
 'narration dark panel':'BTL_HUD_MID' in src and '"터치 >"' in src,
 'touch geometry unchanged':'#define BTL_CELL_W 160' in src and '#define BTL_GRID_X 69' in src and '#define BTL_GRID_Y 274' in src,
 'source mirror exact':src==mirror,
 'interactive preview exists':(ROOT/'TamaPoke-BattleUI-v3.102.0-Preview.html').exists(),
}
bad=[]
for name,ok in checks.items():
    print(('PASS' if ok else 'FAIL')+': '+name)
    if not ok: bad.append(name)
if bad:
    print(f'FAILED {len(bad)} checks', file=sys.stderr); sys.exit(1)
print(f'OK: {len(checks)} battle UI checks')
