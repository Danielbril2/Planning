from ConeGenerator import Generator,Cone,Type
import numpy as np
import math
import matplotlib.pyplot as plt
from fsd_path_planning import PathPlanner, MissionTypes, ConeTypes
from fsd_path_planning.utils.math_utils import unit_2d_vector_from_angle, rotate


###
# Class to generate cones
# generates a map with cones placed on the left, right, and unknown sides of the car
# cones_left: list of left cones
# cones_right: list of right cones
# cones_unknown: list of unknown cones
###
def buildMap():
    # np.arange(start, stop, step), np.pi / 2 - range of angles from 0 to pi/2
    # np.pi / 15 - angle between cones
	phi_inner = np.arange(0, np.pi / 2, np.pi / 15) # array of angles in radians to represent the positions of the cones on the inner circle
	phi_outer = np.arange(0, np.pi / 2, np.pi / 20) # array of angles in radians to represent the positions of the cones on the outer circle

	# convert the angles to x,y coordinates
	# unit_2d_vector_from_angle is a utility function that returns a unit vector in the direction of the specified angle
	points_inner = unit_2d_vector_from_angle(phi_inner) * 9 # multiply by 9 to get the x,y coordinates of the cones on the inner circle
	points_outer = unit_2d_vector_from_angle(phi_outer) * 12 # multiply by 12 to get the x,y coordinates of the cones on the outer circle

	# center the cones around the origin
	center = np.mean((points_inner[:2] + points_outer[:2]) / 2, axis=0) # get the center of the cones
	points_inner -= center	# subtract the center from the points to center the cones around the origin
	points_outer -= center # subtract the center from the points to center the cones around the origin

	# rotate the cones by -pi/2 radians to align the cones with the x-axis
	# rotate is a utility function that rotates the points by the specified angle
	rotated_points_inner = rotate(points_inner, -np.pi / 2) # rotate the points by -pi/2 radians
	rotated_points_outer = rotate(points_outer, -np.pi / 2) # rotate the points by -pi/2 radians
	cones_left_raw = rotated_points_inner # cones on the left are the cones on the inner circle
	cones_right_raw = rotated_points_outer # cones on the right are the cones on the outer circle

	# shuffle the cones
	rng = np.random.default_rng(0)
	rng.shuffle(cones_left_raw)
	rng.shuffle(cones_right_raw)

	# set the car position and direction
	car_position = np.array([0.0, 0.0])
	car_direction = np.array([1.0, 0.0])

	# get the cones that are on the left and right of the car
	mask_is_left = np.ones(len(cones_left_raw), dtype=bool)
	mask_is_right = np.ones(len(cones_right_raw), dtype=bool)

	# for demonstration purposes, we will only keep the color of the first 4 cones
	# on each side
	# the rest of the cones will be set to unknown
	# filter out cones beyond the fourth cone on each side
	mask_is_left[np.argsort(np.linalg.norm(cones_left_raw, axis=1))[4:]] = False
	mask_is_right[np.argsort(np.linalg.norm(cones_right_raw, axis=1))[4:]] = False

	cones_left = cones_left_raw[mask_is_left]
	cones_right = cones_right_raw[mask_is_right]
	cones_unknown = np.row_stack(
	    [cones_left_raw[~mask_is_left], cones_right_raw[~mask_is_right]]
	)

	return cones_left, cones_right, cones_unknown, car_position, car_direction

###
# converts an angle from degrees to radians and returns a unit vector representing the direction of the angle
# angle: angle in degrees
# returns: unit vector representing the direction of the angle
###
def angle2Vector(angle: float):
	#first convert radians to the second
	angle = math.radians(angle) #later will not needed because value will be at radians
	return np.array([math.cos(angle),math.sin(angle)])


