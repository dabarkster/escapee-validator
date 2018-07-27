#include "Arduino.h"
#include "SoftwareSerial.h"

 
int ledPin = 8;    // LEDs (via MOSFET) connected to pin 9
 
void setup()
{
 
  pinMode(ledPin, OUTPUT);
 
  Serial.begin(115200);
  Serial.println(F("Initializing DFPlayer..."));

}
 
void loop()
{
  int flashCount = random (3, 15);        // Min. and max. number of flashes each loop
  int flashBrightnessMin =  10;           // LED flash min. brightness (0-255)
  int flashBrightnessMax =  255;          // LED flash max. brightness (0-255)
 
  int flashDurationMin = 1;               // Min. duration of each seperate flash
  int flashDurationMax = 50;              // Max. duration of each seperate flash
 
  int nextFlashDelayMin = 1;              // Min, delay between each flash and the next
  int nextFlashDelayMax = 150;            // Max, delay between each flash and the next
 
  int loopDelay = random (500, 1000);   // Min. and max. delay between each loop
 
  Serial.println();
  Serial.print(F("Flashing, count: "));
  Serial.println( flashCount );
 
  for (int flash = 0 ; flash <= flashCount; flash += 1) { // Flashing LED strip in a loop, random count
 
    analogWrite(ledPin, random (flashBrightnessMin, flashBrightnessMax)); // Turn LED strip on, random brightness
    delay(random(flashDurationMin, flashDurationMax)); // Keep it tured on, random duration
 
    analogWrite(ledPin, 0); // Turn the LED strip off
    delay(random(nextFlashDelayMin, nextFlashDelayMax)); // Random delay before next flash
  }
 
  Serial.print(F("Pausing before playing thunder sound, milliseconds: "));
  Serial.print(F("Pausing before next loop, milliseconds: "));
  Serial.println(loopDelay);
  delay(loopDelay);
 
}
