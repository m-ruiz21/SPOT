import serial
import time

ser = serial.Serial('/dev/ttyACM1', 9600)  # Change 'COM3' to match your Arduino's serial port
# Open the serial port


while True:
	try:
		if not ser.isOpen():
			ser.open()

		num_times = int(input("Enter PWM Value: "))
		bytes = (str(num_times)+"\n").encode()
		print('bytes:', bytes);
		ser.write(bytes)
		print(f"Sent PWM value: {num_times}")

		# ser.read()

	except Exception as e:
		print(f"Error: {e}")

#	finally:
#		ser.close()