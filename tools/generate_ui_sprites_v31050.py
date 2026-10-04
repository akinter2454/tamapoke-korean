from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
W=H=24
BYTES=W*H//2


def rgb565(rgb):
    r,g,b=rgb
    return ((r>>3)<<11)|((g>>2)<<5)|(b>>3)

class Spr:
    def __init__(self,name,pal):
        self.name=name
        self.pal=pal
        self.im=Image.new('L',(W,H),0)
        self.d=ImageDraw.Draw(self.im)
    def rect(self,xy,c,outline=None,width=1): self.d.rectangle(xy,fill=c,outline=outline,width=width)
    def ellipse(self,xy,c,outline=None,width=1): self.d.ellipse(xy,fill=c,outline=outline,width=width)
    def poly(self,pts,c,outline=None,width=1): self.d.polygon(pts,fill=c); outline is not None and self.d.line(pts+[pts[0]],fill=outline,width=width,joint='curve')
    def line(self,pts,c,width=1): self.d.line(pts,fill=c,width=width,joint='curve')
    def px(self,x,y,c):
        if 0<=x<W and 0<=y<H:self.im.putpixel((x,y),c)
    def clone(self,name):
        s=Spr(name,self.pal); s.im=self.im.copy(); s.d=ImageDraw.Draw(s.im); return s

# 8-color palettes: 0 transparent, then object-specific shades.
P={
 'sack':[(0,0,0),(31,34,42),(91,35,38),(169,52,50),(215,86,63),(246,169,100),(198,202,211),(255,241,208)],
 'shield':[(0,0,0),(25,31,42),(33,64,110),(54,103,181),(88,151,228),(161,205,255),(244,195,74),(248,248,245)],
 'bolt':[(0,0,0),(35,31,26),(132,79,18),(235,155,33),(255,210,67),(255,243,156),(254,250,224),(255,255,255)],
 'heart':[(0,0,0),(47,27,37),(122,30,61),(207,56,86),(239,91,118),(255,163,177),(255,219,224),(255,255,255)],
 'chest':[(0,0,0),(44,29,21),(94,53,27),(160,89,37),(211,133,54),(247,193,73),(121,130,145),(255,235,167)],
 'chest_growth':[(0,0,0),(37,38,24),(82,80,31),(142,125,47),(201,171,72),(242,217,120),(122,132,90),(255,247,194)],
 'chest_shiny':[(0,0,0),(49,27,45),(107,42,92),(176,66,139),(225,102,178),(253,170,215),(118,92,153),(255,232,250)],
 'chest_tech':[(0,0,0),(25,36,50),(39,72,107),(55,112,166),(81,161,215),(153,210,244),(102,116,139),(231,247,255)],
 'gift':[(0,0,0),(42,31,44),(121,31,68),(211,52,95),(244,99,132),(255,191,205),(250,205,68),(255,245,230)],
 'star':[(0,0,0),(44,36,26),(132,87,16),(236,166,25),(255,214,61),(255,242,144),(245,247,250),(255,255,255)],
 'berry':[(0,0,0),(32,45,34),(47,101,53),(80,159,66),(116,192,83),(189,226,139),(108,70,45),(255,242,215)],
 'tool':[(0,0,0),(29,33,41),(60,69,83),(97,111,130),(147,160,177),(210,218,228),(218,119,66),(255,244,225)],
 'machine':[(0,0,0),(28,32,43),(42,66,91),(56,106,145),(73,163,201),(113,220,235),(201,119,231),(246,247,250)],
 'map':[(0,0,0),(52,40,29),(115,79,44),(189,139,78),(225,188,119),(248,224,169),(176,54,48),(255,247,220)],
 'kit':[(0,0,0),(27,39,43),(44,92,96),(65,148,153),(101,196,197),(188,234,229),(239,75,75),(252,252,248)],
 'trainitem':[(0,0,0),(43,31,28),(110,48,34),(208,80,52),(245,128,78),(255,199,131),(255,230,176),(255,255,244)],
 'careitem':[(0,0,0),(27,43,32),(53,107,65),(79,169,92),(126,211,134),(203,241,205),(245,224,232),(255,255,250)],
 'ivitem':[(0,0,0),(36,29,52),(75,48,121),(124,77,186),(165,109,222),(211,166,244),(244,207,70),(255,250,241)],
 'crown':[(0,0,0),(55,41,17),(123,81,13),(210,139,18),(247,187,31),(255,226,92),(225,64,73),(255,248,218)],
 'charm':[(0,0,0),(24,38,49),(34,85,110),(52,145,184),(91,198,224),(176,232,246),(244,189,70),(255,255,250)],
 'shiny':[(0,0,0),(51,29,46),(126,39,94),(214,66,143),(242,105,174),(255,181,218),(177,223,255),(255,255,255)],
 'egg':[(0,0,0),(50,44,34),(132,112,75),(222,201,148),(245,231,191),(255,248,222),(232,166,67),(255,255,255)],
 'fx_impact':[(0,0,0),(53,31,22),(123,51,32),(214,85,45),(250,151,64),(255,213,94),(255,245,209),(255,255,255)],
 'fx_success':[(0,0,0),(24,52,39),(39,105,70),(59,164,102),(101,212,135),(179,240,193),(238,252,243),(255,255,255)],
 'fx_shiny':[(0,0,0),(42,30,59),(88,57,134),(155,87,205),(227,105,220),(255,185,236),(189,225,255),(255,255,255)],
 'fx_item':[(0,0,0),(37,42,58),(68,88,133),(90,145,204),(119,204,232),(190,236,246),(247,214,102),(255,255,255)],
}


