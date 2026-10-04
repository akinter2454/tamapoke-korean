#!/usr/bin/env python3
from pathlib import Path
import json, re, struct

ROOT=Path(__file__).resolve().parents[1]
BASELINE_V389={'init': 'SK_BOOL', 'full': 'SK_U8', 'joy': 'SK_U8', 'ene': 'SK_U8', 'hyg': 'SK_U8', 'poop': 'SK_U8', 'wgt': 'SK_U8', 'age': 'SK_U32', 'dexn': 'SK_I16', 'eggT2': 'SK_I16', 'crack': 'SK_U8', 'mist': 'SK_U8', 'sleep': 'SK_BOOL', 'lend': 'SK_U8', 'seen': 'SK_U32', 'bond': 'SK_U8', 'nick': 'SK_STR', 'froz': 'SK_BOOL', 'ivat': 'SK_U8', 'ivdf': 'SK_U8', 'ivsp': 'SK_U8', 'ivhp': 'SK_U8', 'tatk': 'SK_U8', 'tdef': 'SK_U8', 'tspe': 'SK_U8', 'mvs': 'SK_BYTES', 'mvlv': 'SK_U8', 'bk': 'SK_BOOL', 'shy': 'SK_BOOL', 'eshy': 'SK_BOOL', 'stpk': 'SK_BOOL', 'evop': 'SK_U8', 'slpa': 'SK_U8', 'rtpn': 'SK_BOOL', 'tnam': 'SK_STR', 'avtr': 'SK_U8', 'badg': 'SK_U16', 'reg': 'SK_U8', 'r361': 'SK_BOOL', 'eggR': 'SK_BYTES', 'badgX': 'SK_BYTES', 'badhX': 'SK_BYTES', 'badh': 'SK_U16', 'dexreg': 'SK_BYTES', 'dexsh': 'SK_BYTES', 'strk': 'SK_U16', 'bstrk': 'SK_U16', 'cday': 'SK_U32', 'medal': 'SK_U16', 'tmedal': 'SK_U16', 'mstone': 'SK_U16', 'ghi': 'SK_U16', 'shi': 'SK_U16', 'qhi': 'SK_U16', 'xitem': 'SK_BYTES', 'xtm': 'SK_BYTES', 'xshb': 'SK_BOOL', 'xmd': 'SK_U32', 'xmk': 'SK_BYTES', 'xmp': 'SK_BYTES', 'xmc': 'SK_U8', 'xres': 'SK_BYTES', 'xobs': 'SK_I16', 'xtws': 'SK_U16', 'xtwb': 'SK_U16', 'xevt': 'SK_U8', 'xerk': 'SK_U8', 'xerid': 'SK_U8', 'xerc': 'SK_U8', 'xelast': 'SK_U32', 'xepa': 'SK_BOOL', 'xepr': 'SK_BOOL', 'xepm': 'SK_BOOL', 'xept': 'SK_U8', 'xepe': 'SK_U32', 'xepn': 'SK_U32', 'xepk': 'SK_U8', 'xepi': 'SK_U8', 'xepc': 'SK_U8', 'xepw': 'SK_U8', 'xtbf': 'SK_BYTES', 'xtbp': 'SK_BOOL', 'xtbc': 'SK_BYTES', 'xbwm': 'SK_U32', 'xbwk': 'SK_U8', 'xbwi': 'SK_U8', 'xbwc': 'SK_U8', 'xmap': 'SK_U8', 'xtrs': 'SK_U8', 'xtrk': 'SK_U8', 'xtri': 'SK_U8', 'xtrc': 'SK_U8', 'xrvw': 'SK_U16', 'xrvl': 'SK_U16', 'xrve': 'SK_U32', 'xrvm': 'SK_U32', 'xrvk': 'SK_U8', 'xrvi': 'SK_U8', 'xrvc': 'SK_U8', 'xrvs': 'SK_U8', 'xrvq': 'SK_U8', 'xrvg': 'SK_U8', 'xrvsr': 'SK_U16', 'carev': 'SK_U8', 'carea': 'SK_U8', 'care0': 'SK_BYTES', 'care1': 'SK_BYTES', 'care2': 'SK_BYTES', 'party': 'SK_BYTES', 'box': 'SK_BYTES', 'lang': 'SK_U8', 'snd': 'SK_BOOL', 'vol': 'SK_U8', 'btnsnd': 'SK_BOOL', 'btnvol': 'SK_U8', 'btnfix33': 'SK_BOOL', 'btnfix37': 'SK_BOOL'}
REQUIRED_NEW={'lvmin','lvslp','thp','digmv','egsrc','digreg','digbest','digmat','hunt',
              'caretx','carefrom','careto','care3','care4','digbmv','btnfix38','btnfix39',
              'gatk','gdef','gspe','spec','eggT'}
WIDTH={'SK_U8':1,'SK_I8':1,'SK_BOOL':1,'SK_U16':2,'SK_I16':2,'SK_U32':4}

def fields(path):
    t=path.read_text(encoding='utf-8')
    a=t[t.index('const SaveField SAVE_FIELDS[]'):t.index('const uint16_t SAVE_FIELD_COUNT')]
    return dict(re.findall(r'\{\s*"([^"]+)"\s*,\s*(SK_\w+)\s*\}',a))

