"""Compile 36 separately generated images; never slice an atlas. Pillow required."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
R=Path(__file__).resolve().parents[1];D=R/'assets/habitats'
names='normal fire water electric grass ice fighting poison ground flying psychic bug rock ghost dragon dark steel fairy'.split()
phases=['sunset','night'];W=116
out=['#pragma once','#include <stdint.h>','// Individually generated sunset/night art, 116x116, 4bpp, RGB565.','static const uint8_t HABITAT_TIME_PX[2][18][6728] = {'];pals=[];manifest=[]
for phase in phases:
 out.append('{ // '+phase);pp=[];(D/'runtime'/phase).mkdir(parents=True,exist_ok=True)
 for name in names:
  src=D/'source'/phase/(name+'.png');im=Image.open(src).convert('RGB');assert im.width==im.height,(src,im.size)
  q=im.resize((W,W),Image.Resampling.BOX).quantize(colors=16,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
  raw=q.getpalette()[:48];p=[((raw[i]>>3)<<11)|((raw[i+1]>>2)<<5)|(raw[i+2]>>3) for i in range(0,48,3)];pp.append(p)
  q.putpalette([v for c in p for v in ((c>>11)*255//31,((c>>5)&63)*255//63,(c&31)*255//31)]+[0]*720);q.save(D/'runtime'/phase/(name+'.png'))
  v=list(q.getdata());packed=[v[j]|v[j+1]<<4 for j in range(0,len(v),2)]
  out.append('{ // '+name);out.extend(','.join(str(x) for x in packed[i:i+48])+',' for i in range(0,len(packed),48));out.append('},')
  manifest.append(dict(type=name,phase=phase,source=str(src.relative_to(R)),sha256=hashlib.sha256(src.read_bytes()).hexdigest(),bytes=6760))
 pals.append(pp);out.append('},')
out+=['};','static const uint16_t HABITAT_TIME_PAL[2][18][16] = {']
for pp in pals:out+=['{']+['{'+','.join(str(x) for x in p)+'},' for p in pp]+['},']
out+=['};'];(R/'habitat_time_assets.h').write_text('\n'.join(out)+'\n')
(D/'time_manifest.json').write_text(json.dumps(dict(additional_flash_bytes=243360,total_background_bytes=365040,images=manifest),indent=2))
print('36 images compiled, +243360 flash bytes; no extra framebuffer')
