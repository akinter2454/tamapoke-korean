from pathlib import Path
from PIL import Image, ImageDraw
import json
R=Path(__file__).resolve().parents[1];D=R/'assets/habitats';(D/'runtime').mkdir(exist_ok=True)
names='normal fire water electric grass ice fighting poison ground flying psychic bug rock ghost dragon dark steel fairy'.split()
W=H=116
out=['#pragma once','#include <stdint.h>','// v3.108.11: named type files, never slice an AI atlas.','static constexpr int HABITAT_WIDTH=116;','static constexpr int HABITAT_HEIGHT=116;','static constexpr int HABITAT_TYPE_COUNT=18;','static const uint8_t HABITAT_PX[18][6728] = {']
pals=[];views=[]
for name in names:
 im=Image.open(D/'source/types'/f'{name}.png').convert('RGB');assert im.size==(W,H)
 q=im.quantize(colors=16,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
 pal=q.getpalette()[:48];colors=[tuple(pal[j:j+3]) for j in range(0,48,3)]
 p=[((r>>3)<<11)|((g>>2)<<5)|(b>>3) for r,g,b in colors];pals.append(p)
 # Previews contain the actual RGB565-rounded runtime palette.
 q.putpalette([v for c in p for v in (((c>>11)&31)*255//31,((c>>5)&63)*255//63,(c&31)*255//31)]+[0]*(768-48))
 q.save(D/'runtime'/f'{name}.png');views.append(q.convert('RGB'))
 v=list(q.getdata());packed=[v[j]|v[j+1]<<4 for j in range(0,len(v),2)]
 out.append('{ // '+name);out.extend(','.join(f'0x{x:02x}' for x in packed[j:j+32])+',' for j in range(0,len(packed),32));out.append('},')
out+=['};','static const uint16_t HABITAT_PAL[18][16] = {'];out+=['{'+','.join(f'0x{x:04x}' for x in p)+'},' for p in pals];out+=['};'];(R/'habitat_assets.h').write_text('\n'.join(out)+'\n')
canvas=Image.new('RGB',(696,1524),'#182031');dr=ImageDraw.Draw(canvas)
for i,p in enumerate(views):
 x=i%3*232;y=i//3*254;canvas.paste(p.resize((232,232),Image.Resampling.NEAREST),(x,y));dr.text((x+8,y+236),names[i],fill='white')
canvas.save(D/'habitats_preview.png')
(D/'manifest.json').write_text(json.dumps(dict(width=W,height=H,colors=16,bits_per_pixel=4,type_order=names,flash_bytes=121680,source='source/types/{type}.png',runtime_scale='complete 116x116 mapped uniformly to complete 466x466; no appended edge',mapping='source/type_mapping.json'),indent=2))
print('18 named backgrounds, 121680 bytes including palettes')