sprites=[]
def add(s): sprites.append(s); return s

# --- training: larger, more detailed, each with readable silhouette ---
def sack(name='TRAIN_SACK_IDLE'):
    s=Spr(name,P['sack'])
    # ceiling strap + hook
    s.rect((10,0,13,2),1); s.rect((11,2,12,4),6); s.rect((9,4,14,5),1)
    # bag outline/body
    s.poly([(6,6),(17,6),(19,9),(19,18),(16,22),(7,22),(4,18),(4,9)],2,1,1)
    s.rect((6,8,17,18),3)
    s.rect((7,9,16,10),4); s.rect((7,11,8,17),5)
    # stitched target panel
    s.rect((9,12,15,16),2,6,1); s.line([(12,12),(12,16)],6,1); s.line([(9,14),(15,14)],6,1)
    s.rect((7,20,16,21),2); s.rect((9,22,14,23),1)
    return s
base=add(sack())
sl=base.clone('TRAIN_SACK_HIT_L'); sl.d=ImageDraw.Draw(sl.im); sl.line([(1,10),(4,10)],7,2); sl.line([(2,7),(4,9)],5,1); sl.line([(2,13),(4,11)],5,1); add(sl)
sr=base.clone('TRAIN_SACK_HIT_R'); sr.line([(19,10),(22,10)],7,2); sr.line([(19,9),(21,7)],5,1); sr.line([(19,11),(21,13)],5,1); add(sr)
sc=base.clone('TRAIN_SACK_CRIT'); sc.poly([(20,5),(21,8),(23,9),(21,10),(20,13),(19,10),(17,9),(19,8)],7,5,1); sc.px(3,5,7); sc.px(2,4,5); sc.px(3,3,7); add(sc)

# Shield with rim + crest + spark frames
def shield(name='TRAIN_SHIELD_IDLE'):
    s=Spr(name,P['shield'])
    s.poly([(12,1),(21,4),(20,13),(17,19),(12,23),(7,19),(4,13),(3,4)],2,1,1)
    s.poly([(12,3),(19,5),(18,13),(16,17),(12,20),(8,17),(6,13),(5,5)],3,4,1)
    s.poly([(12,5),(17,7),(16,13),(12,17),(8,13),(7,7)],4)
    # center crest
    s.rect((11,7,13,15),6); s.rect((8,10,16,12),6); s.px(12,8,7); s.px(12,11,7)
    s.line([(6,15),(12,20),(18,15)],5,1)
    return s
