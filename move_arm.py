import time
from math import atan, atan2, pi, asin, acos, cos, sin, radians
from adafruit_servokit import ServoKit

def move_servos(route, servos, speed=1):
    
    '''
    servos:
    0 -> gripper
    1 -> gripper sideways rotate
    2 -> gripper up/down rotate
    3, 4 -> y arm up/down
    5,6,7,8,9,10 -> x arm up/down
    11 -> horiz. rotate
    '''
    for (theta, alpha, beta, gamma, w, o) in route:
        
        '''
        theta:    angle at the base for horizontal rotation (clockwise from the vertical)
        alpha:    angle at the base for vertical roation
        beta:     angle at the elbow for vertical
        gamma:    angle at the wrist for vertical
        w:        wrist rotation
        o:        rotation for finger
        '''
        
        servos[0] = o
        servos[1] = w
        servos[2] = gamma
        servos[3] = servos[4] = beta
        for i in range(5, 11):
            servos[i] = alpha
        servos[11] = theta

def get_rotations(self, x_coord, y_coord, z_coord, w, c, x=40, y=35, a=7, open_ang=radians(10), close_ang=radians(30)):

    '''
    theta:    angle at the base for horizontal rotation (clockwise from the vertical)
    alpha:    angle at the base for vertical roation
    beta:     angle at the elbow for vertical
    gamma:    angle at the wrist for vertical
    w:        wrist rotation
    r:        radius    
    z_coord:  height of hand
    c:        open(0)/closed(1)
    o:        rotation for finger
    a:        length of wrist
    x_coord:  x coord
    y_coord:  y coord
    x:        x arm length 
    y:        y arm length
    '''

    if c:
        o = close_ang
    else:
        o = open_ang

    r = (x_coord**2 + y_coord**2)**0.5
    theta = pi/2 - atan2(y_coord, x_coord)

    b = r**2 + (a+z_coord)**2
    alpha = pi - asin((x**2 - y**2 + b)/(2*x*(b**0.5))) - atan((r)/(a+z_coord))
    beta = acos((x*cos(alpha)-(r))/y) - alpha

    gamma = 3*pi/2 - alpha - beta

    return theta, alpha, beta, gamma, w, o


kit = ServoKit(channels=16)
servos = kit.servo

for servo in servos:
    servo.actuation_range = 135

while True:

    coords = tuple(int(i) for i in input("(x, y, z, w, c) = "))  # w = wrist rotation, c = open(0)/closed(1)
    assert len(coords) == 5
    route = [get_rotations(*coords)]
    move_servos(route, servos)