#!/usr/bin/env python3
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
h=(ROOT/'digimon.h').read_text(encoding='utf-8')
d=(ROOT/'digimon.cpp').read_text(encoding='utf-8')
p=(ROOT/'pet.cpp').read_text(encoding='utf-8')
ph=(ROOT/'pet.h').read_text(encoding='utf-8')
save=(ROOT/'save.cpp').read_text(encoding='utf-8')
sh=(ROOT/'save.h').read_text(encoding='utf-8')

cap=int(re.search(r'DIGI_SPECIES_CAP\s*=\s*(\d+)',h).group(1))
count=len(re.findall(r'\bD\("', d))
maxval=int(re.search(r'#define\s+MAX_VAL\s+(\d+)',save).group(1))
serial=int(re.search(r'#define\s+SAVE_SERIAL_CAP\s+(\d+)',sh).group(1))

assert cap==2048, cap
assert count==458, count
assert cap-count==1590, (cap,count)
assert count<=cap
assert maxval>=cap, (maxval,cap)
assert 2000+cap-1 < 32768, 'Digimon creature namespace exceeds int16_t'
assert 'uint8_t digiBest[DIGI_SPECIES_CAP]' in ph
assert 'uint8_t digiReg[(DIGI_SPECIES_CAP + 7) / 8]' in ph
assert 'uint8_t bestLevel[DIGI_SPECIES_CAP]' in h
assert 'uint8_t registered[(DIGI_SPECIES_CAP+7)/8]' in h

# Persistence must follow live catalog length, NOT the reserved capacity.
assert 'prefs.putBytes("digbest", digiBest, DIGI_SPECIES_COUNT);' in p
assert 'prefs.putBytes("digreg", digiReg, (DIGI_SPECIES_COUNT + 7u) / 8u);' in p
assert 'prefs.putBytes("best",bestLevel,DIGI_SPECIES_COUNT);' in d
assert 'prefs.putBytes("reg",registered,(DIGI_SPECIES_COUNT+7u)/8u);' in d

# Prefix-safe loads are what preserve old saves when arrays grow.
assert 'loadBlob(prefs, "digreg", digiReg, sizeof(digiReg));' in p
assert 'loadBlob(prefs, "digbest", digiBest, sizeof(digiBest));' in p
assert 'min(rl,sizeof(registered))' in d
assert 'min(bl,sizeof(bestLevel))' in d

# A full future 2048-species best-level blob is still legal in save.cpp.
assert maxval == 2048
assert serial >= 8192

# Starter counting must not wrap at 255 if a future device family gets large.
assert 'static uint16_t countOf(uint8_t ver, uint8_t stage)' in d
assert 'uint16_t pick=(uint16_t)random(n);' in d

old_cap=352
old_reg=(old_cap+7)//8
new_reg=(cap+7)//8
# Migration model: old arrays are a prefix of the new zero-filled arrays.
old_best=bytes((i%101 for i in range(old_cap)))
old_bits=bytes((i*7)&0xff for i in range(old_reg))
new_best=bytearray(cap); new_best[:len(old_best)]=old_best
new_bits=bytearray(new_reg); new_bits[:len(old_bits)]=old_bits
assert new_best[:old_cap]==old_best and not any(new_best[old_cap:])
assert new_bits[:old_reg]==old_bits and not any(new_bits[old_reg:])

print(f'DIGIMON CAPACITY OK: roster={count}, cap={cap}, free={cap-count}')
print(f'RAM reserve arrays: best={cap} B + registry={new_reg} B per owner; two owners ~= {(cap+new_reg)*2} B')
print(f'Persistence today follows roster: best={count} B, registry={(count+7)//8} B; old cap={old_cap} prefix migration preserved')
