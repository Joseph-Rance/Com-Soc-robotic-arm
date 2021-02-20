import numpy as np
from sys import argv
import time
from math import atan, pi, asin, acos, cos, sin, radians
import matplotlib.pyplot as plt
from matplotlib.image import imread

def median_filter(input_image, s):
    new_image = np.zeros((input_image.shape[0], input_image.shape[1]))
    for r in range(0, input_image.shape[1]):
        for c in range(0, input_image.shape[0]):
            values = []
            for ri in range(max(0, r - s), min(input_image.shape[1], r + s)):
                for ci in range(max(0, c - s), min(input_image.shape[0], c + s)):
                    values.append(input_image[ci, ri])
            values = sorted(values)
            new_image[c, r] = values[int(len(values) / 2)]

    return new_image


downsize = lambda img, sf: np.array(
    [[img[j, i] for i in range(0, len(img[0]), sf)] for j in range(0, len(img), sf)])
threshold_function = lambda image, threshold: np.asarray(
    [[pixel >= threshold for pixel in row] for row in image])


def dilate(image, radius):
    new_image = np.zeros(image.shape)
    image = np.pad(image, radius)
    for y in range(2, image.shape[0]-2):
        for x in range(2, image.shape[1]-2):
            coords = [[(y+j, x+i) for j in range(-radius, radius+1)]
                        for i in range(-radius, radius+1)]
            total = np.asarray([[image[j] for j in i] for i in coords]).any()
            new_image[y-radius*2, x-radius*2] = total != 0
    return new_image


def DBSCAN(image, radius, core_threshold):

    points = []

    for y in range(len(image)):
        for x in range(len(image[y])):
            if image[y, x] == 1:
                points.append([(y, x), 0])

    groups = [0]  # group 0 -> noise (default)

    for point in points:

        surrounding_points = []
        for other_point in points:
            if ((point[0][0] - other_point[0][0])**2 + (point[0][1] - other_point[0][1])**2)**0.5 <= radius and point != other_point:
                surrounding_points.append(other_point)

        if len(surrounding_points) >= core_threshold:

            if sum([p[1] for p in surrounding_points]) == 0:  # no groups
                new_group = groups[-1] + 1
                groups.append(new_group)

                for p in surrounding_points:
                    p[1] = new_group  # changes main points list as list is reference

            elif sum([p[1] > 0 for p in surrounding_points]) == 1:  # one group

                group = -1  # group should never stay -1
                for p in surrounding_points:
                    group = p[1] if p[1] > 0 else group

                for p in surrounding_points:
                    p[1] = group

            else:  # >1 group

                surrounding_groups = []
                for p in surrounding_points:
                    if p[1] not in surrounding_groups and p[1] != 0:
                        surrounding_groups.append(p[1])

                for p in surrounding_points:
                    p[1] = surrounding_groups[0]

                for p in points:
                    if p[1] in surrounding_groups:
                        p[1] = surrounding_groups[0]

    del groups[0]  # noise group
    centres = [[0, 0] for i in groups]
    totals = [0 for i in groups]

    for point in points:
        if point[1] != 0:
            centres[groups.index(point[1])][0] += point[0][0]
            centres[groups.index(point[1])][1] += point[0][1]
            totals[groups.index(point[1])] += 1

    for i in range(len(groups)):
        if totals[i] > 0:
            centres[i][0] /= totals[i]
            centres[i][1] /= totals[i]

    loss = 0
    for point in points:
        distances = np.array([((point[0][0] - centre[0])**2 + (point[0][1] - centre[1])**2)**0.5 for centre in centres])
        loss += min(distances)

    del_list = []
    for i in range(len(centres)):
        if centres[i] == [0, 0]:
            del_list.append(i)
    for i in sorted(del_list)[::-1]: del centres[i]

    return points, centres, loss