sh=add(shield())
sb=sh.clone('TRAIN_SHIELD_BLOCK'); sb.line([(2,5),(0,4)],5,1); sb.line([(22,5),(23,3)],5,1); sb.line([(2,17),(0,19)],4,1); sb.line([(22,17),(23,19)],4,1); add(sb)
sg=sh.clone('TRAIN_SHIELD_GOOD'); sg.poly([(21,2),(22,4),(24-1,5),(22,6),(21,8),(20,6),(18,5),(20,4)],6,7,1); add(sg)
sp=sh.clone('TRAIN_SHIELD_PERFECT');
for x,y in [(2,3),(21,2),(1,15),(22,17),(12,0)]:
    sp.px(x,y,7); sp.px(max(0,x-1),y,5); sp.px(min(23,x+1),y,5)
add(sp)

# Speed lightning two-frame pulse
def bolt(name,flip=False):
    s=Spr(name,P['bolt'])
    pts=[(13,0),(5,12),(10,12),(7,23),(20,8),(14,8),(18,0)] if not flip else [(11,0),(4,11),(9,11),(5,23),(19,9),(13,9),(17,0)]
    s.poly(pts,4,1,1); s.poly([(13,2),(8,11),(12,11),(9,19),(17,9),(13,9),(16,2)],5)
    for x,y in ([(2,4),(21,5),(3,18),(21,17)] if not flip else [(1,7),(22,3),(2,16),(20,20)]):
        s.px(x,y,7); s.px(x+1 if x<23 else x-1,y,3)
    return s
add(bolt('TRAIN_BOLT_A')); add(bolt('TRAIN_BOLT_B',True))

# Heart with ECG detail
def heart(name='TRAIN_HEART_IDLE'):
    s=Spr(name,P['heart'])
    s.poly([(12,22),(3,13),(2,8),(4,4),(8,3),(12,6),(16,3),(20,4),(22,8),(21,13)],3,1,1)
    s.poly([(12,20),(5,13),(4,8),(6,5),(9,5),(12,8),(15,5),(18,5),(20,8),(19,12)],4)
    s.line([(5,11),(9,11),(10,8),(12,15),(14,10),(15,11),(19,11)],6,1)
    s.px(7,6,5); s.px(8,6,5)
    return s
he=add(heart())
hp=he.clone('TRAIN_HEART_PULSE'); hp.line([(1,12),(4,12)],7,1); hp.line([(20,12),(23,12)],7,1); hp.px(12,1,7); add(hp)
hf=he.clone('TRAIN_HEART_PERFECT');
for x,y in [(2,3),(21,4),(1,18),(22,18),(12,0)]: hf.px(x,y,7)
add(hf)

# --- chest family ---
def chest(name,open_=False,burst=False):
    s=Spr(name,P['chest'])
    if open_:
        s.poly([(4,8),(6,3),(18,3),(20,8)],3,1,1); s.rect((6,4,18,6),4); s.rect((10,5,14,6),5)
        s.rect((3,10,20,21),3,1,1); s.rect((5,12,18,19),4); s.rect((10,11,13,16),5); s.rect((11,13,12,15),1)
        s.rect((5,19,18,21),2)
        # coins/gem
        s.ellipse((6,7,9,10),5,1); s.ellipse((15,7,18,10),5,1); s.poly([(12,7),(14,9),(12,11),(10,9)],7,1,1)
    else:
        s.rect((3,6,20,20),3,1,1); s.rect((5,8,18,12),4); s.rect((4,13,19,15),2); s.rect((5,16,18,19),4)
        s.rect((10,11,13,17),5,1,1); s.rect((11,13,12,15),1)
        s.rect((5,7,18,8),5); s.px(6,9,7); s.px(17,9,7)
    if burst:
        for x,y in [(1,3),(22,2),(0,14),(23,15),(6,0),(18,0)]: s.px(x,y,7)
    return s
add(chest('CHEST_CLOSED')); add(chest('CHEST_OPEN',True)); add(chest('CHEST_BURST',True,True))
cg=chest('CHEST_GROWTH'); cg.pal=P['chest_growth']; add(cg)
cs=chest('CHEST_SHINY'); cs.pal=P['chest_shiny']; add(cs)
ct=chest('CHEST_TECH'); ct.pal=P['chest_tech']; add(ct)

