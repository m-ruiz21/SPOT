#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

#define SERVO_FREQ 50 // Analog servos run at ~50 Hz updates
#define STARTANGLE 350 // PWM value which arduino sets servo to at startup

bool isInteger(String str);
bool parseIntegerFromSerial(int* output);

// called this way, it uses the default address 0x40
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();


void setup() {
  Serial.begin(9600);

  pwm.begin();
  pwm.setOscillatorFrequency(27000000);
  pwm.setPWMFreq(SERVO_FREQ);  // Analog servos run at ~50 Hz updates

  delay(10);
}


int speed = 5; // Speed variable, might be helpful to add a serial command to allow us to change this

int angle = STARTANGLE;
int target = STARTANGLE;

void loop() {
  // Read an integer (with newline) over serial and set the servo's target PWM to it
  // Values should be between 100 and 600
   
  parseIntegerFromSerial(&target);

  // Slowly approach the target PWM instead of setting the PWM directly to it
  angle += ((target - angle) / abs(target - angle)) * speed;
  
  if(abs(angle-target) <= speed) {
    angle = target;
  }
  
  pwm.setPWM(0, 0, angle);
  delay(10);

}

// AI written code below

bool isInteger(String str) {
  if (str.length() == 0) return false; // Empty string is not a valid integer
  for (int i = 0; i < str.length(); i++) {
    if (!isdigit(str.charAt(i)) && str.charAt(i) != '-' && str.charAt(i) != '+') {
      return false; // Non-digit characters found, not a valid integer
    }
  }
  return true; // String represents a valid integer
}

bool parseIntegerFromSerial(int* output) {
  if (Serial.available() > 0) { // Check if serial data is available
    String input = Serial.readStringUntil('\n'); // Read serial input until newline character
    if (isInteger(input)) { // Check if input is a valid integer
      *output = input.toInt(); // Convert input string to integer and store in output
      return true; // Return true for valid input
    } else {
      Serial.println("Invalid input! Please enter an integer."); // Print error message for invalid input
      return false; // Return false for invalid input
    }
  }
  return false; // Return false if no serial data is available
}
