#!/usr/bin/env python3
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
ino=(ROOT/'TamaPoke.ino').read_text(encoding='utf-8',errors='ignore')
fallback=(ROOT/'firmware_source'/'TamaPoke.ino').read_text(encoding='utf-8',errors='ignore')
digi=(ROOT/'digimon.cpp').read_text(encoding='utf-8',errors='ignore')
pet=(ROOT/'pet.cpp').read_text(encoding='utf-8',errors='ignore')
pet_h=(ROOT/'pet.h').read_text(encoding='utf-8',errors='ignore')
save_h=(ROOT/'save.h').read_text(encoding='utf-8',errors='ignore')
err=[]
def need(c,m):
    if not c: err.append(m)

m=re.search(r'^#define\s+FW_VERSION\s+"(\d+)\.(\d+)\.(\d+)"',ino,re.M)
need(bool(m) and tuple(map(int,m.groups())) >= (3,109,4),'FW_VERSION must be >= 3.109.4')
need(ino==fallback,'root and fallback sketches differ')
need('D("Paildramon",22,4,225,1)' in digi,'Paildramon ID/stage record changed or missing')
need('D("Imperialdramon Dragon Mode",22,5,225,1)' in digi,'Imperialdramon DM ID/stage record changed or missing')
need('if(!strcmp(n,"Paildramon")||!strcmp(n,"Dinobeemon"))return 45;' in digi,'Paildramon Lv45 gate missing')
need('if(cur.version==22&&(!strcmp(n,"Paildramon")||!strcmp(n,"Dinobeemon"))&&lv>=45)return target("Imperialdramon Dragon Mode");' in digi,'Paildramon -> Imperialdramon DM route missing')
need('return digimonEvolutionTarget(i,level(),trAtk,trDef,trSpe,trHp,digiBest)!=i;' in pet,'Digimon canEvolveNow target check missing')
need('if (pet.currentIsDigimon()) {' in ino and 'choiceKind = pet.canEvolveNow() ? 1 : 0;' in ino,'Digimon normal-evolution dialog dispatch missing')
need('evoPickCount = pet.eligibleEvolutionOptions(evoPickOpts, MAX_EVO_OPTIONS);' in ino,'Pokemon branch picker missing')
need('if (currentIsDigimon()) {' in pet and 'uint16_t next=digimonEvolutionTarget(old,level(),trAtk,trDef,trSpe,trHp,digiBest);' in pet,'Digimon evolve() target resolver missing')
need('#define SAVE_VERSION 2' in save_h,'SAVE_VERSION changed')
# Decline history only controls the home CTA; it is deliberately absent from
# Digimon canEvolveNow()/digimonEvolutionTarget(), so it cannot invalidate a route.
can_block=re.search(r'bool Pet::canEvolveNow\(\) const \{(.*?)\n\}',pet,re.S)
need(bool(can_block) and 'evoDeclinedLv' not in can_block.group(1),'decline history leaked into actual evolution eligibility')
# Lv100 must still satisfy the >=45 special route; no upper-level exclusion is allowed.
need('lv>=45' in digi and 'lv==100' not in digi[digi.find('dmulSpecialEvolutionTarget'):digi.find('uint16_t digimonJogressTarget')], 'max-level gate conflicts with DMUL special evolution')
if err:
    raise SystemExit('Digimon normal evolution v3.109.4 audit failed:\n- '+'\n- '.join(err))
print('Digimon normal evolution v3.109.4 OK: Paildramon Lv45 -> Imperialdramon DM + Digimon dialog dispatch restored; save/jogress/Pokemon paths preserved')
