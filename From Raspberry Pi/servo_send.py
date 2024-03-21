import serial
import subprocess

def acquire_serial():
	# look for /dev/ttyACM* devices
	tty = subprocess.check_output("ls /dev/ttyACM* | head", shell=True, text=True)

	# remove trailing whitespace
	tty = tty.rstrip()

	if tty == '':
		raise Exception("Cannot acquire serial connection!")


	return serial.Serial(tty, 9600)

ser = acquire_serial()

def servo_send(pwm):
	try:
		# Open the serial port
		if not ser.isOpen():
			ser.open()

		# pwm = int(input("Enter PWM Value: "))
		bytes = (str(pwm)+"\n").encode()
		ser.write(bytes)
		print(f"Sent PWM value: {pwm}")

	except Exception as e:
		print(f"Error: {e}")

#	finally:
#		ser.close()
