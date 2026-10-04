#!/usr/bin/env python3
"""Regression checks for the v3.109.5 local battle roster picker.

Local battles use five live-raising care slots first, while party/box remain
selectable without changing their storage. LAN deliberately keeps the legacy
current+party wire-compatible mapping.
"""
from pathlib import Path
from tamapoke_version import require_semver

ROOT = Path(__file__).resolve().parents[1]
SRC = (ROOT / "TamaPoke.ino").read_text(encoding="utf-8")


def body(signature: str) -> str:
    start = SRC.find(signature)
    if start < 0:
        raise SystemExit(f"missing function: {signature}")
    brace = SRC.find("{", start)
    depth = 0
    for pos in range(brace, len(SRC)):
        if SRC[pos] == "{": depth += 1
        elif SRC[pos] == "}":
            depth -= 1
            if depth == 0: return SRC[brace + 1:pos]
    raise SystemExit(f"unterminated function: {signature}")

local_build = body("static void buildLocalSquad(uint8_t maxLvl")
legacy_build = body("static void buildSquad(uint8_t maxLvl")
exists = body("bool pickExists(uint8_t n) {")
local_exists = body("static bool localPickExists(uint8_t n) {")
draw = body("static void drawPickCell(uint8_t n")
render = body("void renderPick() {")
tap = body("void pickTap(int16_t x, int16_t y) {")
open_picker = body("static void openLocalBattlePicker(uint8_t mode, uint8_t cap) {")
boss_start = body("void startBossBattle() {")
boss_tap = body("void bossTap(int16_t x,int16_t y){")
wild_tap = body("void wildEncounterTap(int16_t x,int16_t y){")
tower_tap = body("void towerTap(int16_t x, int16_t y) {")
rival_tap = body("void rivalTap(int16_t x,int16_t y){")
rival_start = body("void startRivalBattle() {")
trainer_start = body("void startTrainerBattle(uint8_t idx, bool hard) {")
screen = body("uint8_t uiCurrentScreen() {")
main_render = body("void render() {")
on_tap = body("void onTap(int16_t x, int16_t y) {")

checks = {
    "five care slots still declared": "#define CARE_SLOT_COUNT 5" in (ROOT / "care_slots.h").read_text(encoding="utf-8"),
    "32-bit selection mask": "uint32_t squadMask" in SRC and "1UL <<" in SRC,
    "local roster bit layout": all(x in SRC for x in ("PICK_CARE_BASE", "PICK_PARTY_BASE", "PICK_BOX_BASE", "PICK_LOCAL_COUNT")),
    "care candidates": "n < CARE_SLOT_COUNT" in local_exists and "careSlotDex(n)" in local_exists,
    "party candidates preserved": "party.slots[p]" in local_exists,
    "box candidates preserved": "party.box[b]" in local_exists,
    "five care combatants": "for (uint8_t i = 0; i < CARE_SLOT_COUNT" in local_build and "combatantFromCareSlot" in local_build,
    "party combatants preserved": "party.slots[i]" in local_build and "combatantFromParty" in local_build,
    "box combatants preserved": "party.box[i]" in local_build and "combatantFromParty" in local_build,
    "care labels 1..5": 'snprintf(source, sizeof(source), "육성%u"' in draw,
    "three local tabs": all(x in render for x in ('"육성"', '"파티"', '"박스"')) and "i < 3" in render,
    "care first on fresh entry": "pickSourceTab = 0" in open_picker and "pickDefault(cap)" in open_picker,
    "gym uses selected local roster": "buildLocalSquad(top" in trainer_start,
    "boss picker mode": "#define PICK_BOSS" in SRC and "PICK_BOSS,3" in boss_tap,
    "boss exact-three rule": "pickChosen() == 3" in render and "pickChosen() != 3" in tap,
    "boss uses selected local roster": "buildLocalSquad(0, 3, squadMask)" in boss_start,
    "wild opens picker": "openLocalBattlePicker(PICK_WILD,3)" in wild_tap,
    "tower opens picker": "openLocalBattlePicker(PICK_TOWER,TRAINER_TEAM_MAX)" in tower_tap,
    "rival opens picker": "openLocalBattlePicker(PICK_RIVAL,3)" in rival_tap,
    "rival uses selected roster": "buildLocalSquad(0,3,squadMask)" in rival_start,
    "LAN remains legacy party-only": "PICK_LAN" in exists and "buildSquad(0, TRAINER_TEAM_MAX, squadMask)" in SRC,
    "legacy LAN builder unchanged": "party.slots[i]" in legacy_build and "party.box[i]" in legacy_build,
    "picker owns screen priority": screen.find("if (pickOpen)") < screen.find("if (bagOpen"),
    "picker owns render priority": main_render.find("if (pickOpen)") < main_render.find("if (bagOpen"),
    "picker owns touch priority": on_tap.find("if (pickOpen)") < on_tap.find("if (bagOpen"),
    "new firmware identifiable": bool(require_semver(ROOT, "3.109.5")),
}

failed = [name for name, ok in checks.items() if not ok]
if failed:
    raise SystemExit("roster battle picker regression failed: " + ", ".join(failed))

print("v3.109.5 roster picker OK: care slots 1..5 + party/box tabs; gym/boss/wild/tower/rival unified; LAN legacy preserved")
