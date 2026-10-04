#!/usr/bin/env python3
"""Regression guards for v3.97.0 compact Digimon names and evolution quick-view UI."""
from pathlib import Path
import re
from tamapoke_version import require_semver

root = Path(__file__).resolve().parents[1]
fw = require_semver(root, "3.97.0")
cpp = (root / "digimon.cpp").read_text(encoding="utf-8")
h = (root / "digimon.h").read_text(encoding="utf-8")
ino = (root / "TamaPoke.ino").read_text(encoding="utf-8")
fallback = (root / "firmware_source/TamaPoke.ino").read_text(encoding="utf-8")
pend = (root / "pendulum_names_ko.inc").read_text(encoding="utf-8")
save_h = (root / "save.h").read_text(encoding="utf-8")

# Feature release must not alter the persistent format or catalog size/IDs.
assert re.search(r"#define\s+SAVE_VERSION\s+2\b", save_h), "SAVE_VERSION changed"
rows = re.findall(r'D\("([^"]+)",(\d+),(\d+),(\d+),(\d+)\)', cpp)
assert len(rows) == 458, len(rows)
assert rows[0][0] and rows[457][0] == "Imperialdramon OmegaX"

# Full Korean-name table remains index-aligned with all 458 species.
kb = cpp.split('static const char *const DIGI_NAMES_KO[] = {', 1)[1].split('};', 1)[0]
ko_names = re.findall(r'"([^"]+)"', kb)
assert len(ko_names) == 458, len(ko_names)

# Confirmed Korean localized names corrected in the current UI table.
required_names = [
    "파피몬", "뽀글몬", "딜비트몬", "어니몬", "제퍼가몬", "추추몬",
    "아큐라몬", "황금아르마몬", "주엘비몬", "다이노몬", "실피드몬", "토우몬",
    "치코몬", "꼬마몬", "그라디몬", "레파몬", "두프트몬", "워매몬", "콩알몬",
    "퍼펫몬", "프리지몬", "켄터스몬", "고래몬", "메탈콩알몬", "고스몬", "두리몬",
    "째리몬", "모털몬", "실리컨몬", "꼬끼몬", "데이터몬", "다이버몬", "드라고몬",
    "모야몬", "데블드라몬", "태스크몬", "파워드라몬", "빅콩알몬", "배드퍼펫몬",
]
for name in required_names:
    assert name in ko_names, f"localized Korean display name missing: {name}"

# Retired/incorrect display spellings must not remain in the active full-name table.
retired = [
    "나니몬", "데비드라몬", "터스크몬", "무겐드라몬", "빅마메몬", "와루몬자에몬",
    "누메몬", "마메몬", "몬자에몬", "유키다루몬", "켄타루몬", "웨이몬", "바케몬",
    "드리모게몬", "기로몬", "모쟈몬", "코엘라몬", "코카토리몬", "나노몬", "항가몬",
    "다고몬", "글라디몬", "렙파몬", "듀프트몬",
]
for old in retired:
    assert old not in ko_names, f"retired Korean spelling remains in DIGI_NAMES_KO: {old}"

# The legacy Pendulum UI table must use the same corrected Korean display vocabulary.
for old in ["코엘라몬", "웨이몬(완전체)", "항가몬", "다고몬", "바케몬", "빅마메몬",
            "와루몬자에몬", "무겐드라몬", "메탈마메몬", "가부몬"]:
    assert old not in pend, f"retired Pendulum display spelling remains: {old}"
for name in ["실리컨몬", "고래몬(완전체)", "다이버몬", "드라고몬", "고스몬", "빅콩알몬",
             "배드퍼펫몬", "파워드라몬", "메탈콩알몬", "파피몬"]:
    assert name in pend, f"corrected Pendulum display name missing: {name}"

# Small-screen short-name helper is display-only; species keys and IDs stay untouched.
assert "const char *digimonNameKoShort(uint16_t index)" in cpp
assert "const char *digimonNameKoShort(uint16_t index);" in h
short_pairs = [
    ("Omegamon Alter-S", "오메가몬S"),
    ("Dukemon Crimson Mode", "듀크몬 CM"),
    ("MirageGaogamon Burst Mode", "미라쥬가오가몬 BM"),
    ("Beelzebumon Blast Mode", "베르제브몬 BM"),
    ("Lucemon Falldown Mode", "루체몬 FD"),
    ("Lucemon Satan Mode", "루체몬 SM"),
    ("Imperialdramon Dragon Mode", "황제드라몬 DM"),
    ("Imperialdramon Fighter Mode", "황제드라몬 FM"),
    ("Imperialdramon Paladin Mode", "황제드라몬 PM"),
    ("Imperialdramon OmegaX", "황제드라몬 OX"),
    ("Coredramon Blue", "코어드라몬 청"),
    ("Coredramon Green", "코어드라몬 녹"),
]
for key, display in short_pairs:
    assert f'!strcmp(n,"{key}")' in cpp and f'return "{display}"' in cpp, (key, display)
assert "return DIGI_NAMES_KO[index];" in cpp
assert 'if (isDigimonId(id)) return digimonNameKoShort(digimonIndex(id));' in cpp

# Progress card exposes actual next evolution conditions without requiring an external chart.
for token in [
    "digiEvolutionQuickLines", "digiJogressQuickLine", "다음 진화 조건",
    "일반 L%u · 훈련합 %u", "공→%s · 방→%s", "속→%s · 체→%s",
    "조그 L25 + 스나이몬L25 → 파일드라몬", "일반 L70 · 공+속100 → 황제드라몬 OX",
    "최종 형태 · 추가 진화 없음",
]:
    assert token in ino, token
assert ino.count("digimonNameKoShort(") >= 8, "small-screen views are not consistently using short names"

# User-facing quick-view text must use the corrected localized name for Mugendramon.
assert "파워드라몬L55" in ino and "파워드라몬 Lv.55" in ino
assert "무겐드라몬" not in ino

# Fallback source used by CI must remain byte/text identical to the root sketch.
assert ino == fallback, "firmware_source/TamaPoke.ino drift"

print(f"v{fw} Digimon name/evolution QoL OK: 458 names aligned, compact labels, on-device evolution conditions")
