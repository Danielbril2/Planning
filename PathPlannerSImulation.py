import numpy as np
import math
import matplotlib.pyplot as plt
from ConeGenerator import Generator as ConeGenerator, Type
from fsd_path_planning import PathPlanner, MissionTypes, ConeTypes
from fsd_path_planning.utils.math_utils import rotate


class ConeMapBuilder:
    def __init__(self):
        self.generator = ConeGenerator()
        self.car_position = np.array([3.5, 0.0])
        self.car_direction_vector = self.angle_to_vector(90)
        self.car_direction = np.pi / 4
        self.cones_left = np.empty((0, 2))
        self.cones_right = np.empty((0, 2))
        self.cones_unknown = np.empty((0, 2))

    def build_map(self, equation):
        x_range = range(2, 14)
        y_range = [equation(x) for x in x_range]

        self.generator.addBlue(np.full(len(x_range), 2), x_range)
        self.generator.addBlue(np.full(len(x_range), 14), x_range)
        self.generator.addYellow(np.full(len(x_range), 5), x_range)
        self.generator.addYellow(np.full(len(x_range), 11), x_range)

        self.cones_left = self.generator.addNoiseToSide(self.generator.getBluePoints(), sd=0.1)
        self.cones_right = self.generator.addNoiseToSide(self.generator.getYellowPoints(), sd=0.1)

    def angle_to_vector(self, angle):
        angle_rad = math.radians(angle)
        return np.array([math.cos(angle_rad), math.sin(angle_rad)])


class PathPlannerWrapper:
    def __init__(self):
        self.planner = PathPlanner(MissionTypes.acceleration)

    def calculate_path(self, cones_left, cones_right, car_position, car_direction):
        cones_by_type = [np.zeros((0, 2)) for _ in range(5)]
        cones_by_type[ConeTypes.LEFT] = np.array(cones_left)
        cones_by_type[ConeTypes.RIGHT] = np.array(cones_right)
        cones_by_type[ConeTypes.UNKNOWN] = np.empty((0, 2))

        out = self.planner.calculate_path_in_global_frame(
            cones_by_type, car_position, car_direction, return_intermediate_results=True
        )

        return out


def plot_map(cones_left, cones_right, cones_unknown, car_position, car_direction,car_direction_vector, blue_color, yellow_color):
    cones_left = np.array(cones_left)
    cones_right = np.array(cones_right)
    cones_unknown = np.array(cones_unknown)

    plt.scatter(cones_left[:, 0], cones_left[:, 1], c=blue_color, label="left")
    plt.scatter(cones_right[:, 0], cones_right[:, 1], c=yellow_color, label="right")
    plt.scatter(cones_unknown[:, 0], cones_unknown[:, 1], c="k", label="unknown")

    plt.legend()
    plt.plot(
        [car_position[0], car_position[0] + car_direction_vector[0]],
        [car_position[1], car_position[1] + car_direction_vector[1]],
        c="k",
    )

    plt.title("Computed path")
    plt.axis("equal")
    plt.show()



def plot_path(path, car_position, car_direction):
    plt.plot(*path[:(int(len(path)/2)), 1:3].T)
    plt.axis("equal")
    plt.title("Computed Path")
    plt.show()

def plot_map_and_path(cones_left, cones_right, cones_unknown, car_position, car_direction,car_direction_vector, path, blue_color, yellow_color):
    cones_left = np.array(cones_left)
    cones_right = np.array(cones_right)
    cones_unknown = np.array(cones_unknown)

    plt.scatter(cones_left[:, 0], cones_left[:, 1], c=blue_color, label="left")
    plt.scatter(cones_right[:, 0], cones_right[:, 1], c=yellow_color, label="right")
    plt.scatter(cones_unknown[:, 0], cones_unknown[:, 1], c="k", label="unknown")

    plt.legend()
    plt.plot(
        [car_position[0], car_position[0] + car_direction_vector[0]],
        [car_position[1], car_position[1] + car_direction_vector[1]],
        c="k",
    )

    plt.title("Computed path")
    plt.plot(path[:, 0], path[:, 1], c="r", label="path")
    plt.axis("equal")
    plt.show()

def simulate_car_movement(map_builder, planner_wrapper):
    for _ in range(3):
        out = planner_wrapper.calculate_path(
            map_builder.cones_left,
            map_builder.cones_right,
            map_builder.car_position,
            map_builder.car_direction,
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

        plot_map(
            map_builder.cones_left,
            map_builder.cones_right,
            map_builder.cones_unknown,
            map_builder.car_position,
            map_builder.car_direction,
            map_builder.angle_to_vector(map_builder.car_direction),
            path,
            "#7CB9E8",
            "gold"
        )

        plot_path(path, map_builder.car_position, map_builder.car_direction)

        new_point = path[:, 1:3][10]
        new_direction = np.array([new_point[0] - map_builder.car_position[0], new_point[1] - map_builder.car_position[1]])
        magnitude = math.sqrt(np.sum(new_direction ** 2))
        unit_vector = new_direction / magnitude

        map_builder.car_direction = math.atan2(unit_vector[1], unit_vector[0])
        map_builder.car_position = new_point


# Example map equation: y = x^2
def map_equation(x):
    return x ** 2


map_builder = ConeMapBuilder()
map_builder.build_map(map_equation)

planner_wrapper = PathPlannerWrapper()
simulate_car_movement(map_builder, planner_wrapper)
