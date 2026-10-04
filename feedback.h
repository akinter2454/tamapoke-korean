#pragma once
#include <Arduino.h>

// Optional haptic hook. The Waveshare ESP32-S3-Touch-AMOLED-1.75-B does not
// expose an onboard vibration motor, so the stock build compiles this to a
// zero-cost no-op. Builders who add a small externally-driven motor may define
// TAMAPOKE_HAPTIC_PIN to a safe GPIO in their own hardware fork.
void feedbackBegin();
void feedbackUpdate();
void feedbackPulse(uint16_t ms);
bool feedbackHapticAvailable();
