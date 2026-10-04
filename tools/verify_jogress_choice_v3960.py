#!/usr/bin/env python3
from pathlib import Path
from tamapoke_version import require_semver
r=Path(__file__).resolve().parents[1]
cpp=(r/'digimon.cpp').read_text(encoding='utf-8')
h=(r/'digimon.h').read_text(encoding='utf-8')
pet=(r/'pet.cpp').read_text(encoding='utf-8')
ph=(r/'pet.h').read_text(encoding='utf-8')
ino=(r/'TamaPoke.ino').read_text(encoding='utf-8')
FW_VERSION = require_semver(r, "3.96.0")
assert 'digimonJogressTarget' in h and 'uint16_t digimonJogressTarget' in cpp
# Automatic evolution resolver must not contain the legacy fusion precedence.
evo=cpp[cpp.index('uint16_t digimonEvolutionTarget'):]
evo=evo[:evo.index('\n}')+2]
for forbidden in ['pendulumFusionTarget(', 'DIGI_OMNIMON_ALTER_S', 'DIGI_CHAOSMON', 'DIGI_MILLENNIUMMON']:
    assert forbidden not in evo, forbidden
# Explicit Jogress resolver covers all selectable families.
jog=cpp[cpp.index('uint16_t digimonJogressTarget'):cpp.index('uint16_t digimonEvolutionTarget')]
for token in ['pendulumFusionTarget', 'DIGI_OMNIMON_ALTER_S', 'Examon', 'GraceNovamon', 'JESmon GX', 'Paildramon', 'Dinobeemon', 'Silphymon', 'Shakkoumon']:
    assert token in jog, token
assert 'uint16_t Pet::jogressTarget() const' in pet
assert 'bool Pet::canJogressNow() const' in pet
assert 'bool Pet::jogress()' in pet
assert 'bool canJogressNow() const;' in ph and 'bool jogress();' in ph
assert '"일반 진화"' in ino and '"조그레스"' in ino
assert 'choiceKind==4' in ino or 'choiceKind == 4' in ino
print(f'v{FW_VERSION} Jogress choice OK: explicit fusion path no longer preempts normal evolution')
