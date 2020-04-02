#include <Adafruit_NeoPixel.h>

#define LEDPIN		6
#define PSUPIN		12
#define NUMPIXELS	554 // This has to be set accurately on both sides, otherwise updates will be out of sync. Also my setup has 576 LEDs but if this is set to 555 or higher it doesn't write any of them.

#define SERIAL_BAUDRATE	250000

Adafruit_NeoPixel pixels(NUMPIXELS, LEDPIN);


void setup() {
  pixels.begin();
  pixels.setBrightness(50);
  pixels.clear();
  Serial.begin(SERIAL_BAUDRATE);
  pinMode(PSUPIN, OUTPUT);
}

byte readOneByte() {
  int ans = -1;
  while (ans == -1) {
    ans = Serial.read();
  }
  return (byte)ans;
}

/* Accepted commands are:

	"p" and "P": set the PSU pin either low or high.
	"S": show loaded values on the LED strip by submitting them.
	"L": set a value of a pixel. Five bytes follow: the high and low bytes for the index,
	then three for the red, green and blue values.
*/

void loop() {
	handleSerial();
}

void handleSerial(){
	while(Serial.available()>0){
		char command = Serial.read();
		switch(command){
			case 'p': digitalWrite(PSUPIN, LOW);break;
			case 'P': digitalWrite(PSUPIN, HIGH);break;
			case 'L': 
				unsigned int high = Serial.read();
				unsigned int low = Serial.read();
				unsigned int index = high*256 + low;
				unsigned int r,g,b;
				r = Serial.read();
				g = Serial.read();
				b = Serial.read();
				pixels.setPixelColor(index, pixels.Color(r,g,b));
				break;
			case 'S': pixels.show();break;
			case '?': Serial.println(NUMPIXELS);break;
			default: Serial.write(command);
		}
	}
}
