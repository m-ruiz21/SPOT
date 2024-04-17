#include <Wire.h>
#include <Servo.h>

Servo myservo;  // create servo object to control a servo

// #include <Adafruit_PWMServoDriver.h>

#define SERVO_FREQ 50 // Analog servos run at ~50 Hz updates

bool isInteger(String str);
bool parseIntegerFromSerial(int* output);

// called this way, it uses the default address 0x40
// Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();


void setup() {
  Serial.begin(9600);
  Serial.setTimeout(100);

  // pwm.begin();
  // pwm.setOscillatorFrequency(27000000);
  // pwm.setPWMFreq(SERVO_FREQ);  // Analog servos run at ~50 Hz updates
    // pinMode(A5, OUTPUT);  // sets the pin as output
      myservo.attach(A5);  // attaches the servo on pin 9 to the servo object



  delay(10);
  

}


int speed = 10; // Speed variable, might be helpful to add a serial command to allow us to change this

int angle = -1; // Initial value
int target = -1;

void loop() {
  // Read an integer (with newline) over serial and set the servo's target PWM to it
  // Values should be between 100 and 500
  if(parseIntegerFromSerial(&target)) {
  }

  // Don't do anything until we've received a command
  if(target == -1) { return; }
  if(angle == -1) { angle = target; } // initialize angle

  // Slowly approach the target PWM instead of setting the PWM directly to it
  angle += ((target - angle) / abs(target - angle)) * speed;
  
  if(abs(angle-target) <= speed) {
    angle = target;
  }
  
  // Serial.print("Setting angle to ");
  Serial.println(angle);
  // pwm.setPWM(0, 0, angle);
  // (right) = 10
  // (center) = 90
  // (left) = 170
  int actualAngle = map(angle, -45, 45, 170, 10);
  
  myservo.write(actualAngle);

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
    char commandType = input.charAt(0);
    input = input.substring(1);
    switch(commandType) {
      case 'S':
        if (isInteger(input)) { // Check if input is a valid integer
          *output = input.toInt(); // Convert input string to integer and store in output
          return true; // Return true for valid input
        } else {
          Serial.println("Invalid input! Please enter an integer."); // Print error message for invalid input
          return false; // Return false for invalid input
        }
        break;
      case 'B':
        tone(11, 500, 100);
        break;
    }
  }
  return false; // Return false if no serial data is available
}
