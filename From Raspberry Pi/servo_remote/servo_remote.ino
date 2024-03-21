/*************************************************** 
  This is an example for our Adafruit 16-channel PWM & Servo driver
  Servo test - this will drive 8 servos, one after the other on the
  first 8 pins of the PCA9685

  Pick one up today in the adafruit shop!
  ------> http://www.adafruit.com/products/815
  
  These drivers use I2C to communicate, 2 pins are required to  
  interface.

  Adafruit invests time and resources providing this open source code, 
  please support Adafruit and open-source hardware by purchasing 
  products from Adafruit!

  Written by Limor Fried/Ladyada for Adafruit Industries.  
  BSD license, all text above must be included in any redistribution
 ****************************************************/

#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

// called this way, it uses the default address 0x40
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

#define SERVOMIN  150 // This is the 'minimum' pulse length count (out of 4096)
#define SERVOMAX  600 // This is the 'maximum' pulse length count (out of 4096)
#define USMIN  600 // This is the rounded 'minimum' microsecond length based on the minimum pulse of 150
#define USMAX  2400 // This is the rounded 'maximum' microsecond length based on the maximum pulse of 600
#define SERVO_FREQ 50 // Analog servos run at ~50 Hz updates

// our servo # counter
uint8_t servonum = 0;

void setup() {
  Serial.begin(9600);

  pwm.begin();
  pwm.setOscillatorFrequency(27000000);
  pwm.setPWMFreq(SERVO_FREQ);  // Analog servos run at ~50 Hz updates

  delay(10);
}


#define MAX_LINE_LENGTH 64
int parseIntFromSerial() {
  char buffer[MAX_LINE_LENGTH];
  int index = 0;
  
  // Read until newline character or buffer full
  while (index < MAX_LINE_LENGTH - 1) {
    if (Serial.available()) {
      char c = Serial.read();
      if (c == '\n') {
        break; // Stop reading if newline is encountered
      }
      buffer[index++] = c;
    }
  }
  buffer[index] = '\0'; // Null-terminate the string
  
  // Parse the string as an integer
  int parsedInt = atoi(buffer);
  
  return parsedInt;
}

#define STARTANGLE 350

int speed = 5; // Speed variable, might be helpful to add a serial command to allow us to change this

int angle = STARTANGLE;
int target = STARTANGLE;


void loop() {
  // Read an integer (with newline) over serial and set the servo's PWM to it
  // Values should be between 100 and 600
  
  if(Serial.available() > 0) {
    target = parseIntFromSerial();
    
    
//    Serial.print("new angle = ");
//    Serial.println(target);
      

  }
  angle += ((target - angle) / abs(target - angle)) * speed;
  
  if(abs(angle-target) <= speed) {
    angle = target;
  }
  
  pwm.setPWM(servonum, 0, angle);
  delay(10);100
  
//  Serial.print("angle = ");
//  Serial.println(angle);


}
