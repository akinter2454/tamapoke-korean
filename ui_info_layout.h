#pragma once
#include <stdint.h>
// Pure display geometry; half-open bounds, no Pet fields or persistence.
struct UiInfoRect { int16_t x, y, w, h; };
static inline bool uiInfoOverlap(UiInfoRect a, UiInfoRect b) {
  return a.x < b.x+b.w && b.x < a.x+a.w && a.y < b.y+b.h && b.y < a.y+a.h;
}
static inline bool uiInfoInsideScene(UiInfoRect r) {
  if(r.x<18 || r.y<142 || r.x+r.w>448 || r.y+r.h>308) return false;
  for(uint8_t i=0;i<4;++i) {
    int32_t dx=(i&1?r.x+r.w:r.x)-233, dy=(i&2?r.y+r.h:r.y)-233;
    if(dx*dx+dy*dy>225L*225L) return false;
  }
  return true;
}
static inline bool uiInfoHomePosition(UiInfoRect body, UiInfoRect &out) {
  // Above the moving head first. Tall sprites use the nearest free side.
  const int16_t size=24, gap=6;
  int16_t cy=body.y<142?142:body.y;
  if(cy>278)cy=278;
  UiInfoRect candidates[5] = {
    {(int16_t)(body.x+(body.w-size)/2),(int16_t)(body.y-size-gap),size,size},
    {(int16_t)(body.x+body.w+gap),cy,size,size},
    {(int16_t)(body.x-size-gap),cy,size,size},
    {38,150,size,size},{404,150,size,size}
  };
  for(uint8_t i=0;i<5;++i) if(uiInfoInsideScene(candidates[i]) && !uiInfoOverlap(body,candidates[i])) {
    out=candidates[i];return true;
  }
  return false; // No safe space: never cover the header, care tabs or creature.
}
static inline uint8_t uiInfoMaskCount(uint16_t mask) {
  uint8_t n=0;for(;mask;mask>>=1) n+=mask&1;return n;
}
static inline uint8_t uiInfoMaskPick(uint16_t mask,uint32_t turn) {
  uint8_t count=uiInfoMaskCount(mask);if(!count)return 255;
  uint8_t at=turn%count;
  for(uint8_t i=0;i<9;++i)if(mask&(1U<<i)){if(!at)return i;--at;}
  return 255;
}
