#!/usr/bin/env python3
from pathlib import Path
import re, sys
ROOT=Path(__file__).resolve().parents[1]
ino=(ROOT/'TamaPoke.ino').read_text()
pet=(ROOT/'pet.cpp').read_text()
ph=(ROOT/'pet.h').read_text()
dh=(ROOT/'digimon.h').read_text()
dc=(ROOT/'digimon.cpp').read_text()
extras=(ROOT/'game_extras.cpp').read_text()

def need(cond,msg):
    if not cond:
        print('FAIL:',msg); sys.exit(1)
    print('PASS:',msg)

mver=re.search(r'^#define\s+FW_VERSION\s+"(\d+)\.(\d+)\.(\d+)"',ino,re.M)
need(bool(mver) and tuple(map(int,mver.groups())) >= (3,99,0),'firmware version keeps v3.99.0+ Digimon Shiny feature')
need('eggShiny = (random(shinyBase) == 0);' in pet,'Digimon eggs share the normal rare-variant roll')
need('eggIsDigimon() ? false' not in pet and 'shiny = eggIsDigimon() ? false' not in pet,'Digimon shiny suppression removed')
need('shiny = eggShiny;' in pet,'hatching preserves shiny for Digimon')
need('!isCreatureId(speciesId)' in pet,'Shiny Berry accepts Pokemon and Digimon')
need('eggShiny = false;' not in re.search(r'void Pet::setDigimonVersion\(.*?\n\}',pet,re.S).group(0),'changing Digimon version cannot erase/reroll shiny state')
need('digiShinyReg' in ph and 'isDigiShinyRegistered' in ph,'player-wide Digimon shiny discovery registry exists')
need('prefs.putBytes("digshy"' in pet and 'loadBlob(prefs, "digshy"' in pet,'Digimon shiny registry is save-compatible')
need('if (shiny) digiShinyReg' in pet,'raising/evolving a shiny Digimon records the shiny form')
need('digiShinyColor565' in ino,'algorithmic RGB565 shiny palette exists')
need('if(hi<=8||lo>=55)return c;' in ino,'outline/highlight preservation guard exists')
need('if(spriteShiny)c=digiShinyColor565' in ino,'home/companion Digimon render uses shiny palette')
need('if(c.shiny)col=digiShinyColor565' in ino,'battle Digimon render uses shiny palette')
need('silhouette?UI_WHITE:(shiny?digiShinyColor565' in ino,'profile/evolution/ceremony helper uses shiny palette without breaking silhouettes')
need('pet.isDigiShinyRegistered(id)' in ino,'Digimon dex exposes shiny discovery marker')
need('bool shiny = false;' in dh and 'bool eggShiny = false;' in dh,'legacy DigiPet stores shiny state')
need('prefs.putBool("shy",shiny)' in dc and 'prefs.getBool("shy",false)' in dc,'legacy DigiPet shiny state persists')
need('if(shiny)shinyRegistered' in dc,'legacy DigiPet shiny discovery persists through forms')
need('현재 포켓몬/디지몬을 Shiny로 변화' in extras,'Shiny Berry UI describes Digimon support')
need((ROOT/'firmware_source/TamaPoke.ino').read_bytes()==(ROOT/'TamaPoke.ino').read_bytes(),'firmware source mirror matches root')
print('Digimon shiny v3.99.0 verifier PASS')
