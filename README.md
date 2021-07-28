# Com-Soc-robotic-arm
Repo for the code for our robotic arm project

Main Com Soc Repo: https://github.com/CRGS-Computing-Society/Com-Soc-main

## Object detection

The program first takes in an image like the one below as well as an image of the same scene but without objects on it.

<img src="https://github.com/Joseph-Rance/Com-Soc-robotic-arm/blob/master/object%20detection/classified%20images/3/input%20image.jpg" alt="input image" width="200"/>

It then takes the difference between the two images to get a map of where the added objects may be, cleans the map up, and then finds the centre of the objects using DBSCAN. Below shows the predicted centres of objects in the image, marked by red dots.

<img src="https://github.com/Joseph-Rance/Com-Soc-robotic-arm/blob/master/object%20detection/classified%20images/3/output.png" alt="output image" width="200"/>

*Note: The only inputs are the background image and the image with objects in. No other information is used, including how many objects are in the image*

The algorithm also identifies the best angle to rotate the hand to get the best grip on the object

## Cad model render

![arm render](https://github.com/Joseph-Rance/Com-Soc-robotic-arm/blob/master/render.jpg)

# TODO

- [ ] finish TODOs in [combined/main.py](https://github.com/Joseph-Rance/Com-Soc-robotic-arm/blob/master/combined/main.py)
- [x] fix issues with servo power supply (add new cables?)
- [X] test code with each set of servos ~~+ update code to reduce jitter and allow for gearing~~
- [X] add servos in at the correct orientation
- [ ] test arm as whole + fix any problems (inc. fixing horizontal rotate servo, up/down gripper, and checking main.py is up to date with move_arm.py)

# servo offsets

```
0 -> 0 to 25
1 -> 90 (inv)
2 -> 0
3 -> 0
4 -> 0 (inv)
5 -> -3
6 -> -3
7 -> 0
8 -> 5 (inv)
9 -> 12 (inv)
10 -> 5 (inv)
11 -> 22 (inv, gear)
```
