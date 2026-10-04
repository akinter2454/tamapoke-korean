"""Host-run the actual firmware information renderers and layout, no ESP hardware.
Produces JSON drawing traces for offline UI review. g++ and standard library only.
"""
from pathlib import Path
import re,subprocess,tempfile,json,sys,os
ROOT=Path(__file__).resolve().parents[1];s=(ROOT/'TamaPoke.ino').read_text()
def function(name):
 m=re.search(r'(?m)^(?:static\s+)?(?:inline\s+)?[\w*& ]+\b'+re.escape(name)+r'\([^;{}]*\)\s*\{',s)
 assert m,name
 start=m.start();i=m.end();depth=1
 while depth:
  if s[i]=='{':depth+=1
  elif s[i]=='}':depth-=1
  i+=1
 return s[start:i]
base=r'''
#include <algorithm>
#include <cassert>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <iomanip>
#include <iostream>
#include <string>
#include <sstream>
#include <vector>
#include "ui_info_sprites.h"
#include "ui_info_layout.h"
#include "ui_sprites.h"
#define CX 233
#define CY 233
#define C565(r,g,b) ((uint16_t)((((r)>>3)<<11)|(((g)>>2)<<5)|((b)>>3)))
#define TYPE_COUNT 18
#define T_NONE 255
#define DEX_COUNT 4
#define DIGI_SPECIES_COUNT 4
#define KO_FONT_X_BIAS 1
#define KO_FONT_BASELINE_Y 7
#define LANG_KO 0
int gLang=LANG_KO;
uint8_t gUiTextScale=1;
uint32_t testNow=0;
uint32_t millis(){return testNow;}
using std::min;using std::max;
bool tracing=false;
int runs=0;
std::ostringstream trace;
struct Gfx {
 int x=0,y=0,size=1;uint16_t color=0;
 void shape(const char*kind,int x,int y,int w,int h,int r,uint16_t c){
  if(tracing)trace<<"["<<std::quoted(kind)<<","<<x<<","<<y<<","<<w<<","<<h<<","<<r<<","<<c<<"],\n";
 }
 void fillRect(int x,int y,int w,int h,uint16_t c){++runs;shape("rect",x,y,w,h,0,c);}
 void fillRoundRect(int x,int y,int w,int h,int r,uint16_t c){shape("round",x,y,w,h,r,c);}
 void drawRoundRect(int x,int y,int w,int h,int r,uint16_t c){shape("outline",x,y,w,h,r,c);}
 void fillCircle(int x,int y,int r,uint16_t c){shape("circle",x,y,0,0,r,c);}
 void drawCircle(int x,int y,int r,uint16_t c){shape("circle_outline",x,y,0,0,r,c);}
 void drawFastVLine(int x,int y,int h,uint16_t c){fillRect(x,y,1,h,c);}
 void fillScreen(uint16_t c){shape("rect",0,0,466,466,0,c);}
 void setTextColor(uint16_t c){color=c;}
 void setTextSize(uint8_t s){size=s;}
 void setCursor(int xx,int yy){x=xx;y=yy;}
 void print(const char*text){if(tracing)trace<<"[\"text\","<<x<<","<<y-7*size<<","<<size<<","<<color<<","<<std::quoted(text)<<"],\n";}
 void flush(){}
} device,*gfx=&device;
void canvasFillRectFast(int x,int y,int w,int h,uint16_t c){gfx->fillRect(x,y,w,h,c);}
#define RGB565_BLACK 0
struct Pet {
 uint8_t fullness=80,energy=80,hygiene=80,joy=80;
 bool sleeping=false,egg=false,evolution=false,heart=false,ready=false;
 int ceremony=0;int16_t speciesId=1;
 bool isEgg()const{return egg;}bool evolving()const{return evolution;}
 bool eating()const{return false;}bool showMedal()const{return false;}
 bool showMilestone()const{return false;}bool showHeart()const{return heart;}
 bool wantEvolveButton()const{return ready;}
 unsigned badgeCount(bool)const{return 3;}
 bool isRegistered(int)const{return false;}
 bool isDigiRegistered(int)const{return false;}
}pet;
struct CareSlots{uint8_t slot=0;uint8_t active()const{return slot;}}careSlots;
uint32_t bathUntil=0,feedMenuUntil=0,confirmUntil=0,evolveResultUntil=0,itemFxUntil=0;
uint8_t choiceKind=0;bool gymHard=false;
bool gInfoCaptureHome=false,gInfoHomeBoundsValid=false;
UiInfoRect gInfoHomeBounds={0,0,0,0};
bool speciesHasArt(int){return true;}
enum{AIL_NONE,AIL_PARA,AIL_BURN,AIL_POISON,AIL_SLEEP,AIL_FREEZE,AIL_CONFUSE};
enum{SI_ATK,SI_DEF,SI_SPA,SI_SPD,SI_SPE,SI_COUNT};
struct Combatant{uint8_t ailment=0,confuseTurns=0;int8_t stage[SI_COUNT]={};uint16_t maxHp=9999,hp=9000;bool shiny=false;uint8_t level=99;int dex=1;};
const char*localizedTypeName(uint8_t t){static const char *n[]={"노말","불꽃","물","전기","풀","얼음","격투","독","땅","비행","에스퍼","벌레","바위","고스트","드래곤","악","강철","페어리"};return t<18?n[t]:"?";}
const char*btlDisplayName(const Combatant&){return "메탈그레이몬";}
uint8_t creatureType1(int){return 1;}bool isCreatureId(int){return true;}
uint8_t btlSquadAt=0,btlFoeAt=0,btlSquadN=5;
uint8_t btlFoeTeamCount(){return 3;}
uint16_t btlHpShown[2]={9000,9000};
'''
base+='\n'.join(l for l in (ROOT/'species.h').read_text().splitlines() if l.startswith('#define UI_'))+'\n'
base+='\n'.join(l for l in s.splitlines() if l.startswith('#define BTL_HUD_'))+'\n'
types=(ROOT/'types.h').read_text();a=types.index('static const uint16_t TYPE_COL');base+=types[a:]+'\n'
ex=(ROOT/'game_extras.cpp').read_text();tables={}
for name in ['eventTitleKo','eventTextKo']:
 part=ex[ex.index('const char *GameExtras::'+name):];m=re.search(r'N\[9\] = (\{.*?\});',part);tables[name]=m.group(1)
