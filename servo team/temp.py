import numpy as np
from math import radians, sin, cos
import matplotlib.pyplot as plt
from matplotlib.image import imread
import time

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
    for y in range(new_image.shape[0]):
        for x in range(new_image.shape[1]):
            coords = [[(y+j+radius, x+i+radius) for j in range(-radius, radius+1)] for i in range(-radius, radius+1)]
            total = np.asarray([[image[j] for j in i] for i in coords]).any()
            new_image[y, x] = total != 0
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
    return 2*np.argmin(np.asarray([check_line_length(centres[centre_idx], radians(angle), image) for angle in range(0, 180, 2)]))  # only one returned because we only do one rotation per time

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

parameters = {"scaling": 8,
              "filter_radius": 2,
              "threshold": 30,
              "dbscan_radius": 4,
              "dbscan_core_threshold": 10,
              "dilate_size": 2,
              "centre_idx": 1}

def detect_objs(img1, img2):

    img = np.absolute(img1 - img2)
    img = downsize(img, parameters["scaling"])
    img = median_filter(img, parameters["filter_radius"])
    img = threshold_function(img, parameters["threshold"])
    centres = DBSCAN(img, parameters["dbscan_radius"], parameters["dbscan_core_threshold"])[1]
    centres = move_centres(img, centres)
    img = dilate(img, parameters["dilate_size"])
    angle = get_rotations(img, centres, int(parameters["centre_idx"]))

    return centres, angle, img

img1 = imread('input background.jpg')
if img1.ndim == 3:
    img1 = img1.mean(axis=2)

img2 = imread('input image.jpg')
if img2.ndim == 3:
    img2 = img2.mean(axis=2)

start_time = time.perf_counter()
centres, angle, img = detect_objs(img1, img2)
print(f"Time elapsed: {round(time.perf_counter() - start_time, 2)}s")

print(f"angle below horizontal on the right: {angle}")

parameters["scaling"] = 1

plt.imshow(img, cmap="gray")
plt.plot([centres[parameters["centre_idx"]][1]*parameters["scaling"]-30*cos(radians(angle)),
          centres[parameters["centre_idx"]][1]*parameters["scaling"]+30*cos(radians(angle))],
          [centres[parameters["centre_idx"]][0]*parameters["scaling"]-30*sin(radians(angle)),
          centres[parameters["centre_idx"]][0]*parameters["scaling"]+30*sin(radians(angle))], c="r")
for i in range(len(centres)):
    plt.scatter(centres[i][1]*parameters["scaling"], centres[i][0]*parameters["scaling"], c="g" if i == parameters["centre_idx"] else "r")
plt.show()
