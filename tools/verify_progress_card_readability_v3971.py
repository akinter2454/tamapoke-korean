#!/usr/bin/env python3
"""Regression guards for v3.97.1 progress-card readability on the round display."""
from pathlib import Path
import re
from tamapoke_version import require_semver

root = Path(__file__).resolve().parents[1]
fw = require_semver(root, "3.97.1")
ino = (root / "TamaPoke.ino").read_text(encoding="utf-8")
fallback = (root / "firmware_source/TamaPoke.ino").read_text(encoding="utf-8")
save_h = (root / "save.h").read_text(encoding="utf-8")

# Patch must remain save/catalog compatible.
assert re.search(r"#define\s+SAVE_VERSION\s+2\b", save_h), "SAVE_VERSION changed"

start = ino.index("void renderCardProgress()")
end = ino.index("\nvoid renderCard()", start)
card = ino[start:end]

# Growth level uses one less scale step and is moved upward.
assert 'uiSetTextSize(4);' in card
assert 'uiSetCursor(CX - uiTextHalfWidth(lv, 4), 76);' in card
assert 'int bx = 93, bw = 280, by = 132, bh = 20;' in card
assert 'uiSetCursor(CX - uiTextHalfWidth(nx, 2), 160);' in card

# Evolution summary is shifted upward to free vertical room.
assert 'uiSetCursor(CX - uiTextHalfWidth(T(S_EVO_LABEL), 2), 194);' in card
assert 'uiSetCursor(CX - uiTextHalfWidth(evo, 2), 218);' in card

# Exact next-evolution conditions get a taller, wider panel and are never
# reduced to the unreadable size-1 scale.
assert 'const int16_t qx=36,qy=244,qw=408,qh=104;' in card
assert 'uiDrawCenteredFit("다음 진화 조건",CX,249,390,2,2);' in card
assert 'const int16_t qx=36,qy=244,qw=408,qh=104;' in card
assert 'uiDrawCenteredFit("다음 진화 조건",CX,249,390,2,2);' in card
assert 'uiDrawCenteredFit(ql[qi],CX,qStart+qi*qStep,396,qPreferred,2);' in card
assert 'uiDrawCenteredFit(ql[qi],CX,299+qi*14,356,2,1);' not in card

# The one static route that exceeded size-2 width was compacted without
# changing its actual requirement.
assert '일반 L60 + 오메가몬L55 → 황제드라몬 PM' in ino
assert '일반 L60 + 오메가몬L55 기록 → 황제드라몬 PM' not in ino

# Low-priority care text must not overlap a real evolution-delay warning.
assert 'if (!pet.evoPenalty()) {' in card

# CI fallback remains byte-identical to the canonical sketch.
assert ino == fallback, "firmware_source/TamaPoke.ino drift"

print(f"v{fw} progress-card readability baseline OK: level compacted, evolution UI raised, condition text >=2x")
