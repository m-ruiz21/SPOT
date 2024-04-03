import RPi.GPIO as GPIO
import time

# Define the GPIO pins
TRIG_PIN = 6
ECHO_PIN = 5
BUZZER_PIN = 2

# Set up the GPIO channels - one input, one output
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# Initialize PWM on the buzzer pin with a frequency of 1kHz
buzzer = GPIO.PWM(BUZZER_PIN, 1000)

def measure_distance():
    # Clear the TRIG_PIN by setting it LOW
    GPIO.output(TRIG_PIN, False)
    time.sleep(0.000002)

    # Set the TRIG_PIN high for 10 microseconds then set it to LOW
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    # Record the start and end times of the pulse
    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    # Calculate distance
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    
    return distance

try:
    while True:
        distance = measure_distance()
        print("Distance:", distance, "cm")

        # Check distance and set the buzzer frequency
        if distance < 10:
            buzzer.start(50) # 50% duty cycle
            time.sleep(0.1)
            buzzer.stop()
            time.sleep(0.1)
        elif distance < 20:
            buzzer.start(50)
            time.sleep(0.1)
            buzzer.stop()
            time.sleep(0.2)
        elif distance < 30:
            buzzer.start(50)
            time.sleep(0.1)
            buzzer.stop()
            time.sleep(0.3)
        else:
            buzzer.stop()
            time.sleep(0.5)

except KeyboardInterrupt:
    GPIO.cleanup()
