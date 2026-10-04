from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import re
R=Path(__file__).resolve().parents[1];D=R/'previews';D.mkdir(exist_ok=True)
names='normal fire water electric grass ice fighting poison ground flying psychic bug rock ghost dragon dark steel fairy'.split()
f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18);big=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',25)
s=(R/'species.h').read_text();pal={ch:int(n,16) for ch,n in re.findall(r"case '(.)': return (0x[0-9A-Fa-f]+)",s)}
def rgb(c):return ((c>>11)*255//31,((c>>5)&63)*255//63,(c&31)*255//31)
def sprite(n):
 m=re.search(r'const '+n+r'\[\d+\] = \{(.*?)\n\};',s,re.S);rows=re.findall(r'"([.a-zA-Z]+)"',m.group(1));im=Image.new('RGBA',(len(rows),len(rows)))
 for y,row in enumerate(rows):
  for x,ch in enumerate(row[:len(rows)]):
   if ch in pal:im.putpixel((x,y),(*rgb(pal[ch]),255))
 return im
mask=Image.new('L',(466,466));ImageDraw.Draw(mask).ellipse((0,0,465,465),fill=255)
def bg(name):
 # Exact firmware sampling: floor(destination * 116 / 466).
 small=Image.open(R/'assets/habitats/runtime'/f'{name}.png').convert('RGB')
 out=Image.new('RGB',(466,466));sp=small.load();op=out.load()
 for y in range(466):
  for x in range(466):op[x,y]=sp[x*116//466,y*116//466]
 return out

sheet=Image.new('RGB',(6*242,3*266),'#121824');d=ImageDraw.Draw(sheet)
for i,n in enumerate(names):
 im=bg(n);roundim=Image.new('RGB',im.size,'#080b10');roundim.paste(im,(0,0),mask)
 roundim.save(D/(n+'_round_466.png'));x=i%6*242;y=i//6*266
 sheet.paste(roundim.resize((232,232)),(x+5,y));d.text((x+10,y+237),n.upper(),font=f,fill='white')
sheet.save(D/'ALL_18_ROUND.png')
examples=Image.new('RGB',(3*486,520),'#121824')
for k,(typ,pname) in enumerate([('fire','CHARMANDER'),('water','SQUIRTLE'),('grass','BULBASAUR')]):
 im=bg(typ)
 for box,rad in [((18,10,448,102),22),((18,304,448,448),24)]:
  overlay=Image.new('RGB',im.size,(8,16,41));mixed=Image.blend(im,overlay,.25);m=Image.new('L',im.size);ImageDraw.Draw(m).rounded_rectangle(box,rad,fill=255);im.paste(mixed,(0,0),m)
 d=ImageDraw.Draw(im)
 def center(t,y,font=f):d.text((233,y),t,font=font,anchor='mt',fill='white',stroke_width=2,stroke_fill='#172134')
 center('80%  3.90V',16);center(pname,57,big);center('Feeling happy!',88)
 p=sprite('SPR_'+pname).resize((160,160),Image.Resampling.NEAREST);im.paste(p,(153,122),p)
 for x,y,label,val in [(78,318,'FD',.8),(244,318,'JOY',.7),(78,346,'EN',.9),(244,346,'HY',.85)]:
  d.text((x,y),label,font=f,fill='white',stroke_width=1,stroke_fill='black');d.rounded_rectangle((x+48,y,x+148,y+15),4,fill='#d8d2bd');d.rounded_rectangle((x+50,y+2,x+50+int(96*val),y+13),3,fill='#58b868')
 for x,y,icon in [(134,393,'FOOD'),(200,405,'LIGHT'),(266,405,'CLEAN'),(332,393,'TRAIN')]:
  d.rounded_rectangle((x-30,y-30,x+30,y+30),14,fill='white',outline='#2a2a36',width=2);p=sprite('SPR_ICON_'+icon).resize((32,32),Image.Resampling.NEAREST);im.paste(p,(x-16,y-16),p)
 circle=Image.new('RGB',im.size,'#080b10');circle.paste(im,(0,0),mask);circle.save(D/(typ+'_home_example.png'));examples.paste(circle,(k*486+10,0))
 ImageDraw.Draw(examples).text((k*486+20,480),typ.upper()+' / layout example',font=f,fill='white')
examples.save(D/'HOME_EXAMPLES.png')
print('18 exact background previews + 3 illustrative home layouts')