# --- event props ---
def gift():
    s=Spr('EVENT_GIFT',P['gift']); s.rect((3,9,20,22),3,1,1); s.rect((5,11,18,20),4); s.rect((10,9,13,22),6); s.rect((3,8,20,11),2,1,1); s.rect((10,8,13,11),6)
    s.poly([(11,8),(6,7),(5,4),(7,2),(10,4),(12,7)],3,1,1); s.poly([(12,8),(18,7),(19,4),(17,2),(14,4),(12,7)],3,1,1); s.px(6,12,5); s.px(17,12,5); return s
add(gift())

def star():
    s=Spr('EVENT_STAR',P['star']); s.poly([(12,1),(15,8),(22,8),(17,13),(19,21),(12,17),(5,21),(7,13),(2,8),(9,8)],4,1,1); s.poly([(12,4),(14,10),(18,10),(15,13),(16,17),(12,15),(8,17),(9,13),(6,10),(10,10)],5); s.px(18,3,7); s.px(21,5,6); s.px(3,4,7); return s
add(star())

def berry():
    s=Spr('EVENT_BERRY',P['berry']); s.poly([(12,7),(7,4),(4,6),(3,12),(6,19),(12,22),(18,19),(21,12),(20,7),(17,4)],3,1,1); s.poly([(12,8),(7,6),(5,8),(5,13),(8,18),(12,20),(16,18),(19,13),(19,8),(16,6)],4); s.line([(12,6),(13,2),(17,1)],6,2); s.poly([(13,3),(17,2),(19,4),(15,5)],5,1,1); s.px(8,9,5); s.px(7,10,5); return s
add(berry())

def tool():
    s=Spr('EVENT_TOOL',P['tool']); s.rect((8,10,15,13),4,1,1); s.rect((5,8,8,15),3,1,1); s.rect((15,8,18,15),3,1,1); s.rect((2,7,5,16),2,1,1); s.rect((18,7,21,16),2,1,1); s.rect((9,11,14,12),5); s.px(3,8,6); s.px(20,8,6); return s
add(tool())

def machine():
    s=Spr('EVENT_MACHINE',P['machine']); s.rect((4,4,20,22),2,1,1); s.rect((6,6,18,13),4,1,1); s.rect((8,8,16,11),5); s.rect((7,16,9,18),6,1); s.ellipse((13,16,15,18),6,1); s.ellipse((17,16,19,18),5,1); s.line([(12,4),(12,1),(16,0)],6,1); s.rect((7,20,17,21),3); return s
add(machine())

def map_():
    s=Spr('EVENT_MAP',P['map']); s.poly([(4,4),(9,2),(14,4),(20,2),(20,20),(15,22),(10,20),(4,22)],4,1,1); s.line([(9,3),(9,20)],2,1); s.line([(14,4),(14,21)],2,1); s.line([(6,16),(9,14),(12,15),(15,11),(18,12)],5,1); s.line([(16,6),(19,9)],6,2); s.line([(19,6),(16,9)],6,2); s.px(7,17,7); s.px(12,14,7); return s
add(map_())

def kit():
    s=Spr('EVENT_KIT',P['kit']); s.rect((4,7,20,21),3,1,1); s.rect((8,4,16,8),2,1,1); s.rect((10,5,14,7),5); s.rect((10,10,14,18),7); s.rect((7,12,17,16),7); s.rect((6,19,18,20),4); s.px(6,9,5); s.px(18,9,5); return s
add(kit())
# event chest points to detailed chest art but keeps separate name for routing
ce=chest('EVENT_CHEST'); ce.pal=P['chest']; add(ce)

# --- item icons ---
def train_item():
    s=Spr('ITEM_TRAIN',P['trainitem']); s.poly([(4,8),(7,6),(9,8),(15,8),(17,6),(20,8),(20,16),(17,18),(15,16),(9,16),(7,18),(4,16)],3,1,1); s.rect((7,10,17,14),4); s.rect((9,11,15,13),6); s.px(5,9,5); s.px(18,9,5); return s
add(train_item())

def care_item():
    s=Spr('ITEM_CARE',P['careitem']); s.ellipse((4,7,20,17),3,1,1); s.rect((5,8,11,16),4); s.rect((12,8,19,16),5); s.rect((11,8,12,16),7); s.rect((11,10,13,14),7); s.px(7,9,6); return s
add(care_item())

