#pragma once
#include <stdint.h>
// A fixed-size, aspect-preserving thumbnail. 0x0001 is the output color key.
static const int DIGI_THUMB_SIZE = 32;
static bool makeDigiThumbnail(const uint16_t *src, int w, int h,
                              uint16_t transparent, uint16_t *dst) {
  for (int i=0;i<DIGI_THUMB_SIZE*DIGI_THUMB_SIZE;++i) dst[i]=0x0001;
  if (!src || w<=0 || h<=0 || w>48 || h>48) return false;
  int left=w,top=h,right=-1,bottom=-1;
  for(int y=0;y<h;++y)for(int x=0;x<w;++x)if(src[y*w+x]!=transparent){
    if(x<left)left=x;if(x>right)right=x;if(y<top)top=y;if(y>bottom)bottom=y;
  }
  if(right<left)return false;
  int sw=right-left+1,sh=bottom-top+1;
  int dw=sw>=sh?32:sw*32/sh,dh=sh>=sw?32:sh*32/sw;
  if(dw<1)dw=1;if(dh<1)dh=1;
  int ox=(32-dw)/2,oy=(32-dh)/2;
  for(int y=0;y<dh;++y)for(int x=0;x<dw;++x){
    int sx=dw==1?sw/2:x*(sw-1)/(dw-1);
    int sy=dh==1?sh/2:y*(sh-1)/(dh-1);
    uint16_t c=src[(top+sy)*w+left+sx];
    if(c!=transparent)dst[(oy+y)*32+ox+x]=c==0x0001?0x0000:c;
  }
  return true;
}
