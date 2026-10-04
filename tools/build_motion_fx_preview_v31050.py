from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import importlib.util
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('sprgen',ROOT/'tools'/'generate_ui_sprites_v31050.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
lookup={s.name:s for s in m.sprites}
try:
    fb=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',24)
    f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
except: fb=f=None
BG=(12,17,27); PANEL=(28,38,54); WHITE=(244,247,252); MUTED=(156,174,201)

def paste_sprite(im,name,cx,cy,scale=4):
    s=lookup[name]
    z=Image.new('RGBA',(m.W,m.H),(0,0,0,0)); px=z.load(); idx=s.im.load()
    for y in range(m.H):
        for x in range(m.W):
            v=idx[x,y]
            if v: px[x,y]=(*s.pal[v],255)
    z=z.resize((m.W*scale,m.H*scale),Image.Resampling.NEAREST)
    im.alpha_composite(z,(cx-z.width//2,cy-z.height//2))

W=1000; H=1040
out=Image.new('RGBA',(W,H),BG+(255,)); d=ImageDraw.Draw(out)
d.text((36,28),'TamaPoke v3.105.0 · Motion FX Preview',fill=WHITE,font=fb)
labels=[('TRAINING HIT','TRAIN_SACK_IDLE','FX_IMPACT_A'),('ITEM USE','ITEM_CROWN','FX_ITEM_RING_A'),('TREASURE REVEAL','CHEST_BURST','FX_SHINY_A'),('SHINY ENTRANCE','TRAIN_SHIELD_IDLE','FX_SHINY_B')]
for i,(title,obj,fx) in enumerate(labels):
    col=i%2; row=i//2; x=32+col*484; y=90+row*460
    d.rounded_rectangle((x,y,x+450,y+420),20,fill=PANEL,outline=(75,101,143),width=2)
    d.text((x+22,y+18),title,fill=WHITE,font=fb)
    d.text((x+22,y+54),'embedded 24x24 pixel FX',fill=MUTED,font=f)
    cx=x+225; cy=y+220
    # glow backdrop
    d.ellipse((cx-105,cy-105,cx+105,cy+105),fill=(37,50,72),outline=(91,118,159),width=2)
    if title=='ITEM USE':
        paste_sprite(out,fx,cx,cy,5); paste_sprite(out,obj,cx,cy,3)
    elif title=='TREASURE REVEAL':
        paste_sprite(out,fx,cx-38,cy-48,3); paste_sprite(out,fx,cx+55,cy-15,2); paste_sprite(out,obj,cx,cy+25,4)
        for dx,dy in [(-110,0),(110,0),(0,-110),(0,110)]: d.line((cx,cy,cx+dx,cy+dy),fill=(255,210,80),width=4)
    elif title=='SHINY ENTRANCE':
        paste_sprite(out,obj,cx,cy+30,4); paste_sprite(out,fx,cx-50,cy-55,3); paste_sprite(out,'FX_SHINY_A',cx+60,cy-10,2)
    else:
        paste_sprite(out,obj,cx,cy+20,4); paste_sprite(out,fx,cx+55,cy-35,3)
    captions={
      'TRAINING HIT':'Short impact / GOOD / PERFECT feedback',
      'ITEM USE':'Icon pulse + ring + rare-item sparkle',
      'TREASURE REVEAL':'Opening rays + sparkle burst',
      'SHINY ENTRANCE':'Hatch / battle entrance sparkle',
    }
    d.text((x+22,y+374),captions[title],fill=WHITE,font=f)
path=ROOT/'TamaPoke-v3.105.0-MotionFX-Preview.png'
out.convert('RGB').save(path)
print(path)
