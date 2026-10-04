from pathlib import Path
import subprocess,tempfile,zipfile
R=Path(__file__).resolve().parents[1];s=(R/'TamaPoke.ino').read_text()
def function(start,end):return s[s.index(start):s.index(end,s.index(start))]
head='''#include <stdint.h>
#include <cstring>
#include <cassert>
#include <cstdio>
#include "habitat_assets.h"
#include "habitat_time_assets.h"
#define LCD_WIDTH 466
#define LCD_HEIGHT 466
#define TYPE_COUNT 18
#define T_NORMAL 0
int hour=13; int sceneHour(){return hour;}
struct Gfx { uint16_t fb[466*466];bool fallback; uint16_t* getFramebuffer(){return fallback?nullptr:fb;} void fillRect(int x,int y,int w,int h,uint16_t c){assert(x>=0&&x+w<=466&&y>=0&&y+h<=466);for(int j=y;j<y+h;j++)for(int i=x;i<x+w;i++)fb[j*466+i]=c;} } obj,*gfx=&obj;
int pet;struct Extras{int weatherId(int){return 0;}}extras;void drawWeatherOverlay(int,uint32_t,int){}
'''
main='''
int main(){int cases=0;for(hour=0;hour<24;hour++){int phase=(hour<6||hour>=20)?2:hour>=17?1:0;assert(habitatPhase()==phase);
for(int t=0;t<19;t++)for(int fallback=0;fallback<2;fallback++)for(int bottom: {0,312,466,500,-1}){
obj.fallback=fallback;memset(obj.fb,0x77,sizeof(obj.fb));drawTypeScene(t,0,phase==2,232,bottom);int type=t<18?t:0;
const uint8_t *px=phase?HABITAT_TIME_PX[phase-1][type]:HABITAT_PX[type];const uint16_t*pal=phase?HABITAT_TIME_PAL[phase-1][type]:HABITAT_PAL[type];
for(int y=0;y<466;y++)for(int x=0;x<466;x++){uint16_t expected=0x7777;if(y<bottom){int sx=x*116/466,sy=y*116/466;int packed=px[sy*58+sx/2];expected=pal[sx%2?packed>>4:packed&15];}assert(obj.fb[y*466+x]==expected);}cases++;
}}printf("PASS: %d renderer cases, all hours/types, full/partial/clamped draws, both rendering paths\\n",cases);}
'''
code=head+'#include <initializer_list>\n'+function('static uint8_t habitatPhaseForHour(', '// Primary-type habitats')+function('static void drawTypeScene(', '\nvoid drawScene(')+main
with tempfile.TemporaryDirectory() as tmp:
 p=Path(tmp);(p/'check.cpp').write_text(code)
 subprocess.run(['g++','-std=c++17','-O1','-fsanitize=address,undefined','-I',str(R),str(p/'check.cpp'),'-o',str(p/'check')],check=True)
 import os
 subprocess.run([str(p/'check')],check=True,env={**os.environ,'ASAN_OPTIONS':'detect_leaks=0'})
assert 'mix(habitatPhase());' in function('static uint32_t homeBottomSignature()', '// Anything in this set')
assert (R/'firmware_source/TamaPoke.ino').read_bytes()==(R/'TamaPoke.ino').read_bytes()
print('PASS: time phase participates in full-screen invalidation; firmware mirrors match')