base+='struct Extras { int id=1; uint8_t eventId()const{return id;}\n'
for name,arr in tables.items():base+='const char* '+name+'()const{static const char*N[9]='+arr+';return N[id];}\n'
base+='const char* eventChoiceKo(int i)const{static const char*A[]={"","상자를 연다","선물을 받는다","조각을 챙긴다","바로 먹는다","따라 훈련한다","기계를 켠다","지도 조각을 챙긴다","바로 사용한다"};static const char*B[]={"","같이 놀아준다","이야기한다","별빛을 바라본다","가방에 챙긴다","도구를 챙긴다","그냥 쉰다","산책을 계속한다","가방에 보관한다"};return i?B[id]:A[id];} int bossType(const Pet&)const{return 1;} unsigned towerStreak()const{return 12;} unsigned rivalMinutesLeft(const Pet&)const{return 0;} }extras;\n'
for name in ['uiSetTextSize','uiSetCursor','utf8GlyphCount','uiTextWidth','uiTextHalfWidth','uiFitTextSize','uiEllipsize','uiRoundTextWidth','uiDrawCenteredFit','uiDrawLeftFit','uiFxActive','lerp565','drawInfoSprite','drawUiSprite4bpp','drawHomeInfoEmote','infoTypeChipWidth','drawTypeChip','drawInfoTypePair','drawBattleInfoIcons','uiGamePageBase','uiGameCard','uiGameButton','uiGameBackHint','eventSpriteFor','renderRandomEvent','renderBattleHub','btlHpBar']:
 base+=function(name)+'\n'
