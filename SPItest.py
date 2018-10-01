import SPI as spi
from time import sleep

obj = spi.CarControl()
obj.start()
sleep(1)
while True:
	obj.setSpeed(0.2)
	sleep(1)
	obj.setSpeed(-0.2)
	sleep(1)
	obj.setSpeed(0)
	sleep(1)
	obj.steer(0.3)
	sleep(1)
	obj.steer(-0.3)
	sleep(1)

