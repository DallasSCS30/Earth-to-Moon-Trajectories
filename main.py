## Main

import math
from settings import *
from physics import *
import time
import os 


class CelestialBody:

	def __init__(self,radius,mu,colour,xPosition,yPosition):
		self.radius = radius
		self.mu = mu
		self.colour = colour
		self.xPosition = xPosition
		self.yPosition = yPosition
		
Earth = CelestialBody(6378140,3.986005E14,BLUE,0,0)

Moon = CelestialBody(1738000,4.902E12,GRAY,384400000,0)


class Spacecraft:
	
	def __init__(self):
	


		
		self.moonLeadAngle = math.radians(float(input("Enter Moon's lead angle: ")))
		self.position = float(input("Enter initial position: "))
		self.positionAngle = math.radians(float(input("Enter position angle: ")))
		self.velocity = float(input("Enter initial velocity: "))
		self.flightPathAngle = math.radians(float(input("Enter flight path angle: ")))
	
		self.positionX = self.position*math.cos(self.positionAngle)
		self.positionY = self.position*math.sin(self.positionAngle)
		
		self.velocityAngle = 1.571 + self.positionAngle - self.flightPathAngle
		self.velocityX = self.velocity*math.cos(self.velocityAngle)
		self.velocityY = self.velocity*math.sin(self.velocityAngle)
	

outputFile = open("C:\\Users\\Dallas\\Desktop\\trajectory.txt","w+")


timeStep = 1
maximumIterations = 300000
iterations = 0
spacecraft = Spacecraft()

lastPlottedPoint = 0     ## has been 0 iterations since we last plotted


running = True

Earth.spacecraftPositionX = spacecraft.positionX
Earth.spacecraftPositionY = spacecraft.positionY
Moon.spacecraftPositionX = spacecraft.positionX - Moon.xPosition
Moon.spacecraftPositionY = Earth.spacecraftPositionY
Earth.positionMagnitude = magnitude(Earth.spacecraftPositionX,Earth.spacecraftPositionY)
Moon.positionMagnitude = magnitude(Moon.spacecraftPositionX,Moon.spacecraftPositionY)
xAcceleration = calculateAcceleration(Earth.mu,Moon.mu,Earth.positionMagnitude,Moon.positionMagnitude,Earth.spacecraftPositionX,Moon.spacecraftPositionX)
yAcceleration = calculateAcceleration(Earth.mu,Moon.mu,Earth.positionMagnitude,Moon.positionMagnitude,Earth.spacecraftPositionY,Moon.spacecraftPositionY)
magnitudeAcceleration = magnitude(xAcceleration,yAcceleration)


while running:
	if iterations > maximumIterations:
		running = False
		
	##print(spacecraft.velocityX,spacecraft.velocityY)
	
	Earth.spacecraftPositionX = calculatePosition(Earth.spacecraftPositionX,spacecraft.velocityX,timeStep)
	Earth.spacecraftPositionY = calculatePosition(Earth.spacecraftPositionY,spacecraft.velocityY,timeStep)
	Earth.positionMagnitude = magnitude(Earth.spacecraftPositionX,Earth.spacecraftPositionY)

	coordinatePair = transformCoordinates(Earth.spacecraftPositionX,Earth.spacecraftPositionY,-spacecraft.moonLeadAngle)

	outputFile.write(coordinatePair[0])
	outputFile.write(",")
	outputFile.write(coordinatePair[1])
	outputFile.write("\n")


	Moon.spacecraftPositionX = calculatePosition(Moon.spacecraftPositionX,spacecraft.velocityX,timeStep)
	Moon.spacecraftPositionY = calculatePosition(Moon.spacecraftPositionY,spacecraft.velocityY,timeStep)
	Moon.positionMagnitude = magnitude(Moon.spacecraftPositionX,Moon.spacecraftPositionY)

	##	Moon.spacecraftPositionX,Moon.spacecraftPositionY = transformCoordinates(Moon.spacecraftPositionX,Moon.spacecraftPositionY,-spacecraft.moonLeadAngle)
		
	spacecraft.velocityX = calculateVelocity(spacecraft.velocityX,xAcceleration,timeStep)
	spacecraft.velocityY = calculateVelocity(spacecraft.velocityY,yAcceleration,timeStep)
	spacecraft.velocityMagnitude = magnitude(spacecraft.velocityX,spacecraft.velocityY)

	xAcceleration = calculateAcceleration(Earth.mu,Moon.mu,Earth.positionMagnitude,Moon.positionMagnitude,Earth.spacecraftPositionX,Moon.spacecraftPositionX)
	yAcceleration = calculateAcceleration(Earth.mu,Moon.mu,Earth.positionMagnitude,Moon.positionMagnitude,Earth.spacecraftPositionY,Moon.spacecraftPositionY)
	magnitudeAcceleration = magnitude(xAcceleration,yAcceleration)

	spacecraft.moonLeadAngle -= math.radians(0.00015*timeStep)

	iterations += 1 


outputFile.close()

import plot