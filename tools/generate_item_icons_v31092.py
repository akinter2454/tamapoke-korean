from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import re,json
R=Path(__file__).resolve().parents[1];D=R/'assets/items';(D/'runtime').mkdir(exist_ok=True)
p=R/'ui_sprites.h';s=p.read_text();names=['TRAIN','CARE','IV','CROWN','CHARM','SHINY_BERRY'];sheet=Image.new('RGB',(720,320),'#eef3f8');dr=ImageDraw.Draw(sheet);font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',14)
for i,n in enumerate(names):
 im=Image.open(D/'source'/f'{n}.png').convert('RGBA');alpha=im.getchannel('A');assert alpha.getextrema()[0]==0,'requires transparency'
 box=alpha.point(lambda x:255 if x>=128 else 0).getbbox();im=im.crop(box);im.thumbnail((20,20),Image.Resampling.LANCZOS)
 tile=Image.new('RGBA',(24,24));tile.paste(im,((24-im.width)//2,(24-im.height)//2))
 colors=[rgb[:3] for rgb in tile.getdata() if rgb[3]>=128];strip=Image.new('RGB',(len(colors),1));strip.putdata(colors);q=strip.quantize(colors=7,dither=Image.Dither.NONE)
 pal=q.getpalette()[:21];rgb=[tuple(pal[j:j+3]) for j in range(0,21,3)];rgb565=[0]+[((r>>3)<<11)|((g>>2)<<5)|(b>>3) for r,g,b in rgb];indices=[];preview=Image.new('RGBA',(24,24))
 for k,c in enumerate(tile.getdata()):
  idx=0 if c[3]<128 else 1+min(range(7),key=lambda j:sum((c[ch]-rgb[j][ch])**2 for ch in range(3)));indices.append(idx)
  if idx:
   v=rgb565[idx];preview.putpixel((k%24,k//24),((v>>11)*255//31,((v>>5)&63)*255//63,(v&31)*255//31,255))
 packed=[indices[j]|indices[j+1]<<4 for j in range(0,576,2)];arr='static const uint8_t ITEM_'+n+'_PX[UI_SPR_BYTES] = {\n'+','.join(f'0x{x:02x}' for x in packed)+'\n};'
 s,count=re.subn(r'static const uint8_t ITEM_'+n+r'_PX\[UI_SPR_BYTES\] = \{.*?\n\};',lambda _:arr,s,flags=re.S);assert count==1
 palname='PAL_NEW_ITEM_'+n;s=re.sub(r'static const uint16_t '+palname+r'\[8\] = \{.*?\};\n','',s)
 decl='static const uint16_t '+palname+'[8] = {'+','.join(hex(x) for x in rgb565)+'};\n'
 s=s.replace(arr,decl+arr);s=re.sub(r'(ITEM_'+n+r' = \{ ITEM_'+n+r'_PX, )\w+',lambda m:m[1]+palname,s)
 preview.save(D/'runtime'/f'{n}.png');x=(i%3)*240;y=(i//3)*160;big=preview.resize((96,96),Image.Resampling.NEAREST);sheet.paste(big,(x+72,y+15),big);dr.text((x+60,y+125),n,font=font,fill='#182638')
p.write_text(s);sheet.save(D/'ITEMS_PREVIEW.png');print('6 icons compiled: 24x24, transparent + 7 colors, 1824 bytes total')
