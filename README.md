# Com-Soc-robotic-arm
Repo for the code for our robotic arm project

Main Com Soc Repo: https://github.com/Joseph-Rance/Computing-Soc

CRGS Com Soc are working alongside Engineering Soc to create a robotic arm that uses Unsupervised object detection algorithms to detect objects below it and then picks them up. This repo holds the majority for the object detection code as well as some code for the engineering team.

### SEE ISSUES FOR INFO

## What the ML team has done

The programme found at [ml team/rotation finder start.ipynb](https://github.com/Joseph-Rance/Com-Soc-robotic-arm/blob/master/ml%20team/rotation%20finder%20start.ipynb) first takes in an image like the one below as well as an image of the same scene but without objects on it.

<img src="https://github.com/Joseph-Rance/Com-Soc-robotic-arm/blob/master/ml%20team/classified%20images/3/input%20image.jpg?raw=true" alt="input image" width="200"/>

It then uses unsupervised learning (DBSCAN) to locate the centres of objects in the image by using a processed version of the rounded difference between the input image and the background. Below shows the predicted centres of objects in the image, marked by red dots.

<img src="https://github.com/Joseph-Rance/Com-Soc-robotic-arm/blob/master/ml%20team/classified%20images/3/output.png?raw=true" alt="output image" width="200"/>

*Note: The only inputs are the background image and the image with objects in. No other information is used, including how many objects are in the image*

We are currently working on a rotation finder to work out which rotation the grabber should be in to get the best grip on the objects, although there are still a few bugs with this function.

## ML team todo:

DONE!

## Engineering team todo:

 - [ ] Finish x arm
 - [ ] Add servo connections
 - [ ] print
 - [ ] Make wooden supports
 - [ ] Get bearing

## Servo team todo:

 - [ ] Make the code interface with the GPIO
