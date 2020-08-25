# Com-Soc-robotic-arm
Repo for the code for our robotic arm project

Main Repo: https://github.com/Joseph-Rance/Computing-Soc

## ML team todo:

~~1. add inpainting (using colour spreading from centre method)~~

2. find optimised parameters (using previously made graph)
3. add rotaition finder (via assigning vlaues to lines through centre as functions of either length or something to do with tagnents)

Also, pratyaksh pointed out:
*Could we just use the outlier points (i.e. points reachable from core points that are not themselves core points) for [finding the outline of the object]?*

Because the clusters are very dense, and points are evenly spaced, I think this would potentially work quite well, so long as we get the parameters right. Then we could just find the shortest line that passes through the centre and touches two core points on each end (and constrain the centre to be on the object, to avoid doughnuts messing us up)

Hopefully we'll be able to try this out in next week's session.

## Engineering team todo:

Once I've finished the python notebook, we can start testing values. We need to find values that pass all the tests. Once we have that, we can start modelling in CAD / drawing up designs. I think for the value testing, it might be simpler just to do a grid search of all values for x and y in a given range, rather than just guessing

## Servo team todo:

Stilll waiting for dimensions from the engineering team, so there is not much actual work that can be done (other than getting to know python etc.). Once they have the dimensions, though, we can start wrting programs to work out rotations for moving the arm to different points.
