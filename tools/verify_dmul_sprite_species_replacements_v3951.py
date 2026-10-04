#!/usr/bin/env python3
from pathlib import Path
import json,re,csv
from tamapoke_version import require_semver
ROOT=Path(__file__).resolve().parents[1]
cpp=(ROOT/'digimon.cpp').read_text(encoding='utf-8')
ino=(ROOT/'TamaPoke.ino').read_text(encoding='utf-8')
rows=[m.groups() for m in re.finditer(r'D\("([^"]+)",(\d+),(\d+),(\d+),(\d+)\)',cpp)]
FW_VERSION = require_semver(ROOT, "3.95.1")
assert len(rows)==458
assert rows[360][0]=='Lilithmon' and rows[360][1:3]==('17','5')
assert rows[393][0]=='Gazimon' and rows[393][1:3]==('20','2')
assert rows[410][0]=='Patamon' and rows[410][1:3]==('21','2')
assert 'Belphemon: Sleep Mode' not in cpp
assert 'Shamamon' not in cpp
assert 'Luxmon' not in cpp
assert 'set4("Renamon","Impmon","Gazimon","Goblimon")' in cpp
assert 'if(!strcmp(n,"Gazimon"))return set4("Fugamon","Musyamon","Sorcermon","BlackTailmon");' in cpp
assert 'if(!strcmp(n,"Patamon"))return set4("Gladimon","Reppamon","Pidmon","Darcmon");' in cpp
assert 'target("Patamon")' in cpp
for token in [
 'set4("Barbamon","GranDracmon","BeelStarmon","Lilithmon")',
 'set4("Barbamon","Lilithmon","GranDracmon","Murmukusmon")',
 'set4("Murmukusmon","Lilithmon","BeelStarmon","GranDracmon")',
 'set4("GranDracmon","Lilithmon","Murmukusmon","BeelStarmon")']:
    assert token in cpp, token
j=json.loads((ROOT/'data/digimon/types.json').read_text(encoding='utf-8'))['entries']
assert (j[360]['name'],j[360]['type1'],j[360]['type2'])==('Lilithmon','DARK','FAIRY')
assert (j[393]['name'],j[393]['type1'],j[393]['type2'])==('Gazimon','DARK','NORMAL')
assert (j[410]['name'],j[410]['type1'],j[410]['type2'])==('Patamon','FLYING','FAIRY')
manifest=(ROOT/'TamaPoke-v3.95.1-DMUL-ID-283-457-Manifest.csv').read_text(encoding='utf-8')
assert '360,d360.dgi,Lilithmon,17,Dark,5' in manifest
assert '393,d393.dgi,Gazimon,20,Nightmare,2' in manifest
assert '410,d410.dgi,Patamon,21,Secret,2' in manifest
for name in ['Belphemon: Sleep Mode','Shamamon','Luxmon']:
    assert name not in manifest
for tool in [ROOT/'tools/TamaPoke-DMUL-Expanded-Sprite-Downloader-v3.95.1-r13.html', ROOT/'tools/TamaPoke-Digimon-SD-Pack-Maker-v3.95.1-r17-458.html']:
    text=tool.read_text(encoding='utf-8')
    for name in ['Lilithmon','Gazimon','Patamon']: assert name in text
    for name in ['Belphemon: Sleep Mode','Shamamon','Luxmon']: assert name not in text
print(f'v{FW_VERSION} DMUL sprite species replacements OK: ID360 Lilithmon, ID393 Gazimon, ID410 Patamon; IDs/count preserved')
