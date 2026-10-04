"""Build the three v3.110.2 extra UI sprites from the user-provided pixel icon atlas.

Output is firmware-safe 4bpp data using UiInfoSprite. Palette index 0 is transparent.
No game logic or save data is touched.
"""
from pathlib import Path
from PIL import Image
import numpy as np
import json

ROOT = Path(__file__).resolve().parents[1]
ASSET = ROOT / "assets" / "extra_sprites"
SRC = ASSET / "source" / "atlas.png"
RUNTIME = ASSET / "runtime"
RUNTIME.mkdir(parents=True, exist_ok=True)

# The supplied atlas contains exactly: TM disc, gamepad, petting.
# Bounds are measured from the source image's non-transparent pixel groups.
SPECS = [
    ("tm_disc",  (148, 143, 588, 582), 32),
    ("gamepad",  (822, 216, 1350, 551), 24),
    ("petting",  (1603, 146, 2048, 586), 24),
]

im = Image.open(SRC).convert("RGBA")
header = [
    "#pragma once",
    "#include <Arduino.h>",
    "#include \"ui_info_sprites.h\"",
    "// v3.110.3: restored missing v3.110.2 extra UI sprite header.",
    "// Generated from assets/extra_sprites/source/atlas.png.",
    "// 4bpp, low nibble first; palette index 0 is transparent.",
]
manifest = []

for name, box, size in SPECS:
    crop = im.crop(box)
    # Remove fully/near-transparent outer pixels, then fit with a 1px safe border.
    alpha = crop.getchannel("A").point(lambda x: 255 if x >= 24 else 0)
    bbox = alpha.getbbox()
    if bbox:
        crop = crop.crop(bbox)
    crop.thumbnail((size - 2, size - 2), Image.Resampling.BOX)
    tile = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    tile.alpha_composite(crop, ((size - crop.width)//2, (size - crop.height)//2))

    arr = np.asarray(tile)
    opaque = arr[:, :, 3] >= 96
    rgb = tile.convert("RGB")
    q = rgb.quantize(colors=15, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    pal = q.getpalette()
    ix = np.array(q, dtype=np.uint8) + 1
    ix[~opaque] = 0
    colors = [0] + [
        ((pal[i*3] >> 3) << 11) | ((pal[i*3+1] >> 2) << 5) | (pal[i*3+2] >> 3)
        for i in range(15)
    ]
    raw = ix.ravel()
    packed = [int(raw[j]) | (int(raw[j+1]) << 4) for j in range(0, len(raw), 2)]

    sym = "UI_EXTRA_" + name.upper()
    header.append(
        f"static const uint16_t {sym}_PAL[16] PROGMEM = {{" + ",".join(hex(v) for v in colors) + "};"
    )
    header.append(
        f"static const uint8_t {sym}_PX[] PROGMEM = {{" + ",".join(hex(v) for v in packed) + "};"
    )
    header.append(
        f"static const UiInfoSprite {sym} = {{ {sym}_PX, {sym}_PAL, {size} }};"
    )

    # Runtime preview reconstructed from the exact quantized palette.
    out = Image.new("RGBA", (size, size), (0,0,0,0))
    px = out.load()
    for y in range(size):
        for x in range(size):
            idx = int(ix[y, x])
            if not idx:
                continue
            v = colors[idx]
            px[x, y] = (
                ((v >> 11) & 31) * 255 // 31,
                ((v >> 5) & 63) * 255 // 63,
                (v & 31) * 255 // 31,
                255,
            )
    out.save(RUNTIME / f"{name}.png")
    manifest.append({"name": name, "size": size, "bytes": len(packed)+32, "source_box": list(box)})

(ROOT / "ui_extra_sprites.h").write_text("\n".join(header) + "\n", encoding="utf-8")
(ASSET / "manifest.json").write_text(json.dumps({
    "version": "3.110.3",
    "purpose": "restore missing v3.110.2 extra UI sprite header",
    "icons": manifest,
    "total_firmware_bytes": sum(x["bytes"] for x in manifest),
}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"wrote ui_extra_sprites.h with {len(manifest)} sprites; {sum(x['bytes'] for x in manifest)} bytes")