def iv_item():
    s=Spr('ITEM_IV',P['ivitem']); s.poly([(12,3),(18,6),(21,12),(18,19),(12,22),(6,19),(3,12),(6,6)],3,1,1); s.poly([(12,5),(17,8),(18,12),(16,17),(12,19),(8,17),(6,12),(8,8)],4); s.line([(9,8),(15,16)],6,1); s.line([(15,8),(9,16)],6,1); s.px(12,7,7); s.px(12,17,7); return s
add(iv_item())

def crown():
    s=Spr('ITEM_CROWN',P['crown']); s.poly([(3,8),(7,13),(11,6),(14,13),(20,7),(19,19),(5,19)],4,1,1); s.rect((5,16,19,20),3,1,1); s.rect((7,17,17,18),5); s.px(8,15,6); s.px(12,14,7); s.px(16,15,6); return s
add(crown())

def charm():
    s=Spr('ITEM_CHARM',P['charm']); s.ellipse((9,1,15,7),2,1,1); s.ellipse((11,3,13,5),0,1,1); s.poly([(12,6),(15,11),(21,12),(16,16),(17,22),(12,19),(7,22),(8,16),(3,12),(9,11)],4,1,1); s.poly([(12,9),(14,13),(18,13),(15,15),(16,18),(12,16),(8,18),(9,15),(6,13),(10,13)],5); s.px(18,8,7); return s
add(charm())

def shiny_item():
    s=Spr('ITEM_SHINY_BERRY',P['shiny']); s.poly([(12,7),(7,4),(4,7),(4,14),(8,20),(12,22),(17,20),(20,14),(20,7),(17,4)],3,1,1); s.poly([(12,8),(8,6),(6,8),(6,14),(9,18),(12,20),(16,18),(18,14),(18,8),(16,6)],4); s.line([(12,6),(14,2),(18,1)],6,1); s.poly([(15,2),(19,2),(17,5)],5,1,1); s.px(4,3,7); s.px(21,7,7); s.px(19,20,7); return s
add(shiny_item())

# --- egg/hatch ---
def egg(name='EGG_BASE',crack=0,glow=False):
    s=Spr(name,P['egg']); s.poly([(12,1),(8,3),(5,8),(4,14),(6,20),(12,23),(18,20),(20,14),(19,8),(16,3)],3,1,1); s.poly([(12,3),(9,4),(7,8),(6,14),(8,18),(12,21),(16,18),(18,14),(17,8),(15,4)],4); s.px(9,7,6); s.px(15,9,6); s.px(10,16,6); s.px(7,12,5); s.px(12,5,7); s.px(8,6,7)
    if crack>=1: s.line([(13,9),(11,12),(13,13),(10,16)],1,1)
    if crack>=2: s.line([(11,12),(8,11),(7,13)],1,1); s.line([(10,16),(13,18),(12,20)],1,1)
    if glow:
        for x,y in [(1,6),(22,6),(2,18),(21,18),(12,0)]: s.px(x,y,7)
    return s
add(egg()); add(egg('EGG_CRACK1',1)); add(egg('EGG_CRACK2',2)); add(egg('EGG_GLOW',2,True))
# shell shards
es=Spr('EGG_SHELL',P['egg']); es.poly([(2,15),(5,10),(8,15),(11,11),(13,16),(16,11),(21,15),(20,21),(3,21)],3,1,1); es.poly([(4,17),(7,14),(9,18),(12,15),(14,19),(17,15),(19,17),(18,20),(5,20)],4); es.px(6,18,7); es.px(16,17,7); add(es)


# --- v3.105.0 motion/feedback FX sprites ---
def fx_impact(name='FX_IMPACT_A', flip=False):
    s=Spr(name,P['fx_impact'])
    if not flip:
        s.poly([(12,1),(14,8),(20,4),(17,10),(23,12),(17,14),(20,21),(14,16),(12,23),(10,16),(4,21),(7,14),(1,12),(7,10),(4,4),(10,8)],4,1,1)
        s.poly([(12,5),(14,10),(18,8),(16,12),(19,13),(15,14),(16,18),(12,15),(8,18),(9,14),(5,13),(8,11),(6,8),(10,10)],5)
    else:
        s.poly([(12,0),(13,7),(19,3),(17,9),(23,10),(18,13),(21,18),(15,16),(13,23),(10,17),(4,21),(6,14),(0,13),(7,10),(3,6),(10,8)],3,1,1)
        s.poly([(12,4),(13,9),(17,7),(15,11),(19,12),(15,13),(17,17),(12,15),(8,18),(9,14),(5,13),(8,10),(6,8),(10,9)],6)
    for x,y in [(2,3),(21,3),(2,20),(21,19)]: s.px(x,y,7)
    return s
