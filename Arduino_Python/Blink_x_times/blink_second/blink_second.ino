const int ledPin = 13;  // LED connected to digital pin 13
int blinkCount = 0;     // Variable to store the number of times to blink the LED

void setup() {
  pinMode(ledPin, OUTPUT);  // Initialize the LED pin as an output
  Serial.begin(9600);       // Start serial communication at 9600 baud rate
}

void loop() {
  // Check if data is available on the serial port
  if (Serial.available() > 0) {
    // Read the incoming number from the serial port
    blinkCount = Serial.parseInt();

    // Blink the LED the specified number of times
    for (int i = 0; i < blinkCount; i++) {
      digitalWrite(ledPin, HIGH);  // Turn on the LED
      delay(500);                   // Wait for 500 milliseconds
      digitalWrite(ledPin, LOW);   // Turn off the LED
      delay(500);                   // Wait for 500 milliseconds
    }

    // Reset blinkCount to 0
    blinkCount = 0;
  }
}