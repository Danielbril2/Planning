import numpy as np
from enum import Enum
import math
import matplotlib.pyplot as plt

class Type(Enum):
	YELLOW = 1
	BLUE = 2
	ORANGE = 3

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

class Generator:
	def __init__(self,noise = None,blueX=[],blueY=[],yellowX=[],yellowY=[]):
		'''
		args:
			noise: object that has a noise function
		'''
		self.noise = noise
		self.blueX = blueX
		self.blueY = blueY
		self.yellowX = yellowX
		self.yellowY = yellowY

	def addBlue(self,xData,yData):
		self.blueX.extend(xData)
		self.blueY.extend(yData)

	def addYellow(self,xData,yData):
		self.yellowX.extend(xData)
		self.yellowY.extend(yData)

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
		
	@staticmethod
	def addNoise(cones, sd, dist = 0):
		'''
		args:
			cones: list[Cone]
			dist: mean distance to add to each cone -> float. Default is 0
			sd: standard deviation -> float
		return:
			new list of cones with noise
		'''
		mean = 10 #need to somehow calculate the mean
		xNoise = np.random.normal(mean,sd,len(cones))
		yNoise = np.random.normal(mean,sd,len(cones))
		
		newCones = []
		counter = 0
		for c in cones:
			newCones.append(Cone(c.getId(),c.getX() + xNoise[counter],c.getY() + yNoise[counter],c.getType()))
			counter += 1

		return newCones


	@staticmethod
	def showGraph(cones):
		for c in cones:
			color = ""
			if c.getType() == Type.BLUE:
				color = "blue"
			else:
				color = "yellow"

			plt.scatter(c.getX(),c.getY(),c = color)

		plt.show()


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
Generator.showGraph(cones)

newCones = Generator.addNoise(cones,sd = 0.1)
Generator.showGraph(newCones)