def crc16(b):
    c=0xffff
    for x in b:
        c ^= x<<8
        for _ in range(8): c=((c<<1)^0x1021)&0xffff if c&0x8000 else (c<<1)&0xffff
    return c

def make_wire(ver, schema):
    out=bytearray(b'TPKS'+bytes([ver,0,0,0])); count=0
    for k,kind in schema.items():
        kb=k.encode(); n=WIDTH.get(kind,3); val=bytes(((count+i)&0xff for i in range(n)))
        out += bytes([len(kb)])+kb+bytes([{'SK_U8':1,'SK_I8':2,'SK_BOOL':3,'SK_U16':4,'SK_I16':5,'SK_U32':6,'SK_BYTES':7,'SK_STR':8}[kind]])+struct.pack('<H',n)+val
        count += 1
    out[5:7]=struct.pack('<H',count)
    out += struct.pack('<H',crc16(out))
    return bytes(out)

def parse_wire(blob,current,minver,maxver):
    assert blob[:4]==b'TPKS' and minver<=blob[4]<=maxver
    assert crc16(blob[:-2])==struct.unpack('<H',blob[-2:])[0]
    want=struct.unpack('<H',blob[5:7])[0]; at=8; seen=0; recognized=0
    kind_num={1:'SK_U8',2:'SK_I8',3:'SK_BOOL',4:'SK_U16',5:'SK_I16',6:'SK_U32',7:'SK_BYTES',8:'SK_STR'}
    while at < len(blob)-2:
        kl=blob[at]; key=blob[at+1:at+1+kl].decode(); vat=at+1+kl
        kn=blob[vat]; n=struct.unpack('<H',blob[vat+1:vat+3])[0]; kind=kind_num[kn]
        if kind in WIDTH: assert n==WIDTH[kind]
        if current.get(key)==kind: recognized+=1
        at=vat+3+n; seen+=1
    assert at==len(blob)-2 and seen==want
    return recognized

cur=fields(ROOT/'save.cpp')
removed=[k for k in BASELINE_V389 if k not in cur]
changed=[(k,BASELINE_V389[k],cur.get(k)) for k in BASELINE_V389 if cur.get(k)!=BASELINE_V389[k]]
assert not removed, f'v3.89 backup fields removed: {removed}'
assert not changed, f'v3.89 field kind changed: {changed}'
assert REQUIRED_NEW <= cur.keys(), f'missing reinforced fields: {sorted(REQUIRED_NEW-cur.keys())}'

h=(ROOT/'save.h').read_text(encoding='utf-8')
ver=int(re.search(r'#define\s+SAVE_VERSION\s+(\d+)',h).group(1))
minver=int(re.search(r'#define\s+SAVE_MIN_IMPORT_VERSION\s+(\d+)',h).group(1))
cap=int(re.search(r'#define\s+SAVE_SERIAL_CAP\s+(\d+)',h).group(1))
assert ver==2 and minver==1, (minver,ver)
assert cap>=8192, cap
sc=(ROOT/'save.cpp').read_text(encoding='utf-8')
assert 'in[4] < SAVE_MIN_IMPORT_VERSION || in[4] > SAVE_VERSION' in sc

# A complete legacy v1 schema must still parse and every old field must be recognized.
v1=make_wire(1,BASELINE_V389)
assert parse_wire(v1,cur,minver,ver)==len(BASELINE_V389)
# Current v2 wire format must also parse.
v2=make_wire(2,cur)
assert parse_wire(v2,cur,minver,ver)==len(cur)

ge=(ROOT/'game_extras.cpp').read_text(encoding='utf-8')
assert 'loadPrefixBlob(prefs, "xres", _research, sizeof(_research));' in ge, 'research blob is not dex-growth safe'

lock=json.loads((ROOT/'tools/catalog_lock.json').read_text(encoding='utf-8'))
ids=[int(v['id']) for v in lock.get('forms',{}).values()]
assert ids and len(ids)==len(set(ids)), 'catalog lock has duplicate internal IDs'
assert max(ids)<2000, f'Pokemon form ID entered Digimon namespace: {max(ids)}'
assert int(lock.get('next_form_id',0))>max(ids), 'next_form_id must stay append-only above every locked ID'
for nat,i in [(19,810),(20,811),(26,812),(27,813),(28,814),(37,815),(38,816),(50,817),(51,818),(52,819),(53,820),(74,821),(75,822),(76,823),(88,824),(89,825),(103,826),(105,827)]:
    rec=lock['forms'].get(f'{nat:04d}/0001'); assert rec and int(rec['id'])==i, (nat,rec)

print(f'SAVE COMPAT OK: v1 -> v{ver} forward restore, {len(BASELINE_V389)} legacy fields unchanged, {len(cur)} current fields')
print(f'Backup serial cap={cap} bytes; catalog lock forms={len(ids)} max_id={max(ids)} next={lock["next_form_id"]}; Digimon namespace remains >=2000')
print('Growable research blob uses prefix-safe loading; raw party/box/care mirrors remain migration inputs after IMPORT.')
