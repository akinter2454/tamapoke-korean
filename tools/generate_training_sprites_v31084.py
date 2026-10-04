from PIL import Image
from pathlib import Path
import re, colorsys

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'assets/training/source'
RUNTIME=ROOT/'assets/training/runtime24'
HEADER=ROOT/'ui_sprites.h'
W=H=24
RUNTIME.mkdir(parents=True, exist_ok=True)

# Target content boxes inside 24x24. The elongated bag intentionally uses nearly
# the full sprite height while the other targets leave breathing room for UI gauges.
SPECS={
    'attack_sandbag': {'box':(6,0,18,24), 'arrays':['TRAIN_SACK_IDLE_PX','TRAIN_SACK_HIT_L_PX','TRAIN_SACK_HIT_R_PX','TRAIN_SACK_CRIT_PX'], 'pal':'PAL_SACK'},
    'defense_shield': {'box':(2,2,22,22), 'arrays':['TRAIN_SHIELD_IDLE_PX','TRAIN_SHIELD_BLOCK_PX','TRAIN_SHIELD_GOOD_PX','TRAIN_SHIELD_PERFECT_PX'], 'pal':'PAL_SHIELD'},
    'speed_bolt': {'box':(1,1,23,23), 'arrays':['TRAIN_BOLT_A_PX','TRAIN_BOLT_B_PX'], 'pal':'PAL_BOLT'},
    'vitality_heart': {'box':(2,3,22,21), 'arrays':['TRAIN_HEART_IDLE_PX','TRAIN_HEART_PULSE_PX','TRAIN_HEART_PERFECT_PX'], 'pal':'PAL_HEART'},
}

def rgba_fit(path, box):
    im=Image.open(path).convert('RGBA')
    x0,y0,x1,y1=box
    tw,th=x1-x0,y1-y0
    # trim source alpha
    bb=im.getchannel('A').point(lambda a: 255 if a >= 80 else 0).getbbox()
    if bb: im=im.crop(bb)
    scale=min(tw/im.width, th/im.height)
    nw=max(1,round(im.width*scale)); nh=max(1,round(im.height*scale))
    # Nearest samples generated pixel-art clusters without muddy edge blending.
    small=im.resize((nw,nh), Image.Resampling.NEAREST)
    canvas=Image.new('RGBA',(W,H),(0,0,0,0))
    ox=x0+(tw-nw)//2; oy=y0+(th-nh)//2
    canvas.alpha_composite(small,(ox,oy))
    return canvas

def quantize7(im):
    # Quantize only visible pixels; transparent background must not consume palette slots.
    rgba=im.convert('RGBA')
    visible=[]
    for r,g,b,a in rgba.getdata():
        if a>=80:
            visible.append((r,g,b))
    if not visible:
        return [0]*(W*H), [(0,0,0)]*7
    strip=Image.new('RGB',(len(visible),1))
    strip.putdata(visible)
    qstrip=strip.quantize(colors=7, method=Image.Quantize.MEDIANCUT)
    rawpal=qstrip.getpalette()[:21]
    colors=[tuple(rawpal[i:i+3]) for i in range(0,21,3)]
    # Ensure exactly seven entries, then order dark -> light for predictable shades.
    while len(colors)<7: colors.append(colors[-1])
    colors=colors[:7]
    colors=sorted(colors, key=lambda c: 0.2126*c[0]+0.7152*c[1]+0.0722*c[2])
    idx=[]
    for r,g,b,a in rgba.getdata():
        if a<80:
            idx.append(0); continue
        best=min(range(7), key=lambda i: (r-colors[i][0])**2+(g-colors[i][1])**2+(b-colors[i][2])**2)
        idx.append(best+1)
    return idx, colors

def rgb565(c):
    r,g,b=c
    return ((r>>3)<<11)|((g>>2)<<5)|(b>>3)

def pack(idx):
    out=[]
    for i in range(0,W*H,2):
        out.append((idx[i]&0xF)|((idx[i+1]&0xF)<<4))
    return out

def arr_text(vals):
    lines=[]
    for i in range(0,len(vals),24):
        lines.append('  '+', '.join(f'0x{x:02X}' for x in vals[i:i+24])+',')
    return '\n'.join(lines)

def save_index_preview(idx,pal,path,scale=8):
    out=Image.new('RGBA',(W,H),(0,0,0,0))
    pix=out.load()
    for y in range(H):
        for x in range(W):
            k=idx[y*W+x]
            if k:
                r,g,b=pal[k-1]; pix[x,y]=(r,g,b,255)
    out.resize((W*scale,H*scale),Image.Resampling.NEAREST).save(path)
    return out

text=HEADER.read_text(encoding='utf-8')
summary=[]
for name,spec in SPECS.items():
    im=rgba_fit(SRC/f'{name}.png',spec['box'])
    idx,pal=quantize7(im)
    save_index_preview(idx,pal,RUNTIME/f'{name}_24.png',8)
    packed=pack(idx)
    # replace palette
    vals=[0]+[rgb565(c) for c in pal]
    ppat=rf'static const uint16_t {spec["pal"]}\[8\] = \{{[^}}]*\}};'
    prep=f'static const uint16_t {spec["pal"]}[8] = {{ '+', '.join(f'0x{v:04X}' for v in vals)+' };'
    text,n=re.subn(ppat,prep,text)
    if n!=1: raise SystemExit(f'palette replace failed {spec["pal"]}: {n}')
    for arr in spec['arrays']:
        apat=rf'static const uint8_t {arr}\[UI_SPR_BYTES\] = \{{.*?\n\}};'
        arep=f'static const uint8_t {arr}[UI_SPR_BYTES] = {{\n{arr_text(packed)}\n}};'
        text,n=re.subn(apat,arep,text,flags=re.S)
        if n!=1: raise SystemExit(f'array replace failed {arr}: {n}')
    summary.append((name,spec['box'],pal))

HEADER.write_text(text,encoding='utf-8')
print('updated',HEADER)
for x in summary: print(x[0], 'box',x[1], 'palette',x[2])
