from adafruit_servokit import ServoKit
from time import sleep

kit = ServoKit(channels=16)
kit.servo[0].actuation_range = 145
kit.servo[1].actuation_range = 145
kit.servo[2].actuation_range = 145
kit.servo[3].actuation_range = 145
kit.servo[4].actuation_range = 145
kit.servo[5].actuation_range = 145
kit.servo[7].actuation_range = 145
kit.servo[8].actuation_range = 145
kit.servo[9].actuation_range = 145
kit.servo[10].actuation_range = 145
kit.servo[11].actuation_range = 145
kit.servo[12].actuation_range = 145

kit.servo[0].angle = 0 
kit.servo[1].angle = 0 
kit.servo[2].angle = 0 
kit.servo[3].angle = 0 
kit.servo[4].angle = 0 
kit.servo[5].angle = 0 
kit.servo[6].angle = 0 
kit.servo[7].angle = 0 
kit.servo[8].angle = 0 
kit.servo[9].angle = 0 
kit.servo[10].angle = 0 
kit.servo[11].angle = 0 
