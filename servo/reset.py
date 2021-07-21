from adafruit_servokit import ServoKit
from time import sleep

kit = ServoKit(channels=16)
for i in range(12):
    kit.servo[i].actuation_range = 145
    kit.servo[i].angle = 0