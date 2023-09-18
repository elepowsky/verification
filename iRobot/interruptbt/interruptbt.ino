#include "BluetoothSerial.h"

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif

BluetoothSerial SerialBT;

// neopixel
#include <Adafruit_NeoPixel.h>
#define NUMPIXELS 1
Adafruit_NeoPixel pixels(NUMPIXELS, PIN_NEOPIXEL, NEO_GRB + NEO_KHZ800);

// define pin numbers for geiger counters
const int det1 = 13;
const int det2 = 12;
const int det3 = 27;

// define integration time (milliseconds)
const float inttime = 1000;

// initialize counters, one per detector
volatile long counts1 = 0;
volatile long counts2 = 0;
volatile long counts3 = 0;

// initialize timer
long starttime;

// setup
void setup() {
	// start serial connection
	Serial.begin(115200);
	SerialBT.begin("FeatherV2");
	// initialize NeoPixel strip object
	pixels.begin();
	pixels.setBrightness(20);
	// attach interrupts to each detector [digitalPinToInterrupt]
	attachInterrupt(digitalPinToInterrupt(det1), event1, RISING);
	attachInterrupt(digitalPinToInterrupt(det2), event2, RISING);
	attachInterrupt(digitalPinToInterrupt(det3), event3, RISING);
	// start timer
	starttime = millis();
}

// interrupt 1
IRAM_ATTR void event1() {
	// increment counter 1
	counts1++;
}

// interrupt 2
IRAM_ATTR void event2() {
	// increment counter 2
	counts2++;
}

// interrupt 3
IRAM_ATTR void event3() {
	// increment counter 3
	counts3++;
}

// main loop
void loop() {
	// check timer against integration time
	if (( millis () - starttime ) >= inttime) {
		// print counts to serial monitor
		Serial.print(counts1);
		Serial.print(",");
		Serial.print(counts2);
		Serial.print(",");
		Serial.println(counts3);
		SerialBT.print(counts1);
		SerialBT.print(",");
		SerialBT.print(counts2);
		SerialBT.print(",");
		SerialBT.println(counts3);
		if ((counts1 > counts2) && (counts1 > counts3)) {
			pixels.fill(0xff0000);
			pixels.show();
		}
		if ((counts2 > counts1) && (counts2 > counts3)) {
			pixels.fill(0x00ff00);
			pixels.show();
		}
		if ((counts3 > counts1) && (counts3 > counts2)) {
			pixels.fill(0x0000ff);
			pixels.show();
		}
		// reset counters
		counts1 = 0;
		counts2 = 0;
		counts3 = 0;
		// reset timer
		starttime = millis();
	}
}