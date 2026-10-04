#!/usr/bin/env python3
from pathlib import Path
root=Path(__file__).resolve().parents[1]
rtc=(root/'rtcbat.cpp').read_text(encoding='utf-8')
hdr=(root/'rtcbat.h').read_text(encoding='utf-8')
ino=(root/'TamaPoke.ino').read_text(encoding='utf-8')
checks={
 'official ADC channels': all(x in rtc for x in ['enableTemperatureMeasure()', 'enableBattDetection()', 'enableVbusVoltageMeasure()', 'enableBattVoltageMeasure()', 'enableSystemVoltageMeasure()']),
 'direct fuel gauge': 'pmu.getBatteryPercent()' in rtc and 'cachedPct = (pct >= 0 && pct <= 100) ? pct : -1;' in rtc,
 'no hand voltage curve': 'LIION_CURVE' not in rtc and 'voltagePercent(' not in rtc,
 'battery raw voltage': 'pmu.getBattVoltage()' in rtc,
 'vbus voltage': 'pmu.getVbusVoltage()' in rtc,
 'system voltage': 'pmu.getSystemVoltage()' in rtc,
 'charger status': 'pmu.getChargerStatus()' in rtc and 'batChargerStatusText' in rtc,
 'diagnostic API': all(x in hdr for x in ['vbusVoltageMv()', 'systemVoltageMv()', 'pmuTemperatureC()', 'batConnected()', 'vbusGood()']),
 'on-device BAT page': 'AXP2101 BATTERY' in ino and 'Waveshare official telemetry' in ino and 'BAT_DIAG_X' in ino,
 'serial BAT command': 'line == "BAT"' in ino and 'source=Waveshare AXP2101 official telemetry API' in ino,
 'version': bool(__import__('re').search(r'#define\s+FW_VERSION\s+"3\.(?:99\.[2-9]|(?:[1-9][0-9]{2,})\.[0-9]+)"', ino)),
}
for name,ok in checks.items():
    print(('PASS' if ok else 'FAIL'), name)
if not all(checks.values()): raise SystemExit(1)
