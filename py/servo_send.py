import serial
import subprocess
from time import sleep

def acquire_serial():
	# look for /dev/ttyACM* devices
	tty = subprocess.check_output("ls /dev/ttyACM* | head", shell=True, text=True)

	# remove trailing whitespace
	tty = tty.rstrip()

	if tty == '':
		raise Exception("Cannot acquire serial connection!")


	ser = serial.Serial(tty, 9600)
	print(f'Acquiring serial {tty}...')
	sleep(3) # serial takes like 3 seconds to actually connect
	return ser

ser = acquire_serial()

def servo_send(pwm):
	try:
		# Open the serial port
		if not ser.isOpen():
			ser.open()

		# pwm = int(input("Enter PWM Value: "))
		bytes = ("S"+str(pwm)+"\n").encode()
		ser.write(bytes)
		print(f"Sent PWM value: {pwm}")

	except Exception as e:
		print(f"Error: {e}")

def beep_send():
	try:
		# Open the serial port
		if not ser.isOpen():
			ser.open()

		bytes = ("B\n").encode()
		ser.write(bytes)
		print(f"Sent Beep")

	except Exception as e:
		print(f"Error: {e}")
