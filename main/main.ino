/*
 * Send accelerometer data over serial,
 * receive which finger to vibrate from serial
 * and activate corresponding motor for a given time.
 */

#include <Wire.h>
#include <SPI.h>
#include <Adafruit_LIS3DH.h>
#include <Adafruit_Sensor.h>

// Pin map

// Vibration motors
// L or R indicates hand; 1 is thumb, 5 is pinky
#define L1_pin A1
#define L2_pin A2
#define L3_pin A3
#define L4_pin A4
#define L5_pin A5
#define R1_pin 3
#define R2_pin 4
#define R3_pin 5
#define R4_pin 9
#define R5_pin 8
 
// Accelerometer (sw SPI)
#define lis_CLK 13
#define lis_MISO 12
#define lis_MOSI 11
#define lis_CS 10

// Configuration
#define DELAY_FLICKER 80    // time (ms) to vibrate for
#define DELAY_READ 50       // time (ms) between readings

// [finger, multiplier * 10]
int fingers[][3] = {{L5_pin, 13, 0}, 
                    {L4_pin, 15, 1}, 
                    {L3_pin, 10, 2}, 
                    {L2_pin, 10, 3}, 
                    {L1_pin, 14, 4},
                    {R5_pin, 13, 5}, 
                    {R4_pin, 15, 6}, 
                    {R3_pin, 15, 7}, 
                    {R2_pin, 15, 8}, 
                    {R1_pin, 14, 9}};

Adafruit_LIS3DH lis = Adafruit_LIS3DH(lis_CS, lis_MOSI, lis_MISO, lis_CLK);

void send_accel();  // send accelerometer data to serial
int *read_finger();  // read which finger to vibrate from serial
void flicker(int f[]);  // vibrate motor for DELAY_FLICKER time (ms)

void setup() {
  Serial.begin(9600);
  while (!Serial) delay(10);  // wait for Serial to start
  
  if (!lis.begin(0x18)) {
    Serial.println("Couldn't start accelerometer!");
    while (1) yield();
  }
  Serial.println("accelerometer found!");

  lis.setRange(LIS3DH_RANGE_4_G);  // 2, 4, 8 or 16
  
  // configure pins
  pinMode(L1_pin, OUTPUT);
  pinMode(L2_pin, OUTPUT);
  pinMode(L3_pin, OUTPUT);
  pinMode(L4_pin, OUTPUT);
  pinMode(L5_pin, OUTPUT);
  pinMode(R1_pin, OUTPUT);
  pinMode(R2_pin, OUTPUT);
  pinMode(R3_pin, OUTPUT);
  pinMode(R4_pin, OUTPUT);
  pinMode(R5_pin, OUTPUT);

  digitalWrite(L1_pin, LOW);
  digitalWrite(L2_pin, LOW);
  digitalWrite(L3_pin, LOW);
  digitalWrite(L4_pin, LOW);
  digitalWrite(L5_pin, LOW);
  digitalWrite(R1_pin, LOW);
  digitalWrite(R2_pin, LOW);
  digitalWrite(R3_pin, LOW);
  digitalWrite(R4_pin, LOW);
  digitalWrite(R5_pin, LOW);

  Serial.println("<Arduino is ready>");  // main.py is waiting for this signal
}


void loop() {
  send_accel();  // send accelerometer data
  int* target_pin = read_finger();  // pin, multiplier for motor to vibrate
  if (target_pin != NULL) {
    flicker(target_pin);
  }
  delay(DELAY_READ);
}


/* Send accelerometer data via USB Serial
 * Designed to work with save_console.py
 * <x:_,y:_,z:_>\n
 */
void send_accel() {  
  sensors_event_t event;
  lis.getEvent(&event);

  Serial.print("<timestamp:"); Serial.print(millis()); Serial.print(",");
  // in m/s^2
  Serial.print("x:"); Serial.print(event.acceleration.x); Serial.print(",");
  Serial.print("y:"); Serial.print(event.acceleration.y); Serial.print(",");
  Serial.print("z:"); Serial.print(event.acceleration.z); Serial.println(">");

  Serial.println();
}


/* Read finger to vibrate from USB Serial (from a python script)
 * Return [motor_pin, multiplier] for that finger
 */
int *read_finger() {
  if (Serial.available() > 0) {
    int finger = Serial.read() - 48; // convert to int from ASCII
    Serial.print("<read "); Serial.print(finger); Serial.println(">");  // debugging
    
    for (int i=0; i < 10; i++) {
      if (fingers[i][2] == finger):
        return fingers[i];
    }
  }
  return NULL;
}


// Vibrate motor at given pin for DELAY_READ * (multiplier/10)
void flicker(int f[]) {
  digitalWrite(f[0], HIGH);  // vibration on
  delay(DELAY_FLICKER * (float(f[1]) / 10));
  digitalWrite(f[0], LOW);  // vibration off  
}


// Echo received comms
void test_connection() {
  int in = 0;
  while (true) {
    if (Serial.available() > 0) {
      in = Serial.read();
      Serial.print("<Received: "); Serial.print(in, DEC); Serial.println(">");
    }
  }
}
