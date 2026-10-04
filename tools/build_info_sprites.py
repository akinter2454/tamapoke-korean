"""Pack the generated atlas into bounded 4bpp firmware sprites (index 0 transparent)."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np,json
ROOT=Path(__file__).resolve().parents[1]
A=ROOT/'assets/info_sprites'; im=Image.open(A/'source/atlas.png').convert('RGBA')
rows=[(0,215,['burn','poison','paralysis','sleep','confusion','freeze','atk_up','atk_down']),
(215,388,['def_up','def_down','spe_up','spe_down','hungry','tired','low_energy','bath']),
(388,567,['bored','sleepy','happy','train','evolve','type_normal','type_fire','type_water']),
(567,738,['type_grass','type_electric','type_ice','type_fighting','type_poison','type_ground','type_flying','type_psychic','type_bug']),
(738,918,['type_rock','type_ghost','type_dragon','type_dark','type_steel','type_fairy','hub_gym','hub_wild']),
(918,1086,['hub_boss','hub_tower','hub_rival'])]
emotes={'hungry','tired','low_energy','bath','bored','sleepy','happy','train','evolve'}
entries=[];header=['#pragma once','#include <Arduino.h>','// Generated from assets/info_sprites/source/atlas.png. Do not edit pixel arrays.','// 4bpp, low nibble first; palette index 0 is transparent. No heap or SD I/O.','struct UiInfoSprite { const uint8_t *pixels; const uint16_t *palette; uint8_t size; };']
mask=np.asarray(im)[:,:,3]>100
for y1,y2,names in rows:
 on=mask[y1:y2].sum(axis=0)>2;edges=np.diff(np.r_[False,on,False].astype(int));segs=list(zip(np.where(edges==1)[0],np.where(edges==-1)[0]));assert len(segs)==len(names),(names,segs)
 for (x1,x2),name in zip(segs,names):
  crop=im.crop((int(x1),y1,int(x2),y2));crop=crop.crop(crop.getchannel('A').point(lambda x:255 if x>100 else 0).getbbox())
  crop.save(A/'source'/f'{name}.png')
  size=32 if name.startswith('hub_') else 24 if name in emotes else 18
  # Keep one transparent pixel around each icon; alpha threshold removes antialias fringes.
  crop.thumbnail((size-2,size-2),Image.Resampling.BOX)
  tile=Image.new('RGBA',(size,size));tile.alpha_composite(crop,((size-crop.width)//2,(size-crop.height)//2))
  a=np.asarray(tile);opaque=a[:,:,3]>=110
  rgb=tile.convert('RGB');q=rgb.quantize(colors=15,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
  pal=q.getpalette();ix=np.array(q,dtype=np.uint8)+1;ix[~opaque]=0
  colors=[0]+[((pal[i*3]>>3)<<11)|((pal[i*3+1]>>2)<<5)|(pal[i*3+2]>>3) for i in range(15)]
  raw=ix.ravel();packed=[int(raw[j])|(int(raw[j+1])<<4) for j in range(0,len(raw),2)]
  sym=name.upper();header.append('static const uint16_t UI_INFO_'+sym+'_PAL[16] PROGMEM = {'+','.join(hex(v) for v in colors)+'};')
  header.append('static const uint8_t UI_INFO_'+sym+'_PX[] PROGMEM = {'+','.join(hex(v) for v in packed)+'};')
  header.append('static const UiInfoSprite UI_INFO_'+sym+' = { UI_INFO_'+sym+'_PX, UI_INFO_'+sym+'_PAL, '+str(size)+' };')
  runtime=Image.new('RGBA',(size,size));px=runtime.load()
  for y in range(size):
   for x in range(size):
    idx=int(ix[y,x]);v=colors[idx];px[x,y]=(((v>>11)&31)*255//31,((v>>5)&63)*255//63,(v&31)*255//31,255 if idx else 0)
  runtime.save(A/'runtime'/f'{name}.png')
  entries.append({'name':name,'size':size,'bytes':len(packed)+32,'source_cell':[int(x1),y1,int(x2),y2]})
order=['normal','fire','water','electric','grass','ice','fighting','poison','ground','flying','psychic','bug','rock','ghost','dragon','dark','steel','fairy']
header.append('static const UiInfoSprite *const UI_INFO_TYPES[18] = {'+','.join('&UI_INFO_TYPE_'+n.upper() for n in order)+'};')
header.append('static const UiInfoSprite *const UI_INFO_HUB[5] = {&UI_INFO_HUB_GYM,&UI_INFO_HUB_WILD,&UI_INFO_HUB_BOSS,&UI_INFO_HUB_TOWER,&UI_INFO_HUB_RIVAL};')
(ROOT/'ui_info_sprites.h').write_text('\n'.join(header)+'\n');(A/'manifest.json').write_text(json.dumps({'origin':'image_gen built-in; generated atlas, cropped, quantized to 4bpp','type_order':order,'total_bytes':sum(e['bytes'] for e in entries),'icons':entries},indent=2))
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',12)
sheet=Image.new('RGB',(960,720),'#17283b');d=ImageDraw.Draw(sheet)
for i,e in enumerate(entries):
 x=i%8*120;y=i//8*120;pic=Image.open(A/'runtime'/(e['name']+'.png'));big=pic.resize((pic.width*3,pic.height*3),Image.Resampling.NEAREST);sheet.paste(big,(x+(120-big.width)//2,y+4),big);d.text((x+5,y+102),e['name'],font=font,fill='white')
sheet.save(ROOT/'previews/info_sprites/Sprite-Catalog.png')
print(len(entries),'sprites;',sum(e['bytes'] for e in entries),'bytes in packed pixel data + palettes')
