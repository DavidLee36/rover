#include <Arduino.h>
#include <cctype>

void flashLED(int);
bool handleInput();
void toMotors();
void clearMotors();

bool onBoardLEDState = false;
unsigned long lastBlinkTime = 0;

// Motor direction and power: leftFront, leftRear, rightFront, rightRear
bool motorDirections[4]; // true = forward | false = backward
int motorPower[4]; // 0-255
const int PWM_PINS[4] = {33, 36, 28, 29};
const int DIR_PINS[4] = {34, 35, 26, 27};

void setup()
{
	pinMode(LED_BUILTIN, OUTPUT);

	for(int i = 0; i < 4; i++)
	{
		pinMode(PWM_PINS[i], OUTPUT);
		pinMode(DIR_PINS[i], OUTPUT);
		// Push PWM above audible range to kill motor whine.
		// 20 kHz is the MDD10A's rated max PWM frequency.
		analogWriteFrequency(PWM_PINS[i], 20000);
	}

	Serial.begin(115200);
	while (!Serial)
	{
		flashLED(100);
	}
}

void loop()
{
	unsigned long currTime = millis();

	if (!Serial) // No Serial, bail out and flash LED to show error status
	{
		clearMotors();
		flashLED(100);
		return;
	}

	bool receivedInput = handleInput();
	toMotors();

	if (currTime - lastBlinkTime >= 1000) // Blink LED every second to show OK status
	{
		lastBlinkTime = currTime;
		onBoardLEDState = !onBoardLEDState;
		digitalWrite(LED_BUILTIN, onBoardLEDState ? HIGH : LOW);
	}
}

/// @brief Set all motor power to 0
void clearMotors()
{
	for(int i = 0; i < 4; i++)
	{
		motorPower[i] = 0;
		motorDirections[i] = false; // un-important
	}
	toMotors(); // instantly call toMotors() with cleared motor state
}

/// @brief Handles serial input
bool handleInput()
{
	if (!Serial.available())
		return false;

	String data = Serial.readStringUntil('\n');
	int mid = data.indexOf('|');
	String leftData = data.substring(0, mid);
	String rightData = data.substring(mid + 1);
	if (mid < 0 || leftData.length() < 1 || rightData.length() < 1)
	{
		Serial.println("430 Invalid input! (not enough characters)");
		return false;
	}
	char leftDir = std::toupper(leftData.charAt(0));
	char rightDir = std::toupper(rightData.charAt(0));
	int leftPower = leftData.substring(1).toInt() * 255 / 100;
	int rightPower = rightData.substring(1).toInt() * 255 / 100;

	if ((leftDir != 'F' && leftDir != 'R') || (rightDir != 'F' && rightDir != 'R'))
	{
		Serial.print("431 Invalid input! (invalid direction) ");
		Serial.print(leftDir);
		Serial.println(rightDir);
		return false;
	}
	if (leftPower < 0 || leftPower > 255 || rightPower < 0 || rightPower > 255)
	{
		Serial.println("432 Invalid input! (invalid power)");
		return false;
	}

	motorDirections[0] = leftDir == 'F';
	motorDirections[1] = leftDir == 'F';
	motorDirections[2] = rightDir == 'F';
	motorDirections[3] = rightDir == 'F';

	motorPower[0] = leftPower;
	motorPower[1] = leftPower;
	motorPower[2] = rightPower;
	motorPower[3] = rightPower;


	Serial.println("200 Ack");
	return true;
}

void toMotors()
{
	for(int i = 0; i < 4; i++)
	{
		digitalWrite(DIR_PINS[i], motorDirections[i] ? HIGH : LOW);
		analogWrite(PWM_PINS[i], motorPower[i]);
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