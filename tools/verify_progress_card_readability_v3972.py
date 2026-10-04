#!/usr/bin/env python3
"""Regression guards for v3.97.2 long single-route evolution readability."""
from pathlib import Path
import re
from tamapoke_version import require_semver

root = Path(__file__).resolve().parents[1]
fw = require_semver(root, "3.97.2")
ino = (root / "TamaPoke.ino").read_text(encoding="utf-8")
fallback = (root / "firmware_source/TamaPoke.ino").read_text(encoding="utf-8")
save_h = (root / "save.h").read_text(encoding="utf-8")

assert re.search(r"#define\s+SAVE_VERSION\s+2\b", save_h), "SAVE_VERSION changed"

start = ino.index("void renderCardProgress()")
end = ino.index("\nvoid renderCard()", start)
card = ino[start:end]

# One logical route must no longer be forced into one 2x line. Short routes use
# 4x directly; long route/result strings wrap at the arrow and keep >=3x.
assert 'if(uiTextWidth(ql[0],4)<=396)' in card
assert 'const char *arrow=strstr(ql[0],"→");' in card
assert 'uiDrawCenteredFit(ql[0],CX,286,396,4,4);' in card
assert 'uiDrawCenteredFit(lhs,CX,272,396,3,3);' in card
assert 'uiDrawCenteredFit(rhs,CX,306,396,4,3);' in card
assert 'const char *plus=strstr(lhs," + ");' in card
assert 'uiDrawCenteredFit(l1,CX,264,396,3,3);' in card
assert 'uiDrawCenteredFit(l2,CX,290,396,3,3);' in card
assert 'uiDrawCenteredFit(rhs,CX,316,396,4,3);' in card

# Two-line routes also get a 3x preferred size when width permits.
assert 'uint8_t qPreferred = qn==2 ? 3 : 2;' in card

# Alphamon Ouryuken was the real-device regression reported by the user.
alpha = '조그 L55 + 오류우몬L55 → 알파몬 왕룡검'
assert alpha in ino
assert '조그 L55 + 알파몬L55 → 알파몬 왕룡검' in ino

def text_width(s: str, size: int) -> int:
    units = sum(6 if ord(ch) < 128 else 8 for ch in s)
    return units * size

lhs, rhs = [part.strip() for part in alpha.split('→', 1)]
rhs = '→ ' + rhs
assert text_width(alpha, 3) > 396, "fixture no longer exercises wrapping"
assert text_width(lhs, 3) <= 396, "Alphamon condition must fit at 3x after wrap"
assert text_width(rhs, 4) <= 396, "Alphamon Ouryuken target must fit at 4x after wrap"

assert ino == fallback, "firmware_source/TamaPoke.ino drift"
print(f"v{fw} progress-card long-route readability OK: Alphamon Ouryuken wraps to 3x/4x")
