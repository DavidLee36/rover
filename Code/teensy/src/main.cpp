#include <Arduino.h>

void flashLED(int);

bool onBoardLEDState = false;

void setup()
{
	pinMode(LED_BUILTIN, OUTPUT);

	Serial.begin(115200);
	while (!Serial) {
		flashLED(100);
	}
}

void loop()
{
	unsigned long currTime = millis();

	if(!Serial) // No Serial, bail out
	{
		flashLED(100);
		return;
	}

	if(currTime % 1000 == 0)
	{
		if(onBoardLEDState) digitalWrite(LED_BUILTIN, LOW);
		else digitalWrite(LED_BUILTIN, HIGH);
		onBoardLEDState = !onBoardLEDState;
	}
}

void flashLED(int d)
{
	digitalWrite(LED_BUILTIN, HIGH);
	onBoardLEDState = true;
	delay(d);
	digitalWrite(LED_BUILTIN, LOW);
	onBoardLEDState = false;
	delay(d);
}