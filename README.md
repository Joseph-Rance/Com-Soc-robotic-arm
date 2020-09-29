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

~~1. add inpainting (using colour spreading from centre method)~~

2. find optimised parameters (using previously made graph)
3. ~~add~~ fix rotation finder (Rounding issue caused try catch to fail so I've fixed that so it needs to be tested again)

## Engineering team todo:

Once I've finished the python notebook, we can start testing values. We need to find values that pass all the tests. Once we have that, we can start modelling in CAD / drawing up designs. I think for the value testing, it might be simpler just to do a grid search of all values for x and y in a given range, rather than just guessing.

I'll try to finish off debuging the workbook soon after exams finish, so hopefully we can aim to finish modelling by October.

## Servo team todo:

Still waiting for dimensions from the engineering team, so there is not much actual work that can be done (other than getting to know python etc.). Once they have the dimensions, though, we can start wrting programs to work out rotations for moving the arm to different points.
