#!/usr/bin/env python3
"""Regression guard for the browser-only Pendulum sprite importer and current DGI3 motion roles."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
html = (ROOT / "tools/Digimon-SD-Pack-Maker.html").read_text(encoding="utf-8")
standalone = ROOT / "tools/Digimon-Pendulum-DMUL-SD-Pack-Maker-v3.87.0.html"
ino = (ROOT / "TamaPoke.ino").read_text(encoding="utf-8")

for token in (
    "let upload=s.match(/^([0-5])", "(?:vb|ns|ds|wg|me)", "pendulumOnly", "onlyDMUL",
    "scope=${scope}", "whamonperfect", "bakumon",
    "gatomon:'tailmon'", "omnimon:'omegamon'",
    "DGI3", "15,48,48", "id&255", "d${String(id).padStart(3,'0')}.dgi",
):
    assert token in html, f"converter regression: missing {token!r}"

# DMC / Pendulum / DMUL share the current DGI3 role table.  Keep the stable
# DGI3 format while validating roles instead of the pre-v3.90.1 literal code.
for token in (
    "case DIGI_MOTION_IDLE:   return (elapsed/450u)&1u;",
    "case DIGI_MOTION_WALK:   return (elapsed/320u)&1u;",
    "case DIGI_MOTION_EAT:    return ((elapsed/260u)&1u)?8u:9u;",
    "case DIGI_MOTION_SLEEP:  return 11u+((elapsed/850u)&1u);",
    "case DIGI_MOTION_HURT:   return 13u+((elapsed/320u)&1u);",
    "case DIGI_MOTION_SICK:   return 13u+((elapsed/450u)&1u);",
    "case DIGI_MOTION_ATTACK: return 6u+((elapsed/300u)&1u);",
    "case DIGI_MOTION_POSE:   return 1u+((elapsed/300u)&1u);",
    "flip=movingRight",
    "drawY=PET_GROUND-drawH",
    "sx=flip?digiSpriteW-1-px:px",
):
    assert token in ino, f"firmware animation regression: missing {token!r}"

assert standalone.exists(), "standalone Pendulum converter missing"
assert standalone.read_bytes() == (ROOT / "tools/Digimon-SD-Pack-Maker.html").read_bytes(), \
    "standalone converter is not synchronized"
print("PASS: DMC/Pendulum/DMUL importer, DGI3 output and current Pokemon-style Digimon motion roles verified")
