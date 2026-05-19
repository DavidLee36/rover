#include <Arduino.h>

void flashLED(int);
bool handleInput();

bool onBoardLEDState = false;
unsigned long lastBlinkTime = 0;

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

	handleInput();

	if(currTime - lastBlinkTime >= 1000)
	{
		lastBlinkTime = currTime;
		onBoardLEDState = !onBoardLEDState;
		digitalWrite(LED_BUILTIN, onBoardLEDState ? HIGH : LOW);
	}
}

bool handleInput()
{
	if(!Serial.available()) return false;

	String data = Serial.readStringUntil('\n');
	Serial.println(data);
	return true;
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