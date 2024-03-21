import serial
import time

# Define the serial port and baud rate
ser = serial.Serial('COM3', 9600)  # Change 'COM3' to match your Arduino's serial port and set the correct baud rate

def blink_x_times(times):
    try:
        # Open the serial port
        if not ser.isOpen():
            ser.open()

        # Wait for a brief moment to ensure the port is open
        time.sleep(2)

        # Send an integer through serial communication
        number_to_send = int(times)  # Replace with the integer you want to send
        ser.write(str(number_to_send).encode())
        print(f"Sent integer: {number_to_send}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the serial port
        ser.close()

while(1):
    x = input("Input a number: ")
    if x == "Exit":
        break
    else:
        blink_x_times(x)