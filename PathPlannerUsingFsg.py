from ConeGenerator import Generator,Cone,Type
import numpy as np
import math
import matplotlib.pyplot as plt
from fsd_path_planning import PathPlanner, MissionTypes, ConeTypes
from fsd_path_planning.utils.math_utils import unit_2d_vector_from_angle, rotate

def buildMap():
	phi_inner = np.arange(0, np.pi / 2, np.pi / 15) #right cones
	phi_outer = np.arange(0, np.pi / 2, np.pi / 20) #left cones

	points_inner = unit_2d_vector_from_angle(phi_inner) * 9
	points_outer = unit_2d_vector_from_angle(phi_outer) * 12

	center = np.mean((points_inner[:2] + points_outer[:2]) / 2, axis=0)
	points_inner -= center
	points_outer -= center

	rotated_points_inner = rotate(points_inner, -np.pi / 2)
	rotated_points_outer = rotate(points_outer, -np.pi / 2)
	cones_left_raw = rotated_points_inner
	cones_right_raw = rotated_points_outer


	rng = np.random.default_rng(0)
	rng.shuffle(cones_left_raw)
	rng.shuffle(cones_right_raw)


	car_position = np.array([0.0, 0.0])
	car_direction = np.array([1.0, 0.0])

	mask_is_left = np.ones(len(cones_left_raw), dtype=bool)
	mask_is_right = np.ones(len(cones_right_raw), dtype=bool)

	# for demonstration purposes, we will only keep the color of the first 4 cones
	# on each side
	mask_is_left[np.argsort(np.linalg.norm(cones_left_raw, axis=1))[4:]] = False
	mask_is_right[np.argsort(np.linalg.norm(cones_right_raw, axis=1))[4:]] = False

	cones_left = cones_left_raw[mask_is_left]
	cones_right = cones_right_raw[mask_is_right]
	cones_unknown = np.row_stack(
	    [cones_left_raw[~mask_is_left], cones_right_raw[~mask_is_right]]
	)

	return cones_left, cones_right, cones_unknown, car_position, car_direction


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
	car_direction = np.array([0.0, 1.0])
	car_direction = angle2Vector(90)

	cones_left = g.addNoiseToSide(g.getBluePoints(),sd = 0.1)
	cones_right = g.addNoiseToSide(g.getYellowPoints(),sd = 0.1)

	return np.array(cones_left), np.array(cones_right), np.zeros((0, 2)), car_position, car_direction



cones_left, cones_right, cones_unknown, car_position, car_direction = buildMap2()

blue_color = "#7CB9E8"
yellow_color = "gold"

plt.scatter(cones_left[:, 0], cones_left[:, 1], c=blue_color, label="left")
plt.scatter(cones_right[:, 0], cones_right[:, 1], c=yellow_color, label="right")
plt.scatter(cones_unknown[:, 0], cones_unknown[:, 1], c="k", label="unknown")
plt.legend()
plt.plot(
    [car_position[0], car_position[0] + car_direction[0]],
    [car_position[1], car_position[1] + car_direction[1]],
    c="k",
)

planner = PathPlanner(MissionTypes.acceleration)

for i, c in enumerate(ConeTypes):
    print(c, f"= {i}")

for i, c in enumerate(MissionTypes):
	print(c)

cones_by_type = [np.zeros((0, 2)) for _ in range(5)]
cones_by_type[ConeTypes.LEFT] = cones_left
cones_by_type[ConeTypes.RIGHT] = cones_right
cones_by_type[ConeTypes.UNKNOWN] = cones_unknown

for _ in range(1):
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

	plt.plot(
	    [car_position[0], car_position[0] + car_direction[0]],
	    [car_position[1], car_position[1] + car_direction[1]],
	    c="k",
	)


	plt.title("Computed path")
	plt.plot(*path[:(int(len(path)/2)), 1:3].T)
	print(path[:, 1:3])

	#print(path)

	plt.axis("equal")

	plt.show()
	
	new_point = path[:, 1:3][10]

	new_direction = np.array([new_point[0] - car_position[0], new_point[1] - car_position[1]])

	magnitude = math.sqrt(sum(component**2 for component in new_direction))

# Normalize the vector to have a magnitude of 1
	unit_vector = tuple(component/magnitude for component in new_direction)

	car_direction = unit_vector
	
	car_position = new_point