add(fx_impact('FX_IMPACT_A')); add(fx_impact('FX_IMPACT_B',True))

def fx_success(name='FX_SUCCESS_A', wide=False):
    s=Spr(name,P['fx_success'])
    # ring + check + small particles
    s.ellipse((3,3,20,20),3,1,1); s.ellipse((6,6,17,17),0,2,1)
    s.line([(7,12),(10,15),(17,8)],5 if not wide else 6,2)
    pts=[(12,0),(1,6),(22,5),(2,18),(21,19)] if not wide else [(4,1),(19,1),(1,12),(22,12),(5,22),(19,22)]
    for x,y in pts: s.px(x,y,7)
    return s
add(fx_success('FX_SUCCESS_A')); add(fx_success('FX_SUCCESS_B',True))

def fx_shiny(name='FX_SHINY_A', alt=False):
    s=Spr(name,P['fx_shiny'])
    stars=[(5,5,3),(17,4,2),(18,16,3),(7,18,2),(12,11,4)]
    if alt: stars=[(4,12,2),(10,4,3),(19,8,3),(14,18,3),(21,19,2)]
    for cx,cy,r in stars:
        s.line([(cx-r,cy),(cx+r,cy)],5 if r<4 else 6,1)
        s.line([(cx,cy-r),(cx,cy+r)],5 if r<4 else 6,1)
        s.px(cx,cy,7)
        if r>=3:
            s.px(cx-1,cy-1,4); s.px(cx+1,cy+1,4)
    return s
add(fx_shiny('FX_SHINY_A')); add(fx_shiny('FX_SHINY_B',True))

def fx_item(name='FX_ITEM_RING_A', alt=False):
    s=Spr(name,P['fx_item'])
    if not alt:
        s.ellipse((2,2,21,21),3,1,1); s.ellipse((5,5,18,18),0,4,1)
        for x,y in [(12,0),(23,12),(12,23),(0,12)]: s.px(x,y,7)
    else:
        s.ellipse((4,4,19,19),4,1,1); s.ellipse((7,7,16,16),0,5,1)
        for x,y in [(4,3),(20,4),(3,20),(20,20)]: s.px(x,y,6)
    return s
add(fx_item('FX_ITEM_RING_A')); add(fx_item('FX_ITEM_RING_B',True))

# Pack 4bpp. Only indices 0..7 are currently used, leaving room for future accents.
def pack(im):
    vals=list(im.getdata()); out=[]
    for i in range(0,len(vals),2): out.append((vals[i]&0xF)|((vals[i+1]&0xF)<<4))
    return out

def pal_to_565(pal):
    return [rgb565(x) for x in pal]

# Deduplicate palettes by content and give stable family names.
pal_names={}
for key,pal in P.items(): pal_names[tuple(pal)]='PAL_'+key.upper()

# Map sprite to palette family by exact palette content.
header=[]
header += ['#pragma once','#include <Arduino.h>','', '// TamaPoke v3.105.0 enhanced 24x24 4bpp UI + FX sprite pack.', '// 0=transparent; 1..7 are object-specific outline/shadow/base/accent/highlight colors.', '// 4bpp keeps richer shading while using only 288 bytes per 24x24 frame.', '#define UI_SPR_W 24', '#define UI_SPR_H 24', '#define UI_SPR_BYTES 288', '', 'struct UiSprite4bpp {', '  const uint8_t *px;', '  const uint16_t *pal;', '};','']
for key,pal in P.items():
    vals=pal_to_565(pal)
    header.append(f'static const uint16_t PAL_{key.upper()}[8] = {{ '+', '.join(f'0x{v:04X}' for v in vals)+' };')
