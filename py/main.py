from time import sleep
from servo_send import servo_send

servo_send(500)
sleep(2)

for i in range(50,525,25):
	servo_send(i)
	sleep(0.25)
sleep(1)
servo_send(50)
