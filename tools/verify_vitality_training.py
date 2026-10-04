#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ino = (ROOT / "TamaPoke.ino").read_text(encoding="utf-8")
pet_h = (ROOT / "pet.h").read_text(encoding="utf-8")
pet_cpp = (ROOT / "pet.cpp").read_text(encoding="utf-8")
party_h = (ROOT / "party.h").read_text(encoding="utf-8")
party_cpp = (ROOT / "party.cpp").read_text(encoding="utf-8")

def need(ok, message):
    if not ok:
        raise SystemExit("FAIL: " + message)

for token in ("hpOpen", "startVitalityGame", "vitalityTap", "renderVitality", "HP_ROUNDS 12"):
    need(token in ino, f"vitality minigame missing {token}")
need('"체력 훈련"' in ino and "for (int i = 0; i < 4; i++)" in ino,
     "fourth training row missing")
need("pet.trainVitality(hpScore)" in ino, "vitality score is not applied")
need("hpIvReward = grantTrainingIvBerry(rewardReady, hpIvRewardCount)" in ino, "vitality reward does not use compact IV berry")
need("uint8_t id = XITEM_IV;" in ino and "XITEM_IV_HP, rewardReady" not in ino,
     "training still generates legacy stat-specific IV candy")
need("count = random(100) < 30 ? 9 : 5;" in ino and "random(100) >= 30" in ino,
     "vitality does not share the established candy/Shiny reward rates")
need("uint8_t trAtk = 0, trDef = 0, trSpe = 0, trHp = 0;" in pet_h,
     "live vitality training field missing")
need("uint8_t Pet::trainVitality" in pet_cpp and 'putUChar("thp", trHp)' in pet_cpp,
     "vitality training is not applied or persisted")
need("10 + trHp" in pet_cpp, "live maximum HP ignores vitality training")
need("uint8_t trHp = 0" in party_h and "10 + m.trHp" in party_cpp,
     "banked maximum HP ignores vitality training")
need("score * 2 / 3" in pet_cpp and "hits * 2 / 3" in pet_cpp and "hits / 3" in pet_cpp,
     "increased training gain formulas missing")

print("PASS: four-stat training, faster gains, selectable compact IV berry and matched rewards verified")
