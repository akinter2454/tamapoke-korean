#!/usr/bin/env python3
from pathlib import Path
import re
R=Path(__file__).resolve().parents[1]
s=(R/'TamaPoke.ino').read_text();h=(R/'training_art.h').read_text()
body=h.split('TRAINING_ART_PX[ART_COUNT][1152] = {',1)[1]
frames=re.findall(r'\{ // (\w+)\n(.*?)\},',body,re.S)
assert len(frames)==6
payload=[]
for name,b in frames:
 v=[int(n,16) for n in re.findall(r'0x[0-9a-f]+',b)];assert len(v)==1152,name
 assert any(v),name;payload.append(v)
assert payload[0]!=payload[1] and payload[2]!=payload[3]
assert 'pal[idx]' in s and 'sackArtHitUntil = millis() + 110;' in s
assert 'sackArtHitUntil = 0;\n  sackNewHi' in s
assert 'feedbackActive && defFeedback >= 1 && defFeedback <= 3' in s
assert 'drawTrainingArt(ART_BOLT' in s and 'drawTrainingArt(ART_HEART' in s
assert s==(R/'firmware_source/TamaPoke.ino').read_text()
print('PASS: six 48px frames, 1152 bytes each, distinct hit/success art, timer reset, all game hookups, source mirror')