def get_rotations(image, centres, centre_idx=0, debug=False):

    def check_line_length(centre, angle, image):  # angle is from line to right

        def dist(p1, p2):
            return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5

        hyp = 0
        still_on_obj_pos = still_on_obj_neg = True
        coords = [(), ()]

        while still_on_obj_pos or still_on_obj_neg:
            hyp += 2
            dy = hyp * sin(angle)  # keep angle in radians
            dx = hyp * cos(angle)
            try:
                if image[round(centre[0]+dy), round(centre[1]+dx)] == 0 and still_on_obj_pos:
                    still_on_obj_pos = False
                    coords[0] = (round(centre[0]+dy), round(centre[1]+dx))
            except IndexError:
                if still_on_obj_pos:
                    still_on_obj_pos = False
                coords[0] = (round(centre[0]+dy), round(centre[1]+dx))

            try:
                if image[round(centre[0]-dy), round(centre[1]-dx)] == 0 and still_on_obj_neg:
                    still_on_obj_neg = False
                    coords[1] = (round(centre[0]-dy), round(centre[1]-dx))
            except IndexError:
                if still_on_obj_neg:
                    still_on_obj_neg = False
                    coords[1] = (round(centre[0]-dy), round(centre[1]-dx))

        return dist(*coords)

    if debug:
        return [check_line_length(centres[centre_idx], radians(angle), image) for angle in range(0, 180, 2)]
    return np.argmin(np.asarray([check_line_length(centres[centre_idx], radians(angle), image) for angle in range(0, 180, 2)]))  # only one returned because we only do one rotation per time

def move_centres(image, centres):

    new_centres = [(1e5, 1e5) for i in centres]

    def dist(p1, p2):
        return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5

    points = []

    for y in range(len(image)):
        for x in range(len(image[y])):
            if image[y,x] == 1:
                points.append((y,x))

    for point in points:
        for i, centre in enumerate(centres):
            distance = dist(point, centre)
            if distance < new_centres[i][1]:
                new_centres[i] = (point, distance)

    return [i[0] for i in new_centres]

