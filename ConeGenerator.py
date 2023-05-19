import numpy as np
from enum import Enum
import math
import matplotlib.pyplot as plt
import random

class Type(Enum):
	YELLOW = 1
	BLUE = 2

class Cone:
	def __init__(self, id, x,y,type):
		self.id = id
		self.x = x
		self.y = y
		self.type = type

	def getId(self):
		return self.id
	def getX(self):
		return self.x
	def getY(self):
		return self.y
	def getType(self):
		return self.type

###
# Class to generate cones
# blueX: list of x coordinates of blue cones
# blueY: list of y coordinates of blue cones
# yellowX: list of x coordinates of yellow cones
# yellowY: list of y coordinates of yellow cones
###
class Generator:
	def __init__(self,blueX=[],blueY=[],yellowX=[],yellowY=[]):
		self.blueX = blueX
		self.blueY = blueY
		self.yellowX = yellowX
		self.yellowY = yellowY
###
# Adds a list of x and y coordinates to the blue cones
# xData: list of x coordinates
# yData: list of y coordinates
###
	def addBlue(self,xData,yData):
		self.blueX.extend(xData)
		self.blueY.extend(yData)
###
# Adds a list of x and y coordinates to the yellow cones
# xData: list of x coordinates
# yData: list of y coordinates
###
	def addYellow(self,xData,yData):
		self.yellowX.extend(xData)
		self.yellowY.extend(yData)
###
# Adds a list of x and y coordinates to the blue cones
# xData: list of x coordinates
# yData: list of y coordinates
###
	def getBluePoints(self):
		return [(self.blueX[i], self.blueY[i]) for i in range(len(self.blueX))]
###
# Adds a list of x and y coordinates to the yellow cones
# xData: list of x coordinates
# yData: list of y coordinates
###
	def getYellowPoints(self):
		return [(self.yellowX[i], self.yellowY[i]) for i in range(len(self.yellowX))]

###
# Generates a list of cones
# returns: list of cones
###
	def generateData(self):
		#return list of cones in the right coordinates
		cones = []
		idCounter = 0
		for i in range(len(self.blueX)):
			c = Cone(idCounter,self.blueX[i],self.blueY[i],Type.BLUE)
			idCounter += 1
			cones.append(c)

		for i in range(len(self.yellowX)):
			c = Cone(idCounter,self.yellowX[i],self.yellowY[i],Type.YELLOW)
			idCounter += 1
			cones.append(c)

		return cones

###
# adds noise to the cones' coordinates and returns a new list of cones with the added noise
# cones: list of cones
# sd: standard deviation -> float
# dist: mean distance to add to each cone -> float. Default is 0
# returns: new list of cones with noise
###
	@staticmethod
	def addNoise(cones, sd, dist = 0):
     
		xNoise = np.random.normal(dist,sd,len(cones))
		yNoise = np.random.normal(dist,sd,len(cones))

		newCones = []
		for i in range(len(cones)):
			if (random.uniform(0,1) < 0.9): # ~every 1 in 10 cones is not shown
				newCones.append(Cone(cones[i].id,cones[i].x + xNoise[i],cones[i].y + yNoise[i],cones[i].type))

		return newCones
		#return [Cone(cones[i].id,cones[i].x + xNoise[i],cones[i].y + yNoise[i],cones[i].type) for i in range(len(cones))]

###
# adds noise to the cones' coordinates and returns a new list of cones with the added noise
# cones: list of cones
# sd: standard deviation -> float
# dist: mean distance to add to each cone -> float. Default is 0
# returns: new list of cones with noise
###
	@staticmethod
	def addNoiseToSide(cones, sd, dist = 0):
		xNoise = np.random.normal(dist,sd,len(cones))
		yNoise = np.random.normal(dist,sd,len(cones))

		newCones = []
		for i in range(len(cones)):
			if (random.uniform(0,1) < 0.9): # ~every 1 in 10 cones is not shown
				newCones.append((cones[i][0] + xNoise[i],cones[i][1] + yNoise[i]))

		return newCones


###
# The method takes a list of cones and an optional path parameter that represents an additional path to be plotted.
# cones: list of cones
# path: list of points to be plotted
###
	@staticmethod
	def showGraph(cones, path = None):
		for c in cones:
			color = ""
			if c.type == Type.BLUE:
				color = "blue"
			else:
				color = "yellow"

			plt.scatter(c.x,c.y,c = color)

		if path != None:
			for p in path:
				plt.scatter(p[0],p[1],c = "red")

		plt.show()


def main():
	STRAIGHT_RANGE = 9
	C_BLUE_RANGE = range(2,15)
	C_YELLOW_RANGE  = range(5,12)

	blue_half_circle_line = lambda x: math.sqrt(36 - math.pow(x - 8, 2)) + 8 # (x - 8)^2 + (y - 8)^2 = 36
	yellow_half_circle_line = lambda x: math.sqrt(9 - math.pow(x - 8, 2)) + 8 # (x - 8)^2 + (y - 8)^2 = 9

	g = Generator()
	g.addBlue(np.full(STRAIGHT_RANGE,2),range(STRAIGHT_RANGE))
	g.addBlue(C_BLUE_RANGE,[blue_half_circle_line(x) for x in C_BLUE_RANGE])
	g.addBlue(np.full(STRAIGHT_RANGE,14),range(STRAIGHT_RANGE))

	g.addYellow(np.full(STRAIGHT_RANGE,5),range(STRAIGHT_RANGE))
	g.addYellow(C_YELLOW_RANGE,[yellow_half_circle_line(x) for x in C_YELLOW_RANGE])
	g.addYellow(np.full(STRAIGHT_RANGE,11),range(STRAIGHT_RANGE))

	cones = g.generateData()

	newCones = Generator.addNoise(cones,sd = 0.1)
	Generator.showGraph(newCones)


if __name__ == "__main__":
	main()