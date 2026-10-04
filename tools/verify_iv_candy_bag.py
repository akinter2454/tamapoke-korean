#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ino=(ROOT/'TamaPoke.ino').read_text(encoding='utf-8')

def need(ok,msg):
    if not ok: raise SystemExit('FAIL: '+msg)
need('XITEM_IV' in ino and 'bagCompactChoice=2' in ino, 'compact IV berry selector missing')
need('bagCompactChoice==1?XITEM_TRAIN:XITEM_IV' in ino, 'selector touch mapping missing')
need('pet.ivAtk,pet.ivDef,pet.ivSpe,pet.ivHp' in ino, 'IV selector does not show all four stats')
need('if(y>382){bagCompactChoice=0' in ino, 'selector back control missing')
need('uint8_t pages = bagTab == 0 ? 2 : 5;' in ino, 'compact item bag page count wrong')
print('PASS: compact IV berry remains reusable through a four-stat selector')
