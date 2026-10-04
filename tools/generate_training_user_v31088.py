from pathlib import Path
from PIL import Image, ImageDraw
import json
R=Path(__file__).resolve().parents[1];D=R/'assets/training/user_sheet'
source=Image.open(D/'original.png').convert('RGBA')
# Measured bounds; paired frames share the same chain/shield anchor and scale.
specs=[('SACK_IDLE',(4,88,452,536),0),('SACK_HIT',(326,88,774,536),0),('SHIELD_IDLE',(762,152,1146,536),1),('SHIELD_SUCCESS',(1134,152,1518,536),1),('BOLT',(356,595,740,979),2),('HEART',(796,593,1180,977),3)]
frames=[]
for name,box,group in specs:
 im=source.crop(box)
 # Crop bag idle narrowly: the right edge otherwise includes hit particles.
 if name=='SACK_IDLE':
  a=im.getchannel('A');a.paste(0,(324,0,448,448));im.putalpha(a)
 im=im.resize((48,48),Image.Resampling.NEAREST)
 frames.append(im)
pals=[]
for g in range(4):
 vis=[(r,gc,b) for im,sp in zip(frames,specs) if sp[2]==g for r,gc,b,a in im.getdata() if a>=96]
 strip=Image.new('RGB',(len(vis),1));strip.putdata(vis)
 raw=strip.quantize(colors=15,method=Image.Quantize.MEDIANCUT).getpalette()[:45]
 pals.append([tuple(raw[j:j+3]) for j in range(0,45,3)])
text=['#pragma once','#include <stdint.h>','// User sheet, 48x48, 4bpp: 0 transparent, 1..15 palette.','enum TrainingArtId { ART_SACK_IDLE, ART_SACK_HIT, ART_SHIELD_IDLE, ART_SHIELD_SUCCESS, ART_BOLT, ART_HEART, ART_COUNT };','static const uint8_t TRAINING_ART_GROUP[ART_COUNT] = {0,0,1,1,2,3};','static const uint16_t TRAINING_ART_PAL[4][16] = {']
for p in pals:text.append('{0,'+','.join(hex(((r>>3)<<11)|((g>>2)<<5)|(b>>3)) for r,g,b in p)+'},')
text+=['};','static const uint8_t TRAINING_ART_PX[ART_COUNT][1152] = {']
preview=Image.new('RGB',(864,344),'#e5eaf2');draw=ImageDraw.Draw(preview)
for i,(im,(name,box,g)) in enumerate(zip(frames,specs)):
 pal=pals[g];idx=[]
 for r,gc,b,a in im.getdata():
  idx.append(0 if a<96 else 1+min(range(15),key=lambda k:sum((a-b)**2 for a,b in zip((r,gc,b),pal[k]))))
 data=[idx[j]|idx[j+1]<<4 for j in range(0,2304,2)]
 text.append('{ // '+name);text.extend(','.join(hex(x) for x in data[j:j+24])+',' for j in range(0,1152,24));text.append('},')
 out=Image.new('RGBA',(48,48));out.putdata([(0,0,0,0) if not k else (*pal[k-1],255) for k in idx]);out.save(D/(name.lower()+'_48.png'))
 for row,bg in [(0,'#e5eaf2'),(1,'#182030')]:
  x=i*144;y=row*172;draw.rectangle((x,y,x+143,y+171),fill=bg)
  big=out.resize((144,144),Image.Resampling.NEAREST);preview.paste(big,(x,y),big);draw.text((x+4,y+148),name,fill='black' if row==0 else 'white')
text+=['};'];(R/'training_art.h').write_text('\n'.join(text)+'\n')
preview.save(D/'PREVIEW_runtime.png')
(D/'manifest.json').write_text(json.dumps({'source_size':source.size,'runtime':48,'bpp':4,'palette_count':4,'runtime_bytes':6912+128+6,'alpha_threshold':96,'frames':[{'name':n,'box':b,'group':g} for n,b,g in specs]},indent=2))
# Update menu/very-small target source images from the same submitted sheet.
for dest,i in [('attack_sandbag',0),('defense_shield',2),('speed_bolt',4),('vitality_heart',5)]:
 im=Image.open(D/(specs[i][0].lower()+'_48.png'));im.save(R/'assets/training/source'/(dest+'.png'))
print('User runtime: 6 x 1152 + 4 x 32 + 6 = 7046 bytes')
