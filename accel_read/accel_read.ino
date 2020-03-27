/*
 *  Read accelerometer data during testing.
 *  Run with save_console.py to save serial output to a timestamped log file.
 */

#include <Wire.h>
#include <SPI.h>
#include <Adafruit_LIS3DH.h>
#include <Adafruit_Sensor.h>

// Setup software SPI for the accelerometer
#define lis_CLK 13
#define lis_MISO 12
#define lis_MOSI 11
#define lis_CS 10

Adafruit_LIS3DH lis = Adafruit_LIS3DH(lis_CS, lis_MOSI, lis_MISO, lis_CLK); 

void setup() {
  Serial.begin(9600);
  while (!Serial) delay(10);  // wait for Serial to start

  if (!lis.begin(0x18)) {
    Serial.println("Couldn't start lis!");
    while (1) yield();
  }
  Serial.println("lis found!");

  lis.setRange(LIS3DH_RANGE_2_G);  // 2, 4, 8 or 16
  Serial.println("<Arduino is ready>");
}

void loop() {
  sensors_event_t event;
  lis.getEvent(&event);

  // in m/s^2
  Serial.print("<x:"); Serial.print(event.acceleration.x); Serial.print(",");
  Serial.print("y:"); Serial.print(event.acceleration.y); Serial.print(",");
  Serial.print("z:"); Serial.print(event.acceleration.z); Serial.println(">");

  Serial.println();

  delay(200);
}