header.append('')
for s in sprites:
    arr=pack(s.im)
    pxname=s.name+'_PX'
    header.append(f'static const uint8_t {pxname}[UI_SPR_BYTES] = {{')
    for i in range(0,len(arr),24): header.append('  '+', '.join(f'0x{x:02X}' for x in arr[i:i+24])+',')
    header.append('};')
    pname=pal_names[tuple(s.pal)]
    header.append(f'static const UiSprite4bpp {s.name} = {{ {pxname}, {pname} }};')
    header.append('')

(ROOT/'ui_sprites.h').write_text('\n'.join(header),encoding='utf-8')

# Preview image, upscaled with nearest-neighbor so users can inspect actual pixel art.
labels=[
 ('TRAINING',['TRAIN_SACK_IDLE','TRAIN_SACK_HIT_L','TRAIN_SHIELD_IDLE','TRAIN_SHIELD_PERFECT','TRAIN_BOLT_A','TRAIN_HEART_IDLE']),
 ('RANDOM EVENTS',['EVENT_CHEST','EVENT_GIFT','EVENT_STAR','EVENT_BERRY','EVENT_TOOL','EVENT_MACHINE','EVENT_MAP','EVENT_KIT']),
 ('ITEMS',['ITEM_TRAIN','ITEM_CARE','ITEM_IV','ITEM_CROWN','ITEM_CHARM','ITEM_SHINY_BERRY']),
 ('EGG / TREASURE',['EGG_BASE','EGG_CRACK1','EGG_CRACK2','EGG_GLOW','EGG_SHELL','CHEST_GROWTH','CHEST_SHINY','CHEST_TECH']),
 ('MOTION FX',['FX_IMPACT_A','FX_IMPACT_B','FX_SUCCESS_A','FX_SUCCESS_B','FX_SHINY_A','FX_SHINY_B','FX_ITEM_RING_A','FX_ITEM_RING_B'])
]
lookup={s.name:s for s in sprites}
BG=(16,22,34); CARD=(28,37,54); EDGE=(77,96,130); TXT=(236,241,251); SUB=(174,198,236)
cardw=124; cardh=132; margin=32; gap=14; scale=3
maxcols=8
width=margin*2+maxcols*cardw+(maxcols-1)*gap
heights=[]
for _,names in labels: heights.append(48+cardh+28)
height=72+sum(heights)+38
out=Image.new('RGB',(width,height),BG); d=ImageDraw.Draw(out)
try:
    font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
    fontb=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',28)
    fonth=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',20)
except:
    font=fontb=fonth=None

d.text((margin,20),'TamaPoke v3.105.0 · Enhanced Pixel + FX Sprite Preview',fill=TXT,font=fontb)
y=72
for title,names in labels:
    d.text((margin,y),title,fill=SUB,font=fonth); y+=38
    for i,name in enumerate(names):
        x=margin+i*(cardw+gap)
        d.rounded_rectangle((x,y,x+cardw-1,y+cardh-1),radius=12,fill=CARD,outline=EDGE,width=2)
        s=lookup[name]
        pal=s.pal
        rgb=Image.new('RGB',(W,H),(0,0,0)); px=rgb.load(); idx=s.im.load()
        for yy in range(H):
            for xx in range(W):
                v=idx[xx,yy]
                px[xx,yy]=pal[v] if v else CARD
        rgb=rgb.resize((W*scale,H*scale),Image.Resampling.NEAREST)
        out.paste(rgb,(x+(cardw-W*scale)//2,y+13))
        short=name.replace('TRAIN_','').replace('EVENT_','').replace('ITEM_','').replace('EGG_','').replace('CHEST_','')
        d.text((x+8,y+98),short,fill=TXT,font=font)
    y+=cardh+28

d.text((margin,height-30),'24x24 · 4bpp · 8-shade indexed pixel art · embedded in firmware',fill=(145,157,180),font=font)
preview=ROOT/'TamaPoke-v3.105.0-FXSprite-Preview.png'
out.save(preview)
print(f'wrote {ROOT/"ui_sprites.h"}')
print(f'wrote {preview}')
print(f'sprites={len(sprites)} bytes/frame={BYTES} pixel_bytes={len(sprites)*BYTES}')
