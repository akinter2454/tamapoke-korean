#include "feedback.h"

#ifndef TAMAPOKE_HAPTIC_PIN
#define TAMAPOKE_HAPTIC_PIN (-1)
#endif

#if TAMAPOKE_HAPTIC_PIN >= 0
static uint32_t gHapticUntil = 0;
#endif

void feedbackBegin() {
#if TAMAPOKE_HAPTIC_PIN >= 0
  pinMode(TAMAPOKE_HAPTIC_PIN, OUTPUT);
  digitalWrite(TAMAPOKE_HAPTIC_PIN, LOW);
#endif
}

void feedbackPulse(uint16_t ms) {
#if TAMAPOKE_HAPTIC_PIN >= 0
  if (!ms) return;
  digitalWrite(TAMAPOKE_HAPTIC_PIN, HIGH);
  gHapticUntil = millis() + ms;
#else
  (void)ms;
#endif
}

void feedbackUpdate() {
#if TAMAPOKE_HAPTIC_PIN >= 0
  if (gHapticUntil && (int32_t)(millis() - gHapticUntil) >= 0) {
    digitalWrite(TAMAPOKE_HAPTIC_PIN, LOW);
    gHapticUntil = 0;
  }
#endif
}

bool feedbackHapticAvailable() {
#if TAMAPOKE_HAPTIC_PIN >= 0
  return true;
#else
  return false;
#endif
}
