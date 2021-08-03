import time
from math import atan, atan2, pi, asin, acos, cos, sin, radians, degrees
from adafruit_servokit import ServoKit

def get_rotations(x_coord, y_coord, z_coord, w, c, x=40, y=35, a=7, open_ang=radians(0), close_ang=radians(25)):

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

def move_servos(route, servos, speed=1):

    route = [[degrees(i) for i in j] for j in route]
    
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
        
        servos[0].angle = o
        servos[1].angle = 90 - w
        servos[2].angle = 180 - gamma
        servos[3].angle = beta
        servos[4].angle = 145 - beta

        servos[5].angle = servos[6].angle = 145 - alpha - 3  # 145 is max rotation
        servos[7].angle = 145 - alpha
        servos[8].angle = servos[10].angle = alpha + 5
        servos[9].angle = alpha + 12

        servos[11].angle = theta * -0.75 + 22

        #time.sleep(0.5)
        #for i in range(12):  # turn off servos when not moving to avoid jitter
        #    servos[i].angle = None
        time.sleep(0.3)  # ensure servos have finished moving before next move

def main():

    kit = ServoKit(channels=16)
    servos = kit.servo
    
    for i in range(16):
        servos[i].actuation_range = 145

    route = [
        [0, 45, 10, 0, 0],
        [10, 34, 20, 0, 0],
        [0, 45, 10, pi/2, 1],
        [0, 45, 10, 0, 0]
    ]

    route = [[0, 35, 30, 0, 0]]

    for coords in route:
        rotations = get_rotations(*coords)
        print([degrees(i) for i in rotations])
        move_servos([rotations], servos)
        time.sleep(1)

    for i in range(12):
        servos[i].angle = None

    print("Done.")

if __name__ == "__main__":
    main()

