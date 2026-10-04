#include "rtcbat.h"
#include "pin_config.h"  // define XPOWERS_CHIP_AXP2101
#include <Wire.h>
#include <time.h>
#include <SensorPCF85063.hpp>
#include <XPowersLib.h>

static SensorPCF85063 rtc;
static XPowersPMU pmu;
static bool rtcOk = false;
static bool pmuOk = false;

bool rtcBegin() {
  rtcOk = rtc.begin(Wire, IIC_SDA, IIC_SCL);
  if (!rtcOk) Serial.println("PCF85063 no detectado");
  return rtcOk;
}

uint32_t rtcEpoch() {
  if (!rtcOk) return 0;
  RTC_DateTime t = rtc.getDateTime();
  if (t.getYear() < 2025 || t.getYear() > 2120) return 0;  // sin hora valida
  struct tm tmv = {};
  tmv.tm_year = t.getYear() - 1900;
  tmv.tm_mon = t.getMonth() - 1;
  tmv.tm_mday = t.getDay();
  tmv.tm_hour = t.getHour();
  tmv.tm_min = t.getMinute();
  tmv.tm_sec = t.getSecond();
  time_t e = mktime(&tmv);  // TZ por defecto = UTC, consistente con gmtime_r
  return e > 0 ? (uint32_t)e : 0;
}

void rtcSetEpoch(uint32_t e) {
  if (!rtcOk) return;
  time_t tt = e;
  struct tm tmv;
  gmtime_r(&tt, &tmv);
  rtc.setDateTime(RTC_DateTime(tmv.tm_year + 1900, tmv.tm_mon + 1, tmv.tm_mday,
                               tmv.tm_hour, tmv.tm_min, tmv.tm_sec));
}

bool batBegin() {
  pmuOk = pmu.begin(Wire, AXP2101_SLAVE_ADDRESS, IIC_SDA, IIC_SCL);
  if (!pmuOk) {
    Serial.println("AXP2101 no detectado");
    return false;
  }

  // v3.57.2: explicitly enable the AXP2101 channels used by the battery UI.
  // The board can boot with these ADC/detection bits in different states after
  // a deep discharge or PMU reset, so do not rely on power-on defaults.
  // Match Waveshare 05_LVGL_AXP2101_ADC_Data::adcOn().
  pmu.enableTemperatureMeasure();
  pmu.enableBattDetection();
  pmu.enableVbusVoltageMeasure();
  pmu.enableBattVoltageMeasure();
  pmu.enableSystemVoltageMeasure();
  return true;
}

// Enciende la alimentacion de la AMOLED. En la Waveshare 1.75 el panel (OLED VDD)
// cuelga del rail BLDO1 a 3.3V del AXP2101. El firmware daba por hecho que estaba
// encendido; si el PMU se resetea (drenaje total), BLDO1 queda OFF y la pantalla
// se ve negra aunque el resto funcione. Hay que llamarla ANTES de gfx->begin().
void pmuEnablePanel() {
  if (!pmu.begin(Wire, AXP2101_SLAVE_ADDRESS, IIC_SDA, IIC_SCL)) {
    Serial.println("AXP2101 no detectado (pmuEnablePanel)");
    return;
  }
  pmu.setBLDO1Voltage(3300);   // OLED VDD
  pmu.enableBLDO1();
}

// Battery telemetry follows Waveshare's official AXP2101 Arduino example.
// The vendor demo enables battery detection plus battery/VBUS/system/temperature
// measurements, then reports getBatteryPercent() directly from the AXP2101 fuel
// gauge.  TamaPoke keeps only a short cache to avoid hammering the shared I2C
// bus; it no longer clamps the PMU gauge against a hand-written voltage curve.
static uint32_t powerCacheT = 0;
static int cachedPct = -1;
static uint16_t cachedMv = 0;
static uint16_t cachedVbusMv = 0;
static uint16_t cachedSystemMv = 0;
static float cachedTempC = 0.0f;
static bool cachedCharging = false;
static bool cachedDischarging = false;
static bool cachedUsb = false;
static bool cachedVbusGood = false;
static bool cachedBattery = false;
static uint8_t cachedChargeStatus = 0xFF;

static void refreshPower() {
  uint32_t now = millis();
  if (powerCacheT && now - powerCacheT < 1000) return;
  powerCacheT = now ? now : 1;

  if (!pmuOk) {
    cachedPct = -1;
    cachedMv = cachedVbusMv = cachedSystemMv = 0;
    cachedTempC = 0.0f;
    cachedCharging = cachedDischarging = cachedUsb = cachedVbusGood = cachedBattery = false;
    cachedChargeStatus = 0xFF;
    return;
  }

  cachedBattery = pmu.isBatteryConnect();
  cachedCharging = pmu.isCharging();
  cachedDischarging = pmu.isDischarge();
  cachedUsb = pmu.isVbusIn();
  cachedVbusGood = pmu.isVbusGood();
  cachedChargeStatus = pmu.getChargerStatus();
  cachedTempC = pmu.getTemperature();

  // Same telemetry sources used by Waveshare 05_LVGL_AXP2101_ADC_Data.
  cachedMv = cachedBattery ? pmu.getBattVoltage() : 0;
  cachedVbusMv = cachedUsb ? pmu.getVbusVoltage() : 0;
  cachedSystemMv = pmu.getSystemVoltage();
  int pct = cachedBattery ? (int)pmu.getBatteryPercent() : -1;
  cachedPct = (pct >= 0 && pct <= 100) ? pct : -1;
}

int batPercent() { refreshPower(); return cachedPct; }
uint16_t batVoltageMv() { refreshPower(); return cachedMv; }
bool batCharging() { refreshPower(); return cachedCharging; }
bool batDischarging() { refreshPower(); return cachedDischarging; }
bool usbPresent() { refreshPower(); return cachedUsb; }
bool vbusGood() { refreshPower(); return cachedVbusGood; }
bool batConnected() { refreshPower(); return cachedBattery; }
bool pmuReady() { return pmuOk; }
uint16_t vbusVoltageMv() { refreshPower(); return cachedVbusMv; }
uint16_t systemVoltageMv() { refreshPower(); return cachedSystemMv; }
float pmuTemperatureC() { refreshPower(); return cachedTempC; }
uint8_t batChargerStatus() { refreshPower(); return cachedChargeStatus; }

const char *batChargerStatusText() {
  refreshPower();
  switch (cachedChargeStatus) {
    case XPOWERS_AXP2101_CHG_TRI_STATE: return "TRI";
    case XPOWERS_AXP2101_CHG_PRE_STATE: return "PRE";
    case XPOWERS_AXP2101_CHG_CC_STATE: return "CC";
    case XPOWERS_AXP2101_CHG_CV_STATE: return "CV";
    case XPOWERS_AXP2101_CHG_DONE_STATE: return "DONE";
    case XPOWERS_AXP2101_CHG_STOP_STATE: return "STOP";
    default: return "N/A";
  }
}

void pwrSetup() {
  if (!pmuOk) return;
  pmu.setPowerKeyPressOffTime(XPOWERS_POWEROFF_4S);
  pmu.disableIRQ(XPOWERS_AXP2101_ALL_IRQ);
  pmu.enableIRQ(XPOWERS_AXP2101_PKEY_SHORT_IRQ);
  pmu.clearIrqStatus();
}

bool pwrShortPressed() {
  if (!pmuOk) return false;
  pmu.getIrqStatus();
  bool hit = pmu.isPekeyShortPressIrq();
  if (hit) pmu.clearIrqStatus();
  return hit;
}
