from adafruit_servokit import ServoKit
from time import sleep

kit = ServoKit(channels=16)

for i in range(12):
    kit.servo[i].actuation_range = 145

while True:
    kit.servo[0].angle = 0
    sleep(0.2)
    kit.servo[0].angle = None
    sleep(2)

    kit.servo[0].angle = 10
    sleep(0.2)
    kit.servo[0].angle = None
    sleep(2)