def buildMap2():
	STRAIGHT_RANGE = 9
	C_BLUE_RANGE = range(2,15)
	C_YELLOW_RANGE  = range(5,12)

	g = Generator()

	blue_half_circle_line = lambda x: math.sqrt(36 - math.pow(x - 8, 2)) + 9 # (x - 8)^2 + (y - 9)^2 = 36
	yellow_half_circle_line = lambda x: math.sqrt(9 - math.pow(x - 8, 2)) + 9 # (x - 8)^2 + (y - 9)^2 = 9

	g.addBlue(np.full(STRAIGHT_RANGE,2),range(STRAIGHT_RANGE))
	g.addBlue(C_BLUE_RANGE,[blue_half_circle_line(x) for x in C_BLUE_RANGE])
	g.addBlue(np.full(STRAIGHT_RANGE,14),range(STRAIGHT_RANGE))

	g.addYellow(np.full(STRAIGHT_RANGE,5),range(STRAIGHT_RANGE))
	g.addYellow(C_YELLOW_RANGE,[yellow_half_circle_line(x) for x in C_YELLOW_RANGE])
	g.addYellow(np.full(STRAIGHT_RANGE,11),range(STRAIGHT_RANGE))

	car_position = np.array([3.5, 0.0])
	car_direction = np.pi /4
	car_direction_vector = angle2Vector(car_direction)
	cones_left = g.addNoiseToSide(g.getBluePoints(),sd = 0.1)
	cones_right = g.addNoiseToSide(g.getYellowPoints(),sd = 0.1)

	return np.array(cones_left), np.array(cones_right), np.zeros((0, 2)), car_position, car_direction,car_direction_vector

def plot_path(path, car_position, car_direction):
    plt.scatter(cones_left[:, 0], cones_left[:, 1], c=blue_color, label="left")
    plt.scatter(cones_right[:, 0], cones_right[:, 1], c=yellow_color, label="right")
    plt.scatter(cones_unknown[:, 0], cones_unknown[:, 1], c="k", label="unknown")
    plt.legend()
    car_direction_vector = angle2vector(car_direction)
    plt.plot(
        [car_position[0], car_position[0] + car_direction_vector[0]],
        [car_position[1], car_position[1] + car_direction_vector[1]],
        c="k",
    )
    plt.title("Computed path")
    plt.plot(*path[:(int(len(path)/2)), 1:3].T)
    plt.axis("equal")
    plt.show()

cones_left, cones_right, cones_unknown, car_position, car_direction, car_direction_vector = buildMap2()

blue_color = "#7CB9E8"
yellow_color = "gold"
# plot the cones
plt.scatter(cones_left[:, 0], cones_left[:, 1], c=blue_color, label="left") #plot the blue cones
plt.scatter(cones_right[:, 0], cones_right[:, 1], c=yellow_color, label="right") #plot the yellow cones
plt.scatter(cones_unknown[:, 0], cones_unknown[:, 1], c="k", label="unknown")
plt.legend() #show the legend
plt.plot( #plot the car
    [car_position[0], car_position[0] + car_direction_vector[0]],
    [car_position[1], car_position[1] + car_direction_vector[1]],
    c="k",
)

planner = PathPlanner(MissionTypes.acceleration) #create a path planner

for i, c in enumerate(ConeTypes):
    print(c, f"= {i}")

for i, c in enumerate(MissionTypes):
	print(c)

cones_by_type = [np.zeros((0, 2)) for _ in range(5)]
cones_by_type[ConeTypes.LEFT] = cones_left
cones_by_type[ConeTypes.RIGHT] = cones_right
cones_by_type[ConeTypes.UNKNOWN] = cones_unknown

for _ in range(5):
	out = planner.calculate_path_in_global_frame(
	    cones_by_type, car_position, car_direction, return_intermediate_results=True
	)

	(
	    path,
	    sorted_left,
	    sorted_right,
	    left_cones_with_virtual,
	    right_cones_with_virtual,
	    left_to_right_match,
	    right_to_left_match,
	) = out

	plt.scatter(cones_left[:, 0], cones_left[:, 1], c=blue_color, label="left")
	plt.scatter(cones_right[:, 0], cones_right[:, 1], c=yellow_color, label="right")
	plt.scatter(cones_unknown[:, 0], cones_unknown[:, 1], c="k", label="unknown")

	plt.legend()
	car_direction_vector = angle2Vector(car_direction)
	plt.plot(
	    [car_position[0], car_position[0] + car_direction_vector[0]],
	    [car_position[1], car_position[1] + car_direction_vector[1]],
	    c="k",
	)


	plt.title("Computed path")
	plt.plot(*path[:(int(len(path)/2)), 1:3].T)
	print(path[:, 1:3])
	print(car_direction)

	#print(path)

	plt.axis("equal")

	plt.show()
	
	new_point = path[:, 1:3][10]

	new_direction = np.array([new_point[0] - car_position[0], new_point[1] - car_position[1]])

	magnitude = np.linalg.norm(new_direction)

# Normalize the vector to have a magnitude of 1
	unit_vector = new_direction / magnitude

	car_direction = np.arctan2(new_direction[1], new_direction[0])
	
	car_position = new_point

