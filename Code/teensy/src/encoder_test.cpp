// Encoder bring-up test sketch (standalone — does NOT touch motor firmware).
//
// Purpose: confirm all 4 GoBilda quadrature encoders are wired correctly before
// adding closed-loop PID to main.cpp.
//
// Build/upload only this file with the dedicated PlatformIO env:
//     pio run -e enctest -t upload
//     pio device monitor -e enctest
//
// WIRING (Teensy 4.1 — 3.3V GPIO, NOT 5V tolerant):
//   Power every encoder from the Teensy 3.3V pin (NOT VIN/5V), share GND.
//   A/B channel pairs:  LF = 2/3   LR = 4/5   RF = 6/7   RR = 8/9
//   These don't overlap the motor pins (PWM 33,36,28,29 / DIR 34,35,26,27).
//
// HOW TO READ THE OUTPUT (spin each wheel by hand):
//   - Count should climb steadily when the wheel turns "forward", fall in reverse.
//   - Wrong direction (counts fall on forward)  -> swap that encoder's A/B pins.
//   - Random jumps / counts with no motion       -> bad pin, loose lead, or 5V/GND issue.
//   - Dead channel (always 0 while spinning)      -> A or B not connected.
//   Turn one wheel at a time so you can attribute the moving column.

#include <Arduino.h>
#include <Encoder.h>

// Order matches main.cpp motor arrays: leftFront, leftRear, rightFront, rightRear.
const char *LABELS[4] = {"LF", "LR", "RF", "RR"};

Encoder encoders[4] = {
	Encoder(2, 3),
	Encoder(4, 5),
	Encoder(6, 7),
	Encoder(8, 9),
};

long lastCounts[4] = {0, 0, 0, 0};
unsigned long lastPrint = 0;
const unsigned long PRINT_INTERVAL_MS = 200;

void setup()
{
	pinMode(LED_BUILTIN, OUTPUT);
	digitalWrite(LED_BUILTIN, HIGH); // solid LED = encoder test running

	Serial.begin(115200);
	while (!Serial)
		; // wait for USB serial (Teensy returns immediately once host opens port)

	Serial.println("Encoder bring-up test. Spin each wheel by hand.");
	Serial.println("Columns: <label>=<count>(<delta since last print>)");
	Serial.println("Forward should climb, reverse should fall. One wheel at a time.");
}

void loop()
{
	unsigned long now = millis();
	if (now - lastPrint < PRINT_INTERVAL_MS)
		return;
	lastPrint = now;

	String line = "";
	for (int i = 0; i < 4; i++)
	{
		long count = encoders[i].read();
		long delta = count - lastCounts[i];
		lastCounts[i] = count;

		line += LABELS[i];
		line += "=";
		line += count;
		line += "(";
		if (delta >= 0)
			line += "+";
		line += delta;
		line += ")";
		if (i < 3)
			line += "  ";
	}
	Serial.println(line);
}
