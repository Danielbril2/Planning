from ConeGenerator import Generator,Cone,Type
import numpy as np
import math
from typing import Tuple
import time

g = Generator()
###
# Creates a map of the track
###
def createMap():
	STRAIGHT_RANGE = 9 # the number of cone coordinates in the straight sections.
	C_BLUE_RANGE = range(2,15) # the number of cone coordinates in the blue half circle section.
	C_YELLOW_RANGE  = range(5,12) # the number of cone coordinates in the yellow half circle section.
 
	# (x - 8)^2 + (y - 8)^2 = 36
	# (x - 8)^2 + (y - 8)^2 = 9
	blue_half_circle_line = lambda x: math.sqrt(36 - math.pow(x - 8, 2)) + 8 
	yellow_half_circle_line = lambda x: math.sqrt(9 - math.pow(x - 8, 2)) + 8

	g.addBlue(np.full(STRAIGHT_RANGE,2),range(STRAIGHT_RANGE)) # adds the blue straight section
	g.addBlue(C_BLUE_RANGE,[blue_half_circle_line(x) for x in C_BLUE_RANGE]) # adds the blue half circle section
	g.addBlue(np.full(STRAIGHT_RANGE,14),range(STRAIGHT_RANGE)) # adds the blue straight section

	g.addYellow(np.full(STRAIGHT_RANGE,5),range(STRAIGHT_RANGE)) # adds the yellow straight section
	g.addYellow(C_YELLOW_RANGE,[yellow_half_circle_line(x) for x in C_YELLOW_RANGE]) # adds the yellow half circle section
	g.addYellow(np.full(STRAIGHT_RANGE,11),range(STRAIGHT_RANGE)) # adds the yellow straight section

###
# Calculates the path of the car
# @param cones: the cones on the track
# @return: tuple of slope and y-intercept
def findLine(cor1: tuple[float,float],cor2: tuple[float,float]) -> tuple[float,float]:
	#cor1,cor2: (x,y)
	m: float = (cor2[1] - cor1[1])/(cor2[0] - cor1[0]) #slope
	b: float = cor1[1] - m * cor1[0] #y-intercept
	return (m,b) #y = mx + b
###
# Calculates the point of intersection of two lines
# @param line1: the first line
# @param line2: the second line
# @return: tuple of x and y coordinates of the point of intersection
def findPoint(line1: tuple[float,float],line2: tuple[float,float]) -> tuple[float,float]:
	x: float = (line2[1] - line1[1])/(line1[0] - line2[0]) #x-coordinate
	y: float = line1[0] * x + line1[1] #y-coordinate
	return (x,y) #point of intersection

###
# Calculates the path of the car
# @param cones: the cones on the track
# @return: list of tuples of x and y coordinates of the path
def calculatePath(cones: list[Cone]) -> list[(float,float)]:
	blueCones: list[Cone] = [c for c in cones if c.type == Type.BLUE] #list of blue cones
	yellowCones: list[Cone] = [c for c in cones if c.type == Type.YELLOW] #list of yellow cones

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
