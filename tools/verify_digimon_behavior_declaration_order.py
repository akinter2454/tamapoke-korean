from pathlib import Path

s=(Path(__file__).resolve().parents[1]/"TamaPoke.ino").read_text(encoding="utf-8")
beh=s.index("} beh;")
proto=s.index("static void digiBehNext();")
defn=s.index("static void digiBehNext(){")
assert proto < beh < defn, (proto,beh,defn)
# Ensure no use of beh exists inside a digiBehNext body before its declaration.
assert s.find("beh.t0=now;",0,beh) == -1
print("Digimon behavior declaration order OK: prototype < beh global < function definition")
