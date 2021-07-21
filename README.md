# Com-Soc-robotic-arm
Repo for the code for our robotic arm project

Main Com Soc Repo: https://github.com/CRGS-Computing-Society/Com-Soc-main

## Object detection

The program first takes in an image like the one below as well as an image of the same scene but without objects on it.

<img src="https://github.com/Joseph-Rance/Com-Soc-robotic-arm/blob/master/ml%20team/classified%20images/3/input%20image.jpg?raw=true" alt="input image" width="200"/>

It then takes the difference between the two images to get a map of where the added objects may be, cleans the map up, and then finds the centre of the objects using DBSCAN. Below shows the predicted centres of objects in the image, marked by red dots.

<img src="https://github.com/Joseph-Rance/Com-Soc-robotic-arm/blob/master/ml%20team/classified%20images/3/output.png?raw=true" alt="output image" width="200"/>

*Note: The only inputs are the background image and the image with objects in. No other information is used, including how many objects are in the image*

The algorithm also identifies the best angle to rotate the hand to get the best grip on the object

## Cad model render

![image](https://user-images.githubusercontent.com/56409230/123335270-20348900-d53c-11eb-8eee-9fbc30d04f5f.png)

# TODO

- [ ] finish TODOs in combined/main

- [ ] fix issues with servo power supply (add new cables?)
- [ ] test code with each set of servos + update code to reduce jitter and allow for gearing
- [ ] add servos in at the correct orientation
- [ ] test arm