#!/usr/bin/env python3
"""Guard DMUL 16-22 branching, special evolutions/Jogress, and Imperial activation."""
from pathlib import Path
from tamapoke_version import require_semver
import re,json
r=Path(__file__).resolve().parents[1]
FW_VERSION=require_semver(r,'3.96.0')
cpp=(r/'digimon.cpp').read_text(encoding='utf-8')
h=(r/'digimon.h').read_text(encoding='utf-8')
ino=(r/'TamaPoke.ino').read_text(encoding='utf-8')
rows=[(m.group(1),int(m.group(2)),int(m.group(3))) for m in re.finditer(r'D\("([^"]+)",(\d+),(\d+),(\d+),(\d+)\)',cpp)]
assert len(rows)==458
assert 'DIGI_SPECIES_CAP = 2048' in h and 'DIGI_DEVICE_SLOT_COUNT = 18' in h
assert 'return (v>=1&&v<=5)||(v>=10&&v<=22)' in h
assert 'return v>=16&&v<=22' in h
fields={
16:('Dodomon', {'Dorimon','Gigimon'}),17:('Kuramon', {'Tsumemon'}),18:('Pitchmon', {'Moonmon'}),
19:('Bubbmon', {'Mochimon'}),20:('Mokumon', {'Pokomon'}),21:('Botamon', {'Koromon'}),22:('Chibomon', {'DemiVeemon'}),
}
for ver,(baby1,baby2) in fields.items():
    got1=[n for n,vv,s in rows if vv==ver and s==0]
    got2={n for n,vv,s in rows if vv==ver and s==1}
    assert got1==[baby1],(ver,got1)
    assert baby2<=got2,(ver,baby2,got2)
# Four visible training values remain the normal route selectors.
for token in ['const uint16_t tr[4]={a,d,s,h}','uint8_t natural=cur.style&3','tr[natural]==high','digiFindRoute(cur.version,nm[k])']:
    assert token in cpp,token
# Expanded route anchors across all seven versions.
for token in [
 'set4("DORUgamon","Coredramon Blue","Raptordramon","Coredramon Green")',
 'set4("Keramon","Dracmon","Ghostmon","Tsukaimon")',
 'set4("Swimmon","Kamemon","Lunamon","Sangomon")',
 'set4("Gaomon","Pomumon","Funbeemon","Lalamon")',
 'set4("Renamon","Impmon","Gazimon","Goblimon")',
 'set4("Hackmon","Kudamon","Lucemon","Morphomon")',
 'set4("Veemon","Wormmon","Hawkmon","Armadillomon")']:
    assert token in cpp,token
# Balanced/rare Child branches.
for token in ['target("Penmon")','target("Phascomon")','target("Patamon")','target("Coronamon")']:
    assert token in cpp,token
# Special/Jogress targets.
for token in ['target("Examon")','target("Armagemon")','target("GraceNovamon")',
              'target("MirageGaogamon Burst Mode")','target("Beelzebumon Blast Mode")','target("JESmon GX")',
              'target("Lucemon Falldown Mode")','target("Lucemon Satan Mode")',
              'target("Paildramon")','target("Dinobeemon")','target("Silphymon")','target("Shakkoumon")',
              'target("Imperialdramon Dragon Mode")','target("Imperialdramon Fighter Mode")','target("Imperialdramon Paladin Mode")','target("Imperialdramon OmegaX")']:
    assert token in cpp,token
assert 'DMUL Imperial' in cpp
assert 'REGION_COUNT+DIGI_DEVICE_SLOT_COUNT-1' in ino
# Coronamon line uses normal stage power seeds, not special-form 225 power.
for name,power in [('Coronamon',32),('Firamon',52),('Flaremon',100),('Apollomon',180)]:
    assert re.search(r'D\("'+re.escape(name)+r'",21,\d+,'+str(power)+r',',cpp),name
# Type index alignment.
types=json.loads((r/'data/digimon/types.json').read_text(encoding='utf-8'))['entries']
assert len(types)==458 and all(e['index']==i for i,e in enumerate(types))
print(f'DMUL v{FW_VERSION} routes OK: 7 DigiTama, Ver.22 active, OmegaX final evolution and special/Jogress targets present')
