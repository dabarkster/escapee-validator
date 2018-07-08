#include <Firmata.h>

byte previousPIN[TOTAL_PORTS];  // PIN means PORT for input
byte previousPORT[TOTAL_PORTS];

#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif

#define PIN 6
int val = 0;
bool flash = false;
Adafruit_NeoPixel strip = Adafruit_NeoPixel(4, PIN, NEO_GRB + NEO_KHZ800);

void outputPort(byte portNumber, byte portValue)
{
  // only send the data when it changes, otherwise you get too many messages!
  if (previousPIN[portNumber] != portValue) {
    Firmata.sendDigitalPort(portNumber, portValue);
    previousPIN[portNumber] = portValue;
  }
}

void setPinModeCallback(byte pin, int mode) {
  if (IS_PIN_DIGITAL(pin)) {
    pinMode(PIN_TO_DIGITAL(pin), mode);
  }
}

void digitalWriteCallback(byte port, int value)
{
  byte i;
  byte currentPinValue, previousPinValue;

  if (port < TOTAL_PORTS && value != previousPORT[port]) {
    for (i = 0; i < 8; i++) {
      currentPinValue = (byte) value & (1 << i);
      previousPinValue = previousPORT[port] & (1 << i);
      if (currentPinValue != previousPinValue) {
        digitalWrite(i + (port * 8), currentPinValue);
      }
    }
    previousPORT[port] = value;
  }
}

void colorpulse(uint32_t c, uint8_t wait)
{
  while(flash == true)
  {
    for(uint16_t i=0; i<strip.numPixels(); i++) 
      {
        strip.setPixelColor(i, c);
      }
      strip.show();
      delay(wait);
      for(uint16_t i=0; i<strip.numPixels(); i++) 
      {
        strip.setPixelColor(i, 0, 0, 0);
      }
      strip.show();
      delay(wait);
      val = digitalRead(5);
      if(val == 1)
      { 
        flash = true;
      }
      else
      {
        flash = false;
      }
      while (Firmata.available())
        Firmata.processInput();
  }
}

void setup()
{
  Firmata.setFirmwareVersion(FIRMATA_FIRMWARE_MAJOR_VERSION, FIRMATA_FIRMWARE_MINOR_VERSION);
  Firmata.attach(DIGITAL_MESSAGE, digitalWriteCallback);
  Firmata.attach(SET_PIN_MODE, setPinModeCallback);
  Firmata.begin(57600);

  pinMode(5, INPUT); 
  strip.begin();
  strip.show(); 
}

void loop()
{
  byte i;

  for (i = 0; i < TOTAL_PORTS; i++) {
    outputPort(i, readPort(i, 0xff));
  }

  val = digitalRead(5);
  if(val == 1)
  {
    flash = true;
    colorpulse(strip.Color(0, 0, 255), 50);
  }

  while (Firmata.available()) {
    Firmata.processInput();
  }
}