btl=function('btlSide');base+=btl[:btl.index('  // A small shadow')]+'}\n'
base+=r'''
static void saveTrace(const char*name){
 std::cout<<"{\"name\":"<<std::quoted(name)<<",\"calls\":["<<trace.str()<<"[\"end\"]]}\n";trace.str("");trace.clear();
}
int main(){
 // Exhaust moving, very wide, tall and off-centre creature bounds.
 int positions=0,hidden=0;
 for(int x=-50;x<=420;x+=13)for(int y=30;y<=280;y+=11)for(int w:{32,96,128,190,270,350}) {
  UiInfoRect body={(int16_t)x,(int16_t)y,(int16_t)w,(int16_t)(304-y)},out;
  if(uiInfoHomePosition(body,out)){assert(uiInfoInsideScene(out));assert(!uiInfoOverlap(body,out));++positions;}
  else ++hidden;
 }
 for(unsigned mask=0;mask<512;++mask){
  unsigned seen=0,count=uiInfoMaskCount(mask);
  if(!count){assert(uiInfoMaskPick(mask,0)==255);continue;}
  for(unsigned i=0;i<count;++i){unsigned idx=uiInfoMaskPick(mask,i);assert(idx<9);seen|=1<<idx;}
  assert(seen==mask);
 }
 for(unsigned ail=0;ail<256;++ail)for(int val=-6;val<=6;++val){
  Combatant c;c.ailment=ail;c.confuseTurns=2;c.stage[SI_ATK]=val;c.stage[SI_DEF]=-val;c.stage[SI_SPE]=val;
  Combatant old=c;drawBattleInfoIcons(82,112,c);assert(!memcmp(&c,&old,sizeof c));
 }
 tracing=true;
 for(int i=1;i<=8;++i){extras.id=i;testNow=i*220;renderRandomEvent();std::string n="event_"+std::to_string(i);saveTrace(n.c_str());}
 renderBattleHub();saveTrace("hub");
 gfx->fillScreen(UI_BG_DAY);
 for(int i=0;i<18;++i)drawTypeChip(84+(i%3)*102,80+(i/3)*50,i);
 saveTrace("types");
 gfx->fillScreen(C565(0x33,0x49,0x53));
 Combatant c;c.ailment=AIL_POISON;c.confuseTurns=2;c.stage[SI_ATK]=2;c.stage[SI_DEF]=-1;c.stage[SI_SPE]=3;
 btlSide(82,82,300,40,c,1);btlSide(250,188,76,166,c,0);saveTrace("battle_max_status");
 // Actual overlay inputs and read-only check.
 for(int scenario=0;scenario<9;++scenario){
  pet=Pet{};pet.energy=55;pet.fullness=55;pet.hygiene=55;pet.joy=55;
  switch(scenario){case 0:pet.fullness=15;break;case 1:pet.energy=35;break;case 2:pet.energy=10;break;case 3:pet.hygiene=10;break;case 4:pet.joy=10;break;case 5:pet.sleeping=true;break;case 6:pet.heart=true;break;case 7:pet.energy=90;break;case 8:pet.ready=true;break;}
  gfx->fillScreen(C565(0x78,0xb8,0xb0));gInfoHomeBoundsValid=true;gInfoHomeBounds={185,200,96,104};
  testNow+=10000;Pet before=pet;int oldRuns=runs;drawHomeInfoEmote();assert(runs>oldRuns);assert(!memcmp(&pet,&before,sizeof pet));
  saveTrace(("emote_"+std::to_string(scenario)).c_str());
  testNow+=2000;oldRuns=runs;drawHomeInfoEmote();assert(oldRuns==runs);
 }
 tracing=false;
 std::cerr<<"PASS: "<<positions<<" safe placements, "<<hidden<<" intentionally hidden, 512 masks, 3328 status combinations, 9 live emotes, expiry, read-only state.\n";
}
'''
with tempfile.TemporaryDirectory() as tmp:
 tmp=Path(tmp);(tmp/'Arduino.h').write_text('#pragma once\n#include <stdint.h>\n#define PROGMEM\n#define pgm_read_byte(p) (*(const uint8_t*)(p))\n#define pgm_read_word(p) (*(const uint16_t*)(p))\n')
 (tmp/'check.cpp').write_text(base)
 cmd=['g++','-std=c++17','-g','-fsanitize=address,undefined','-I'+str(tmp),'-I'+str(ROOT),str(tmp/'check.cpp'),'-o',str(tmp/'check')]
 subprocess.run(cmd,check=True)
 out=subprocess.run([str(tmp/'check')],capture_output=True,text=True,env={**os.environ,"ASAN_OPTIONS":"detect_leaks=0"})
 if out.returncode:
  print(out.stderr);raise SystemExit(out.returncode)
 (ROOT/'previews/info_sprites/draw-traces.jsonl').write_text(out.stdout)
 print(out.stderr.strip());print('PASS: actual firmware render functions compiled and executed under address/undefined-behavior sanitizers')