class servo_control(object):

    offsets, scalings = (0, 0), (1, 1)  # (x,y)

    def __init__(self, drop_pos):
        if input("Calibrate arm? (y/n) ") == "y":
            self.calibrate()
        self.drop_pos = drop_pos

    def calibrate(self):

        def get_calibration_image():  # placeholder function
            return np.zeros((100, 100))

        image = get_calibration_image()

        a, b, c, d = input("what are the real positions in m of the dots in the image? (in format: 'x, y, x, y') ").split(", ")
        real1, real2 = (float(a), float(b)), (float(c), float(d))

        exit = False
        while not exit:
            a, b, c, d = input("What are the positions in pixels of the dots in the image? (in format: 'x, y, x, y') ").split(", ")
            image1, image2 = (float(a), float(b)), (float(c), float(d))

            plt.imshow(image)
            plt.scatter([int(a), int(c)], [int(b), int(d)])
            plt.show()

            exit = input("Would you like to change these values? (y/n) ") != "y"

        plt.imshow(image)
        plt.scatter([int(a), int(c)], [int(b), int(d)])
        plt.show()
    
        try:
            scalingx = (real1[0] - real2[0]) / (image1[0] - image2[0])
            scalingy = (real1[1] - real2[1]) / (image1[1] - image2[1])
        except:
            raise ValueError("division by zero due to points being aligned in x or y. Try again with different image x,y values")
        mean_scaling = (scalingx + scalingy) / 2
        scalings = (mean_scaling, mean_scaling)

        offsetx_1 = real1[0] - (image1[0] * scalings[0])
        offsetx_2 = real2[0] - (image2[0] * scalings[0])
        mean_offsetx = (offsetx_1 + offsetx_2) / 2

        offsety_1 = real1[1] - (image1[1] * scalings[1])
        offsety_2 = real2[1] - (image2[1] * scalings[1])
        mean_offsety = (offsety_1 + offsety_2) / 2

        offsets = (mean_offsetx, mean_offsety)
    
        self.scalings, self.offsets = scalings, offsets

        return offsets, scalings

    def get_rotations(self, x_coord, y_coord, z_coord, w, c, x=40, y=35, a=0.07, image_height=1, open_ang=10, close_ang=30):  # g is grabber servo rotation

        '''
        theta:    angle at the base for horizontal rotation
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

        y = image_height - y
        r = (x**2 + y**2)**0.5
        theta = atan(y_coord/x_coord)

        b = (r/100)**2 + (a+z_coord)**2
        alpha = pi - asin((x**2 - y**2 + b)/(2*x*(b**0.5))) - atan((r/100)/(a+z_coord))
        beta = acos((x*cos(alpha)-(r/100))/y) - alpha

        gamma = 3*pi/2 - alpha - beta

        return (theta, alpha, beta, gamma, w, o)

    def get_route(self, w, x, y, z=0.04, x_len=40, y_len=40, a_len=0.07, img_h=1, open_ang=10, close_ang=30):  # x,y in pixels

        if z < 0.01:
            raise ValueError("DONT HIT THE TABLE")

        x = self.offsets[0] + self.scalings[0]*x
        y = self.offsets[1] + self.scalings[1]*y

        h = 0.05  # height above object

        actions = []
        args = (x_len, y_len, a_len, img_h, open_ang, close_ang)

        actions.append(self.get_rotations(x, y, z+h, w, 0, *args))  # go above object
        actions.append(self.get_rotations(x, y, z, w, 0, *args))  # go down to object
        actions.append(self.get_rotations(x, y, z, w, 1, *args))  # grab object
        actions.append(self.get_rotations(x, y, z+h, w, 1, *args))  # go up from table
        actions.append(self.get_rotations(self.drop_pos[0], self.drop_pos[1], z+h, 0, 1, *args))  # go to drop position
        actions.append(self.get_rotations(self.drop_pos[0], self.drop_pos[1], z+h, 0, 0, *args))  # drop object

        return actions

def move_and_check_servos(route):  # TODO
    pass

if __name__ == "__main__":

    args = argv[1:]  # python main.py scaling=0.1

    parameters = {"scaling": 8,  # TODO
                  "filter_radius": 2,
                  "threshold": 40,
                  "dbscan_radius": 5,
                  "dbscan_core_threshold": 3,
                  "dilate_size": 2,
                  "centre_idx": 2,
                  "photo_location_x": 40,
                  "photo_location_y": 0,
                  "photo_location_z": 20,
                  "pickup_height": 0.04,
                  "image_height": 1,
                  "x_arm_length": 40,
                  "y_arm_length": 35,
                  "a_arm_length": 0.07,
                  "alpha_min": radians(5),
                  "alpha_max": radians(80),
                  "beta_max": radians(130),
                  "beta_min": 0,
                  "drop_location_x": 0,
                  "drop_location_y": 0,
                  "drop_location_z": 20,
                  "grabber_open_angle": 10,
                  "grabber_close_angle": 30}

    exit = False
    try:
        if args[0] == "help":
            print(f"default params: {parameters}")
            exit = True
    except:
        pass

    if exit:
        quit()

    for arg in args:
        arg = arg.split("=")
        assert len(arg) == 2

        if arg[0] not in parameters:
            raise ValueError(f"{arg[0]} is not an accepted parameter!")

        parameters[arg[0]] = float(arg[1])

    controller = servo_control((parameters["drop_location_x"], parameters["drop_location_y"], parameters["drop_location_z"]))

    time.sleep(5)

    no_objects = 1
    centre_idx = 0

    while no_objects != 0:

        print("taking images")

        rotations = controller.get_rotations(parameters["photo_location_x"],
                                             parameters["photo_location_y"],
                                             parameters["photo_location_z"],
                                             0, 0,
                                             parameters["x_arm_length"],
                                             parameters["y_arm_length"],
                                             parameters["a_arm_length"],
                                             parameters["image_height"],
                                             parameters["grabber_open_angle"],
                                             parameters["grabber_close_angle"])
        move_and_check_servos([rotations])

        img1 = np.zeros((100, 100)) # take images
        img2 = np.zeros((100, 100))

        print("searching for objects")

        img = np.absolute(img1 - img2)
        img = downsize(img, parameters["scaling"])
        img = median_filter(img, parameters["filter_radius"])
        img = threshold_function(img, parameters["threshold"])
        img = dilate(img, parameters["dilate_size"])
        centres = DBSCAN(img, parameters["dbscan_radius"], parameters["dbscan_core_threshold"])[1]
        centres = move_centres(img, centres)

        no_objects = len(centres)
        if no_objects == 0:
            break

        print("getting rotation for first object")

        angle = get_rotations(img, centres, int(parameters["centre_idx"]))

        print("getting rotations for arm")

        route = controller.get_route(angle,
                                     centres[int(parameters["centre_idx"])][0],
                                     centres[int(parameters["centre_idx"])][1],
                                     parameters["pickup_height"],
                                     parameters["x_arm_length"],
                                     parameters["y_arm_length"],
                                     parameters["a_arm_length"],
                                     parameters["image_height"],
                                     parameters["grabber_open_angle"],
                                     parameters["grabber_close_angle"])

        print("picking up object")

        move_and_check_servos(route)

    print("Done.")