import serial
import time

ser = serial.Serial('COM3', 9600)  # Change 'COM3' to match your Arduino's serial port

try:
    # Open the serial port
    if not ser.isOpen():
        ser.open()
        
    time.sleep(2)

    num_times = int(input("Enter the number of times to move the servo: "))
    ser.write(str(num_times).encode())
    print(f"Sent number of times: {num_times}")

except Exception as e:
    print(f"Error: {e}")

finally:
    ser.close()
