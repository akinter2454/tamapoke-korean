#!/usr/bin/env python3
"""Regression checks for card-only evolution and explicit manual Jogress choice.

This verifier intentionally ignores harmless C++ whitespace/style differences.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / 'TamaPoke.ino').read_text(encoding='utf-8')
PET = (ROOT / 'pet.cpp').read_text(encoding='utf-8')


def function_body(source: str, signature: str) -> str:
    start = source.find(signature)
    if start < 0:
        raise SystemExit(f'missing function: {signature}')
    brace = source.find('{', start)
    depth = 0
    for pos in range(brace, len(source)):
        if source[pos] == '{':
            depth += 1
        elif source[pos] == '}':
            depth -= 1
            if depth == 0:
                return source[brace + 1:pos]
    raise SystemExit(f'unterminated function: {signature}')


def require(text: str, pattern: str, msg: str) -> None:
    if not re.search(pattern, text, re.S):
        raise SystemExit(msg)


touch = function_body(SOURCE, 'void onTap(int16_t x, int16_t y) {')
stats = function_body(SOURCE, 'void renderCardStats() {')
card = function_body(SOURCE, 'void renderCard() {')
render = function_body(SOURCE, 'void render() {')

# Card stats must expose both choices when applicable. Normal evolution uses
# canEvolveNow() directly so a declined Lv.100 evolution is never permanently hidden.
for token in ('pet.canEvolveNow()', 'pet.canJogressNow()', 'CARD_EVO_X', 'CARD_EVO_Y', '"일반 진화"', '"조그레스"'):
    if token not in stats:
        raise SystemExit(f'card stats evolution control missing: {token}')

# Touch routing: accept any harmless whitespace around assignments/comparisons.
require(touch, r'cardPage\s*==\s*1', 'card evolution touch path missing: cardPage == 1')
if not (re.search(r'choiceKind\s*=\s*1\s*;', touch, re.S) or 'openNormalEvolutionDialog()' in touch):
    raise SystemExit('card evolution touch path missing: normal evolution choice')
require(touch, r'choiceKind\s*=\s*4\s*;', 'card evolution touch path missing: Jogress choice')

for token in ('pet.evolve()', 'pet.jogress()', 'pet.declineEvolve()'):
    if token not in touch:
        raise SystemExit(f'card evolution decision missing: {token}')

# Confirm dialog must be rendered inside the card, not as the old home CTA.
require(card, r'choiceKind\s*==\s*1', 'normal evolution confirmation missing from card')
require(card, r'choiceKind\s*==\s*4', 'Jogress confirmation missing from card')
if 'drawChoiceDialog()' not in card:
    raise SystemExit('evolution confirmation must render inside the card')
if 'drawEvolveButton()' in render:
    raise SystemExit('home render must not draw the evolution button')
if 'EVO_BTN_X' in touch or 'EVO_BTN_Y' in touch:
    raise SystemExit('home touch handler still exposes the old evolution button')

# Pet API must keep Jogress separate from normal evolution.
for token in ('uint16_t Pet::jogressTarget() const', 'bool Pet::canJogressNow() const', 'bool Pet::jogress()'):
    if token not in PET:
        raise SystemExit(f'Pet manual Jogress API missing: {token}')
require(PET, r'bool\s+Pet::canEvolveNow\(\)\s+const.*?digimonEvolutionTarget',
        'normal Digimon evolution path missing')
require(PET, r'uint16_t\s+Pet::jogressTarget\(\)\s+const.*?digimonJogressTarget',
        'Jogress target is not separated from normal evolution')

print('card-only evolution UI regression OK: normal evolution and Jogress are explicitly selectable')
