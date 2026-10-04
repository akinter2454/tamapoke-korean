#!/usr/bin/env python3
from pathlib import Path
import re
r=Path(__file__).resolve().parents[1]
ino=(r/'TamaPoke.ino').read_text(encoding='utf-8')
pet=(r/'pet.cpp').read_text(encoding='utf-8')
checks={
 'animation globals declared before use':ino.find('static uint32_t digiActionUntil = 0;') < ino.find('static void digiReact('),
 'state priority':'PetMood mood=pet.mood();' in ino and 'mood==MOOD_SLEEPING' in ino and 'mood==MOOD_EATING' in ino and 'mood==MOOD_SAD' in ino,
 'idle 0/1':'case DIGI_MOTION_IDLE:   return (elapsed/450u)&1u;' in ino,
 'walk 0/1':'case DIGI_MOTION_WALK:   return (elapsed/320u)&1u;' in ino,
 'eat 9/8':"case DIGI_MOTION_EAT:    return ((elapsed/260u)&1u)?8u:9u;" in ino,
 'sleep 11/12':'case DIGI_MOTION_SLEEP:  return 11u+((elapsed/850u)&1u);' in ino,
 'hurt 13/14 battle':'case DIGI_MOTION_HURT:   return 13u+((elapsed/320u)&1u);' in ino and 'df=digiMotionFrame(DIGI_MOTION_HURT' in ino,
 'sick 13/14 home':'case DIGI_MOTION_SICK:   return 13u+((elapsed/450u)&1u);' in ino and 'frame=digiMotionFrame(DIGI_MOTION_SICK,now);' in ino,
 'attack 6/7':'case DIGI_MOTION_ATTACK: return 6u+((elapsed/300u)&1u);' in ino and 'df=digiMotionFrame(DIGI_MOTION_ATTACK' in ino,
 'pose 1/2':"case DIGI_MOTION_POSE:   return 1u+((elapsed/300u)&1u);" in ino,
 'touch/training use pose reaction':'DIGI_ANIM_TOUCH' in ino and 'DIGI_ANIM_TRAIN' in ino and 'frame=digiMotionFrame(DIGI_MOTION_POSE,now);' in ino,
 'walk faces travel direction':'bool movingRight=d>0;' in ino and 'flip=movingRight;' in ino,
 'Pokemon ground':'drawY=PET_GROUND-drawH' in ino,
 'Pokemon evolution FX shared':'drawDigiEvolveFX' in ino and 'if (pet.evolving()) {' in ino and 'drawDigiEvolveFX(now);' in ino,
 'post-evolution pose celebration':'digiEvolveCelebrateUntil=now+1800;' in ino and 'digiMotionFrame(DIGI_MOTION_POSE,now)' in ino,
 'evolution transformation fixed frame 2':'drawDigiFrameCentered(spriteId,2,CX,PET_GROUND,0,false,silhouette,pet.shiny)' in ino,
 'old/new DGI forms alternate':'showOld?previous:current' in ino and 'digimonIndex(pet.prevSpeciesId)' in ino,
 'same halo rays sparks':'int halo=36+(int)(t*150)' in ino and 'for(int i=0;i<12;i++)' in ino and 'for(int i=0;i<10;i++)' in ino,
 'DGI ground alignment':'x=centerX-drawW/2,y=groundY-drawH;' in ino,
 'no PMD load for Digimon':'if (wasDigimon)' in ino and 'else evoPmd.load(old, pet.shiny);' in ino,
 'affection idle animation':'drawDigiFrameCentered(digimonIndex(pet.speciesId),digiMotionFrame(DIGI_MOTION_IDLE,millis()),CX,220,2,false,false,pet.shiny)' in ino and 'drawDigiMissingGlyph(CX,220,2,false);' in ino,
 'Digimon ceremony routing':'if(pet.currentIsDigimon()){drawDigiCeremony();return;}' in ino,
 'farewell pose and walk':'drawDigiCeremony' in ino and 'frame=digiMotionFrame(DIGI_MOTION_POSE,now);' in ino and 'frame=digiMotionFrame(DIGI_MOTION_WALK,now);' in ino and 'flip=true;' in ino,
 'decline gate resets':'evoDeclinedLv = 0;' in pet and 'evoDeclinedLv=0; registerSpecies(speciesId);' in pet,
 'care-independent Digimon evolution gate':'digimonEvolutionTarget(i,level(),trAtk,trDef,trSpe,trHp,digiBest)!=i;' in pet,
 'card agrees':'digimonHasNormalEvolutionPotential(digiId)' in ino and 'digimonHasJogressPotential(digiId)' in ino and 'pet.canJogressNow()' in ino,
 'fusion levels':'if(i==83)return 60;' in (r/'digimon.cpp').read_text(encoding='utf-8') and 'if(i==14||i==32||i==51||i==66||i==48)return 55;' in (r/'digimon.cpp').read_text(encoding='utf-8'),
}
bad=[k for k,v in checks.items() if not v]
if bad: raise SystemExit('Digimon animation/evolution FAIL: '+', '.join(bad))

cpp=(r/'digimon.cpp').read_text(encoding='utf-8')
rows=[(n,int(v),int(s)) for n,v,s,_,_ in re.findall(r'D\("([^"]+)",(\d+),(\d+),(\d+),(\d+)\)',cpp)]
fusion={'Mastemon','Tlalocmon','Aegisdramon','Mitamamon','Voltobautamon','Cernumon','Omegamon','Chaosdramon','Proximamon'}
assert len(rows)==458
for version in (1,2,3,4,5,10,11,12,13,14,15,16,17,18,19,20,21):
    for stage in range(5):
        sources=[n for n,v,s in rows if v==version and s==stage]
        targets=[n for n,v,s in rows if v==version and s==stage+1 and not (version>=10 and n in fusion)]
        assert sources, f'no source forms for version {version} stage {stage}'
        assert 0 < len(targets) <= 12, f'bad evolution targets for version {version} stage {stage}: {len(targets)}'
print('Digimon animation/evolution OK: Pokemon-style DGI3 roles, Sick/Hurt split, fixed-frame-2 evolution + Pose completion, 458-form DMC/P0-P5/DMUL branches')
