from pathlib import Path
from tamapoke_version import require_semver
root=Path(__file__).resolve().parents[1]
s=(root/'TamaPoke.ino').read_text(encoding='utf-8')
FW_VERSION = require_semver(root)
assert '현재 찾기: N.%03d %s  %u/6' in s
assert '찾는 포켓몬: %s  %u/6' in s
assert '찾는 포켓몬: N.%03d  %u/6' in s
assert 'pet.huntTargetDex() == dex' in s
assert 'uiDrawCenteredFit("찾는 중"' in s
assert 'gfx->fillRoundRect(62, 392, 342, 30, 9, UI_BAR_WARN)' in s
assert 'uiDrawCenteredFit(huntFoot, CX, 400, 326, 2, 1)' in s
assert 'pet.huntMisses()' in s
print('Pokedex hunt target UI OK: high-contrast target badge + readable footer')
