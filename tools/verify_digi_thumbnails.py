from pathlib import Path
import tempfile,subprocess,os
R=Path(__file__).resolve().parents[1];s=(R/'TamaPoke.ino').read_text();a=s.index('// Six visible box/party slots:');b=s.index('static bool loadBattleDigi(',a);block=s[a:b]
head='''#include <cassert>
#include <algorithm>
#include <cstdio>
#include "digi_thumbnail.h"
uint32_t clockMs=0;uint32_t millis(){return clockMs;}
bool isDigimonId(uint16_t id){return id>=1000;}uint16_t digimonIndex(uint16_t id){return id-1000;}
uint16_t digiPixels[48*48],digiTransparent=1;int digiSpriteW=48,digiSpriteH=48,loads=0,draws=0,missing=0;bool available=true;
bool loadDigiSprite(uint16_t,uint8_t){++loads;return available;}
void drawDigiMissingGlyph(int,int,int,bool){++missing;}
uint16_t digiShinyColor565(uint16_t c,uint16_t){return c;}
void canvasFillRectFast(int x,int y,int w,int h,uint16_t){assert(x>=10&&x+w<=42&&y>=19&&y+h<=51);++draws;}
'''
main='''int main(){
uint16_t output[1026];output[0]=output[1025]=0xabcd;
for(int w: {16,48})for(uint16_t key: {0,1}){
std::fill(digiPixels,digiPixels+2304,key);digiPixels[0]=0xffff;digiPixels[w*w-1]=0xf800;
assert(makeDigiThumbnail(digiPixels,w,w,key,output+1));assert(output[0]==0xabcd&&output[1025]==0xabcd);assert(output[1]==0xffff&&output[1024]==0xf800);
std::fill(digiPixels,digiPixels+2304,key);assert(!makeDigiThumbnail(digiPixels,w,w,key,output+1));
for(int y=0;y<w;++y)digiPixels[y*w+w/2]=0x1234;
assert(makeDigiThumbnail(digiPixels,w,w,key,output+1));int count=0;for(int i=1;i<=1024;++i)if(output[i]!=1)++count;assert(count==32*(32/w));
}
std::fill(digiPixels,digiPixels+2304,0xf800);
for(int i=0;i<6;i++)drawDigiListIcon(1000+i,false,i,10,19);assert(loads==6&&draws>0);
for(int frame=0;frame<20;frame++)for(int i=0;i<6;i++)drawDigiListIcon(1000+i,true,i,10,19);assert(loads==6);
drawDigiListIcon(1010,false,0,10,19);assert(loads==7);
available=false;drawDigiListIcon(1011,false,0,10,19);assert(loads==8&&missing==1);
clockMs=4999;drawDigiListIcon(1011,false,0,10,19);assert(loads==8);
clockMs=5000;available=true;drawDigiListIcon(1011,false,0,10,19);assert(loads==9);
drawDigiListIcon(1011,false,6,10,19);drawDigiListIcon(1,false,0,10,19);assert(loads==9);
printf("PASS: thumbnail bounds/transparency/aspect, six-slot cache, page change, retry, invalid inputs; cache=%zu bytes\\n",sizeof(digiThumbCache));}
'''
# 48px one-pixel-wide input has a clamped one-pixel-wide output.
main=main.replace('32*(32/w)','32*std::max(1,32/w)')
with tempfile.TemporaryDirectory() as tmp:
 p=Path(tmp);(p/'test.cpp').write_text(head+block+main)
 subprocess.run(['g++','-std=c++17','-fsanitize=address,undefined','-I',str(R),str(p/'test.cpp'),'-o',str(p/'test')],check=True)
 subprocess.run([str(p/'test')],check=True,env={**os.environ,'ASAN_OPTIONS':'detect_leaks=0'})
assert s.index('static bool loadDigiSprite(uint16_t id,uint8_t wantedFrame) {')<a
assert s.count('drawDigiListIcon(m.dex,')==2
assert (R/'firmware_source/TamaPoke.ino').read_text()==s
print('PASS: definition order, box+party call sites, mirrored firmware')
