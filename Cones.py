from typing import Tuple, Callable, Iterator
from math import sqrt
from enum import Enum
from functools import reduce
import numpy as np
from sklearn.linear_model import LinearRegression
from scipy.optimize import minimize


class Color(Enum):
    BLUE = 1
    ORANGE = 3
    YELLOW = 2


cone = Tuple[float, float, Color]


def is_blue_cone(x: any) -> bool:
    return isinstance(x, Tuple) and len(x) == 3 and isinstance(x[0], float) \
        and isinstance(x[1], float) and x[2] == Color.BLUE


def is_yellow_cone(x: any) -> bool:
    return isinstance(x, Tuple) and len(x) == 3 and isinstance(x[0], float) \
        and isinstance(x[1], float) and x[2] == Color.YELLOW


def is_orange_cone(x: any) -> bool:
    return isinstance(x, Tuple) and len(x) == 3 and isinstance(x[0], float) \
        and isinstance(x[1], float) and x[2] == Color.ORANGE


yellow_blue_pair = Tuple[cone, cone]


def is_yellow_blue_pair(x: any) -> bool:
    return isinstance(x, Tuple) and len(x) == 2 \
        and is_blue_cone(x[0]) and is_yellow_cone(x[1])


track_path = list[yellow_blue_pair]

start_stop_pair = Tuple[cone, cone]


def is_start_stop_pair(x: any) -> bool:
    return isinstance(x, Tuple) and len(x) == 2 \
        and is_orange_cone(x[0]) and is_orange_cone(x[1])


circle = Tuple[track_path, Tuple[float, float], float, float]


# list of cones, a center, a radius, and the wide between 2 cones


def distance(point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
    dx: float = (point1[0] - point2[0]) ** 2
    dy: float = (point1[1] - point2[1]) ** 2
    return sqrt(dx + dy)


def is_circle(x: any) -> bool:
    return isinstance(x, Tuple) and len(x) == 4 \
        and isinstance(x[0], list) and isinstance(x[1], Tuple) and isinstance(x[2], float) and isinstance(x[3], float) \
        and reduce(lambda acc, c: acc and distance((c[0], c[1]), (x[1][0], x[1][1])) == x[2], x[0], True)


straight = Tuple[track_path, float]


# list of cones and the wide between 2 cones


def is_straight(x: any) -> bool:
    return True


acceleration_track_layout = Tuple[start_stop_pair, straight]

def get_acc_cones(acc: acceleration_track_layout)->track_path:
    return acc[1][0]

def get_blue(pair:yellow_blue_pair)->cone:
    return pair[0]

def get_yellow(pair:yellow_blue_pair)->cone:
    return pair[1]

def get_cone_x(c:cone)->float:
    return c[0]
def get_cone_y(c:cone)->float:
    return c[1]

def is_acceleration_track_layout(x: any) -> bool:
    return True


def cones_generator(start_x: float, finish_x: float, interval: int, f: Callable[[float], float]):
    i = start_x
    while i < finish_x:
        yield f(i)
        i += interval


def append(acc: list[float], cp: yellow_blue_pair) -> list[float]:
    acc.append(cp[0][0])
    return acc


def acceleration_interpolate(at: acceleration_track_layout, interval: int, start_x: float, start_y: float,
                             finish_x: float):
    # blue_x = np.array(reduce(lambda acc, cp: acc.append(cp[0][0]), atl[1], list())).reshape((-1, 1))
    trackpath:track_path = get_acc_cones(at)
    blue_x = np.array(list(map(lambda cp: get_cone_x(get_blue(cp)), trackpath))).reshape((-1, 1))
    blue_y = np.array(list(map(lambda cp: get_cone_y(get_blue(cp)), trackpath)))

    print(blue_x)
    blue_model = LinearRegression()
    blue_model.fit(blue_x, blue_y)
    blue_gen = cones_generator(start_x, finish_x, interval,
                               lambda x: blue_model.coef_ * x + blue_model.intercept_)

    yellow_x = np.array(list(map(lambda cp: get_cone_x(get_yellow(cp)), trackpath))).reshape((-1, 1))
    yellow_y = np.array(list(map(lambda cp: get_cone_y(get_yellow(cp)), trackpath)))

    yellow_model = LinearRegression()
    yellow_model.fit(yellow_x, yellow_y)
    yellow_gen = cones_generator(start_x, finish_x, interval,
                                 lambda x: yellow_model.coef_ * x + yellow_model.intercept_)

    return list(map(lambda cp: (blue_gen.__next__() + yellow_gen.__next__())/2, at[1][0]))



def dist(a:float,c:list(cone)!=None,coefficient:float = 30)->float:
    curve = lambda a,cone: a*get_cone_x(cone)**2 + a*get_cone_y(cone)**2 -coefficient
    cone_dist = lambda cone: np.linalg.norm(curve(a,cone))
    return np.sum(list(map(cone_dist,c)))

def circle_trajectory(cones:track_path = None,coefficient:float = 30):
    if cones is not None:
        blue_cones = list(map(lambda y_b_p:get_blue(y_b_p) ,cones))
        yellow_cones = list(map(lambda y_b_p:get_yellow(y_b_p) ,cones))
        cones = blue_cones+yellow_cones
        return minimize(dist,1.0,args=(cones, coefficient), bound=[(0,None)])
    else:
        raise np.linalg.LinAlgError


cones = [(0, 1,Color.BLUE), (1, 2,Color.YELLOW), (2, 3,Color.BLUE), (3, 4,Color.YELLOW), (4, 5,Color.BLUE)]
res = minimize(dist,1.0,args=(cones,20),bounds=[(0,None)])
print("dist:",res)
print("minimum:",res.fun)

""" # pair: yellow_blue_pair = tuple[tuple[1.4, 1.4, Color.BLUE], tuple[1.3, 0.09, Color.YELLOW]]
=======
# pair: yellow_blue_pair = tuple[tuple[1.4, 1.4, Color.BLUE], tuple[1.3, 0.09, Color.YELLOW]]
pair: yellow_blue_pair = ((1.4, 1.4, Color.BLUE), (1.3, 0.09, Color.YELLOW))

cones: list[yellow_blue_pair] = [((1.4, 1.4, Color.BLUE), (1.3, 0.09, Color.YELLOW)),
                                 ((2.6, 1.0, Color.BLUE), (2, 0.03, Color.YELLOW)),
                                 ((4.3, 2.0, Color.BLUE), (4.65, 0.11, Color.YELLOW)),
                                 ((6.9, 1.01, Color.BLUE), (6.7, 0.4, Color.YELLOW)),
                                 ((8, 1.2, Color.BLUE), (8.001, 0.9, Color.YELLOW)),
                                 ((10, 1, Color.BLUE), (10, 0.7, Color.YELLOW))]

st = (cones, 10.0)
atl: acceleration_track_layout = (((0, 1, Color.ORANGE), (0, 0.05, Color.ORANGE)), st)
cones_b = acceleration_interpolate(atl, 3, 0, 0, 10)
print(cones_b)
for cone in cones_b:
    print(cone) """

