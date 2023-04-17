from ConeGenerator import Generator,Cone,Type
import numpy as np
import math
from typing import Tuple
import time

g = Generator()

def createMap():
	STRAIGHT_RANGE = 9
	C_BLUE_RANGE = range(2,15)
	C_YELLOW_RANGE  = range(5,12)

	blue_half_circle_line = lambda x: math.sqrt(36 - math.pow(x - 8, 2)) + 8 # (x - 8)^2 + (y - 8)^2 = 36
	yellow_half_circle_line = lambda x: math.sqrt(9 - math.pow(x - 8, 2)) + 8 # (x - 8)^2 + (y - 8)^2 = 9

	g.addBlue(np.full(STRAIGHT_RANGE,2),range(STRAIGHT_RANGE))
	g.addBlue(C_BLUE_RANGE,[blue_half_circle_line(x) for x in C_BLUE_RANGE])
	g.addBlue(np.full(STRAIGHT_RANGE,14),range(STRAIGHT_RANGE))

	g.addYellow(np.full(STRAIGHT_RANGE,5),range(STRAIGHT_RANGE))
	g.addYellow(C_YELLOW_RANGE,[yellow_half_circle_line(x) for x in C_YELLOW_RANGE])
	g.addYellow(np.full(STRAIGHT_RANGE,11),range(STRAIGHT_RANGE))


def findLine(cor1: (float,float),cor2: (float,float)) -> (float,float):
	#cor1,cor2: (x,y)
	m: float = (cor2[1] - cor1[1])/(cor2[0] - cor1[0])
	b: float = cor1[1] - m * cor1[0]
	return (m,b)

def findPoint(line1: (float,float),line2: (float,float)) -> (float,float):
	#line1,line2: (m,b)
	x: float = (line2[1] - line1[1])/(line1[0] - line2[0])
	y: float = line1[0] * x + line1[1]
	return (x,y)


def calculatePath(cones: list[Cone]) -> list[(float,float)]:
	blueCones: list[Cone] = [c for c in cones if c.type == Type.BLUE]
	yellowCones: list[Cone] = [c for c in cones if c.type == Type.YELLOW]

	path = []
	for i in range(len(yellowCones)): #in the shorter list
		try:
			blue1 = (blueCones[i].x,blueCones[i].y)
			blue2 = (blueCones[i+1].x,blueCones[i+1].y)
			yellow1 = (yellowCones[i].x,yellowCones[i].y)
			yellow2 = (yellowCones[i+1].x,yellowCones[i+1].y)

			line1 = findLine(blue1,yellow2)
			line2 = findLine(yellow1,blue2)

			intercept = findPoint(line1,line2)
			path.append(intercept)

		except:
			pass

	return path


def filterPath(cones,path):
	return None

def main():
	t = time.time()
	createMap()
	cones = g.generateData()
	NoiseCones = Generator.addNoise(cones, sd = 0.2)
	
	halfPath = calculatePath(NoiseCones)
	NoiseCones.reverse()

	secondHalfPath = calculatePath(NoiseCones)
	secondHalfPath.reverse()

	path = halfPath[:int(len(halfPath)/2)] + secondHalfPath[int(len(secondHalfPath)/2):]
	print(time.time()-t)

	#Generator.showGraph(NoiseCones,path)


if __name__ == "__main__":
	main()
