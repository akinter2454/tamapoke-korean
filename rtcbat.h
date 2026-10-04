#pragma once
#include <Arduino.h>

// RTC PCF85063: hora persistente mientras la placa tenga alimentacion
bool rtcBegin();
uint32_t rtcEpoch();             // segundos unix; 0 si el RTC no es valido
void rtcSetEpoch(uint32_t e);

// PMU AXP2101: estado de la bateria
bool batBegin();
void pmuEnablePanel();           // enciende BLDO1 (OLED VDD 3.3V); llamar antes de gfx->begin()
int batPercent();                 // Waveshare/AXP2101 fuel-gauge 0-100, -1 if unavailable
uint16_t batVoltageMv();          // official AXP2101 battery ADC, mV
bool batCharging();
bool batDischarging();
bool usbPresent();
bool vbusGood();
bool batConnected();
bool pmuReady();
uint16_t vbusVoltageMv();         // official AXP2101 VBUS ADC, mV
uint16_t systemVoltageMv();       // official AXP2101 system-voltage ADC, mV
float pmuTemperatureC();
uint8_t batChargerStatus();
const char *batChargerStatusText();

// boton PWR del AXP2101: pulsacion larga 4s = apagado fisico (RTC sigue vivo);
// la pulsacion corta la captura el firmware (pantalla on/off)
void pwrSetup();
bool pwrShortPressed();  // sondear en el loop
