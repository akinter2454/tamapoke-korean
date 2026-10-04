#!/usr/bin/env python3
from pathlib import Path
import re
from tamapoke_version import require_semver

root = Path(__file__).resolve().parents[1]
fw = require_semver(root, "3.98.0")
battle = (root / "battle.cpp").read_text(encoding="utf-8")
ino = (root / "TamaPoke.ino").read_text(encoding="utf-8")

# Combatant.name is 12 bytes. Four Korean UTF-8 syllables already require
# 12 bytes before the NUL terminator, so a canonical Korean species name must
# never be stored in this transport/nickname field.
assert len("아쿠스타".encode("utf-8")) > 11

for fn in ("combatantFromPet", "combatantFromParty"):
    start = battle.index("void " + fn)
    end = battle.index("\n}\n", start) + 3
    body = battle[start:end]
    assert "creatureName(" not in body, f"{fn} still copies canonical species name into Combatant.name"
    assert "else c.name[0] = 0;" in body, f"{fn} does not leave canonical species names dex-derived"

m = re.search(r'static const char \*btlDisplayName\(const Combatant &c\) \{(.*?)\n\}', ino, re.S)
assert m, "btlDisplayName missing"
body = m.group(1)
assert 'if (c.name[0]) return c.name;' in body, "nickname path missing"
assert 'creatureName(c.dex)' in body, "canonical species name is not derived from dex"
assert 'DEX_TBL[c.dex].name' not in body, "old canonical-name comparison path remains"

# Gym and generic mission/adventure/tower opponents all funnel through the
# corrected constructors, so both battle entry paths inherit the fix.
assert 'foeFromSpecies(btlFoe' in ino
assert 'combatantFromPet(btlFoe, foe);' in ino
assert 'combatantFromPet(c, foe);' in ino

print(f'v{fw} battle-name regression OK: canonical Korean names stay dex-derived; Combatant.name is nickname-only')
