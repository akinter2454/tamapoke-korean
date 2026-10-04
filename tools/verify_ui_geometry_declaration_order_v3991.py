#!/usr/bin/env python3
from pathlib import Path
import re, sys

ROOT = Path(__file__).resolve().parents[1]
s = (ROOT / 'TamaPoke.ino').read_text(encoding='utf-8')

checks = []
def need(cond, msg):
    checks.append((bool(cond), msg))

mver = re.search(r'^#define\s+FW_VERSION\s+"(\d+)\.(\d+)\.(\d+)"', s, re.M)
need(bool(mver) and tuple(map(int, mver.groups())) >= (3, 99, 1), 'firmware is v3.99.1 or newer')

cx = s.find('#define CX 233')
cy = s.find('#define CY 233')
round_fn = s.find('static int16_t uiRoundTextWidth')
center_fn = s.find('static uint8_t uiDrawCenteredFit')
need(cx >= 0 and cy >= 0, 'CX/CY center constants exist')
need(round_fn >= 0 and center_fn >= 0, 'round text helpers exist')
need(cx < round_fn and cy < round_fn, 'CX/CY are declared before uiRoundTextWidth')
need(cx < center_fn and cy < center_fn, 'CX/CY are declared before uiDrawCenteredFit')
need(s.count('#define CX 233') == 1 and s.count('#define CY 233') == 1, 'CX/CY are defined exactly once')

# Guard the exact regression from the GitHub compiler log: no use of CX/CY may
# occur in the early text-helper section before their preprocessor definitions.
helper_start = s.find('static int16_t uiRoundTextWidth')
helper_end = s.find('TouchDrvCST92xx touch;')
helper = s[helper_start:helper_end] if helper_start >= 0 and helper_end > helper_start else ''
need('centerX == CX' in helper and 'y - CY' in helper, 'text helpers still use round-panel center constants')

mirror = (ROOT / 'firmware_source/TamaPoke.ino').read_bytes()
need(mirror == (ROOT / 'TamaPoke.ino').read_bytes(), 'firmware source mirror matches root')

for ok, msg in checks:
    print(('PASS' if ok else 'FAIL') + ': ' + msg)
if not all(ok for ok, _ in checks):
    sys.exit(1)
print('UI geometry declaration-order v3.99.1 verifier PASS')
