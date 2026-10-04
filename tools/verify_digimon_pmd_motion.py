from pathlib import Path
import re
from tamapoke_version import require_semver
root=Path(__file__).resolve().parents[1]
s=(root/"TamaPoke.ino").read_text(encoding="utf-8")
checks={
"version": bool(require_semver(root, "3.90.1")),
"dgi3 retained": '"DGI3"',
"no DGI4": '"DGI4"' not in s,
"idle": "case DIGI_MOTION_IDLE:   return (elapsed/450u)&1u;" in s,
"walk": "case DIGI_MOTION_WALK:   return (elapsed/320u)&1u;" in s,
"eat 9-8": "case DIGI_MOTION_EAT:    return ((elapsed/260u)&1u)?8u:9u;" in s,
"sleep 11-12": "case DIGI_MOTION_SLEEP:  return 11u+((elapsed/850u)&1u);" in s,
"hurt 13-14": "case DIGI_MOTION_HURT:   return 13u+((elapsed/320u)&1u);" in s,
"attack 6-7": "case DIGI_MOTION_ATTACK: return 6u+((elapsed/300u)&1u);" in s,
"pose 1-2": "case DIGI_MOTION_POSE:   return 1u+((elapsed/300u)&1u);" in s,
"refuse 10": "case DIGI_MOTION_REFUSE: return 10u;" in s,
"walk direction": "flip=movingRight;" in s,
"pokemon-like scheduler": "if(r<35)" in s and "else if(r<60)" in s,
"battle attack": "DIGI_MOTION_ATTACK" in s and "btlLungeUntil" in s,
"battle hurt": "DIGI_MOTION_HURT" in s and "btlHitUntil" in s,
"battle orientation": "bool mirror=who==0;" in s,
"save unchanged": '#define SAVE_VERSION 2' in (root/"save.h").read_text(encoding="utf-8"),
}

assert 'DIGI_MOTION_SICK' in s
assert 'case DIGI_MOTION_SICK:   return 13u+((elapsed/450u)&1u);' in s
assert 'frame=digiMotionFrame(DIGI_MOTION_SICK,now);' in s

bad=[k for k,v in checks.items() if not v]
for k,v in checks.items(): print(("PASS" if v else "FAIL"),k)
if bad: raise SystemExit("FAILED: "+", ".join(bad))
