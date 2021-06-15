# Com-Soc-robotic-arm
Repo for the code for our robotic arm project

Main Com Soc Repo: https://github.com/CRGS-Computing-Society/Com-Soc-main

CRGS Com Soc are working alongside Engineering Soc to create a robotic arm that uses Unsupervised object detection algorithms to detect objects below it and then picks them up. The CAD models and arm code can be found in this repo.

### SEE ISSUES FOR ENGINEERING NOTES

## What the ML team has done

The programme found at [ml team/rotation finder start.ipynb](https://github.com/Joseph-Rance/Com-Soc-robotic-arm/blob/master/ml%20team/Rotation%20Finder%20Final%20%5B%2BDBSCAN%5D.ipynb) first takes in an image like the one below as well as an image of the same scene but without objects on it.

<img src="https://github.com/Joseph-Rance/Com-Soc-robotic-arm/blob/master/ml%20team/classified%20images/3/input%20image.jpg?raw=true" alt="input image" width="200"/>

It then uses unsupervised learning (DBSCAN) to locate the centres of objects in the image by using a processed version of the rounded difference between the input image and the background. Below shows the predicted centres of objects in the image, marked by red dots.

<img src="https://github.com/Joseph-Rance/Com-Soc-robotic-arm/blob/master/ml%20team/classified%20images/3/output.png?raw=true" alt="output image" width="200"/>

*Note: The only inputs are the background image and the image with objects in. No other information is used, including how many objects are in the image*

The algorithm also identifies the best angle to rotate the hand to get hte best grip on the object

## Cad model render

![image](https://user-images.githubusercontent.com/56409230/122041137-8a2c9000-cdd0-11eb-80de-dc97544bcafd.png)

## ML team todo

 - [X] fix the rotation finder code

## Engineering team todo

 - [X] check we have all the components we need in the Tech block
 - [X] Finish x arm
 - [ ] finish servo base connections on model
 - [ ] print
 - [ ] Make wooden base
 - [X] Get bearing

## Servo team todo

 - [X] Make the code interface with the GPIO
 - [ ] Add code for getting images from picam
 - [ ] Add offsets to servo default rotations
 - [ ] DEBUG
