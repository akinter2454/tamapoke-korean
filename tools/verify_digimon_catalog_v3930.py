#!/usr/bin/env python3
from pathlib import Path
import re,json,hashlib
from tamapoke_version import require_semver
r=Path(__file__).resolve().parents[1]
cpp=(r/'digimon.cpp').read_text(encoding='utf-8')
h=(r/'digimon.h').read_text(encoding='utf-8')
ino=(r/'TamaPoke.ino').read_text(encoding='utf-8')
rows=[(m.group(1),int(m.group(2)),int(m.group(3)),int(m.group(4)),int(m.group(5))) for m in re.finditer(r'D\("([^"]+)",(\d+),(\d+),(\d+),(\d+)\)',cpp)]
assert len(rows)==458, len(rows)
old=rows[:333]
assert hashlib.sha256(json.dumps(old,separators=(',',':')).encode()).hexdigest()=='c01af200e4db2392620ec396ba3f4c04dd4d244702aac92e017886e54dd4d462', 'legacy Digimon IDs 0..332 changed'
expected=['Dracomon', 'Coredramon Blue', 'Coredramon Green', 'GeoGreymon', 'Wingdramon', 'Groundramon', 'RizeGreymon', 'Slayerdramon', 'Breakdramon', 'Examon', 'Dracmon', 'Ghostmon', 'Tsukaimon', 'Soulmon', 'IceDevimon', 'Sangloupmon', 'Fangmon', 'Witchmon', 'Boogiemon', 'Matadormon', 'Astamon', 'NeoDevimon', 'SkullBaluchimon', 'Wisemon', 'Cerberumon', 'GranDracmon', 'Barbamon', 'Lilithmon', 'BeelStarmon', 'Murmukusmon', 'Swimmon', 'Kamemon', 'Sangomon', 'Penmon', 'Dolphmon', 'Tylomon', 'Tobiumon', 'Orcamon', 'MarinChimairamon', 'Gusokumon', 'WaruSeadramon', 'Divemon', 'Regalecusmon', 'Neptunemon', 'Leviamon', 'AncientMermaimon', 'Pomumon', 'Funbeemon', 'Lalamon', 'Parasaurmon', 'Sunflowmon', 'Waspmon', 'Ajatarmon', 'CannonBeemon', 'Lilamon', 'GrandisKuwagamon', 'TigerVespamon', 'Lotusmon', 'Bancho Lilimon', 'Impmon', 'Gazimon', 'Goblimon', 'Phascomon', 'Sorcermon', 'BlackTailmon', 'Musyamon', 'Fugamon', 'Baalmon', 'Bastemon', 'Archnemon', 'SkullSatamon', 'Beelzebumon', 'Gulfmon', 'Plutomon', 'Kuzuhamon', 'Kudamon', 'Lucemon', 'Patamon', 'Morphomon', 'Gladimon', 'Reppamon', 'Pidmon', 'Darcmon', 'Chirinmon', 'Hippogriffomon', 'Mistymon', 'Seraphimon', 'Ophanimon', 'Duftmon', 'Craniummon', 'Sleipmon', 'Armagemon', 'GraceNovamon', 'Coronamon', 'Firamon', 'Flaremon', 'Apollomon', 'MirageGaogamon Burst Mode', 'Beelzebumon Blast Mode', 'JESmon GX', 'Lucemon Falldown Mode', 'Lucemon Satan Mode', 'Chibomon', 'DemiVeemon', 'Veemon', 'Wormmon', 'Hawkmon', 'Armadillomon', 'ExVeemon', 'Snimon', 'Aquilamon', 'Ankylomon', 'JewelBeemon', 'Yatagaramon', 'Meteormon', 'Paildramon', 'Dinobeemon', 'Silphymon', 'Shakkoumon', 'Valkyrimon', 'Ravmon', 'Imperialdramon Dragon Mode', 'Imperialdramon Fighter Mode', 'Imperialdramon Paladin Mode', 'Imperialdramon OmegaX']
assert [x[0] for x in rows[333:]]==expected
assert len(set(expected))==125
assert (set(expected)&set(x[0] for x in old))=={'Gazimon','Patamon'}, 'only deliberate DMUL/base duplicate names are allowed'
assert rows[333][0]=='Dracomon' and rows[456][0]=='Imperialdramon Paladin Mode' and rows[457][0]=='Imperialdramon OmegaX'
assert any(n=='Chibomon' and v==22 and s==0 for n,v,s,_,_ in rows)
assert any(n=='Imperialdramon Paladin Mode' and v==22 and s==5 for n,v,s,_,_ in rows)
assert any(n=='Imperialdramon OmegaX' and v==22 and s==5 for n,v,s,_,_ in rows)
assert any(n=='GraceNovamon' and v==0 and s==5 for n,v,s,_,_ in rows)
assert 'DIGI_SPECIES_CAP = 2048' in h
FW_VERSION = require_semver(r, "3.93.0")
# v{FW_VERSION} activates Imperial Ver.22 while preserving all catalog IDs.
assert 'DIGI_DEVICE_SLOT_COUNT = 18' in h
assert 'return (v>=1&&v<=5)||(v>=10&&v<=22)' in h
# Korean names and explicit type table stay index-aligned.
kb=cpp.split('static const char *const DIGI_NAMES_KO[] = {',1)[1].split('};',1)[0]
kn=re.findall(r'"([^"]+)"',kb)
assert len(kn)==458, len(kn)
types=json.loads((r/'data/digimon/types.json').read_text(encoding='utf-8'))['entries']
assert len(types)==458 and all(e['index']==i for i,e in enumerate(types))
print(f'v{FW_VERSION} catalog OK: legacy IDs 0..332 fixed, new IDs 333..457 appended, total=458, CAP=2048')
