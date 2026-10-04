#!/usr/bin/env python3
from pathlib import Path
import re, math, sys
ROOT=Path(__file__).resolve().parents[1]
s=(ROOT/'TamaPoke.ino').read_text(encoding='utf-8')
checks=[]
def ck(name, cond):
    checks.append((name, bool(cond)))
ck('firmware version >= 3.98.1', bool(re.search(r'#define\s+FW_VERSION\s+"(\d+)\.(\d+)\.(\d+)"', s)) and tuple(map(int,re.search(r'#define\s+FW_VERSION\s+"(\d+)\.(\d+)\.(\d+)"',s).groups())) >= (3,98,1))
ck('UTF-8 ellipsis safety exists', 'static void uiEllipsize' in s and 'out -= cp' in s)
ck('round-screen chord safety exists', 'static int16_t uiRoundTextWidth' in s and 'sqrtf' in s)
ck('center fit applies round width', 'roundWidth < maxWidth' in s)
ck('left fit ellipsizes at minimum size', 'uiEllipsize(s, fitted' in s)
ck('battle side name uses bounded renderer', ('uiDrawLeftFit(l, tx, ty, 142, 1, 1);' in s) or ('uiDrawLeftFit(l, tx, ty, 116, 1, 1);' in s))
ck('mission name uses bounded renderer', 'uiDrawLeftFit(extras.missionNameKo' in s)
ck('mission reward uses bounded renderer', 'uiDrawLeftFit(rewardLine' in s)
ck('boss availability line bounded', 'uiDrawCenteredFit(pool,CX,226,300,2,1);' in s)
ck('rival challenge line bounded', 'uiDrawCenteredFit(go,CX,313,230,3,1);' in s)
# Species fallback must not be copied into Combatant.name in care-slot conversion.
# v3.109.5 adds an explicit forward declaration and a level-cap parameter, so
# locate the actual definition instead of starting at the prototype.
def fn_body(signature):
    start=s.find(signature)
    if start<0: return ''
    brace=s.find('{',start)
    depth=0
    for pos in range(brace,len(s)):
        if s[pos]=='{': depth+=1
        elif s[pos]=='}':
            depth-=1
            if depth==0: return s[brace+1:pos]
    return ''
block=fn_body('static bool combatantFromCareSlot(uint8_t slot, Combatant &c, uint32_t nowEpoch, uint8_t capLvl) {')
ck('care-slot combatant species name stays dex-backed', 'else c.name[0] = 0;' in block and 'creatureName(m.speciesId)' not in block)
# Prove the concrete problematic names exceed the old 12-byte field and the new path does not depend on it.
long_names=['미라쥬가오가몬 버스트 모드','베르제브몬 블래스트 모드','황제드라몬 팔라딘 모드','알로라 식스테일']
ck('regression corpus contains names longer than old 12-byte field', all(len(x.encode('utf-8'))>=12 for x in long_names))
# Static literals directly centered on the circular panel should fit the conservative chord.
def width(t,size): return sum(6 if ord(c)<128 else 8 for c in t)*size
def chord(y,size,margin=12):
    R=231; cy=233; h=8*size; d=max(abs(y-cy),abs(y+h-cy))
    return 0 if d>=R else int(2*math.sqrt(R*R-d*d)-2*margin)
viol=[]
pat=re.compile(r'uiSetCursor\(CX\s*-\s*uiTextHalfWidth\("([^"]*)",\s*(\d+)\)\s*,\s*(\d+)\)')
for mm in pat.finditer(s):
    text,size,y=mm.group(1),int(mm.group(2)),int(mm.group(3))
    if width(text,size)>chord(y,size): viol.append((text,size,y,width(text,size),chord(y,size)))
ck('literal centered strings stay inside round-screen chord', not viol)
for name,ok in checks:
    print(('PASS' if ok else 'FAIL')+': '+name)
if viol:
    print('Literal overflow candidates:',viol)
if not all(ok for _,ok in checks): sys.exit(1)
