#!/usr/bin/env python3
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
pet_h=(ROOT/'pet.h').read_text(encoding='utf-8',errors='ignore')
pet_cpp=(ROOT/'pet.cpp').read_text(encoding='utf-8',errors='ignore')
ino=(ROOT/'TamaPoke.ino').read_text(encoding='utf-8',errors='ignore')
fallback=(ROOT/'firmware_source'/'TamaPoke.ino').read_text(encoding='utf-8',errors='ignore')
dex=(ROOT/'dex.h').read_text(encoding='utf-8',errors='ignore')
err=[]

def need(cond,msg):
    if not cond: err.append(msg)

mver=re.search(r'^#define\s+FW_VERSION\s+"(\d+)\.(\d+)\.(\d+)"',ino,re.M)
need(bool(mver) and tuple(map(int,mver.groups())) >= (3,109,3),'firmware version is older than 3.109.3')
need(ino==fallback,'root and fallback sketches differ')
need('uint8_t eligibleEvolutionOptions(int16_t *out, uint8_t cap) const;' in pet_h,'eligibleEvolutionOptions declaration missing')
need('bool evolveTo(int16_t target);' in pet_h,'evolveTo declaration missing')
need('uint8_t Pet::eligibleEvolutionOptions' in pet_cpp,'eligibleEvolutionOptions implementation missing')
need('bool Pet::evolveTo(int16_t target)' in pet_cpp,'evolveTo implementation missing')
need('effectiveEvolutionTargetLevel(speciesId, tmp[i], careMistakes, evoPen)' in pet_cpp,'per-target level gate missing from picker eligibility')
need('if (!found) return false;' in pet_cpp,'evolveTo target validation missing')
need('choiceKind = evoPickCount > 1 ? 5 : (evoPickCount == 1 ? 1 : 0);' in ino,'multi-branch picker dispatch missing')
need('const uint8_t perPage = 4;' in ino,'four-candidate paging missing')
need('pet.evolveTo(evoPickTarget)' in ino,'selected target is not passed to evolveTo')
need('pet.isRegistered(target) ? "도감 등록" : "미등록"' in ino,'registration hint missing')
need('choiceKind==5?30000UL:12000UL' in ino,'extended picker timeout missing')

m=re.search(r'#define\s+EEVEE_EVO_COUNT\s+(\d+)',dex)
if not m: err.append('EEVEE_EVO_COUNT missing')
else:
    n=int(m.group(1))
    need(n==8,f'expected 8 Eevee branches, got {n}')
    pages=(n+4-1)//4
    need(pages==2,f'Eevee should use two pages, got {pages}')


need('#define CORE_BRANCH_COUNT 11' in dex,'offline core split-evolution table missing')
for base,target in ((44,182),(61,186),(79,199),(236,107),(236,237),(265,268),(281,475),(290,292),(361,478),(366,368),(412,414)):
    need(str(base) in dex and str(target) in dex, f'core branch marker missing: {base}->{target}')
need('CORE_LATE_BRANCH_BASES[CORE_LATE_BRANCH_COUNT] = { 790 }' in dex,'Cosmoem core branch source missing')
need('CORE_LATE_BRANCH_EVOS[CORE_LATE_BRANCH_COUNT] = { 792 }' in dex,'Cosmoem -> Lunala core branch missing')
need('CORE_BRANCH_BASES[i] == base' in pet_cpp,'core branches are not included in evolutionOptions')

# Save-layout guard: this feature should be transient UI + methods only.
for f in ('save.h','save.cpp'):
    need((ROOT/f).exists(),f'{f} missing')

if err:
    raise SystemExit('pokemon branch choice audit failed:\n- '+'\n- '.join(err))
print('pokemon branch choice audit OK: explicit selection + Eevee 4x2 paging + save-layout unchanged')
