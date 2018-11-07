## Physics Module

import math


def calculateAcceleration(mu1,mu2,position1,position2,component1,component2):
	acceleration = -mu1/position1**3*component1 - mu2/position2**3*component2
	return acceleration
	
def calculateVelocity(initialVelocity,acceleration,timeStep):
	velocity = initialVelocity + acceleration*timeStep
	return velocity
	
def calculatePosition(initialPosition,velocity,timeStep):
	position = initialPosition + velocity*timeStep 
	return position
	
def transformCoordinates(x,y,angle):
	pair = []
	transformedX = x*math.cos(angle)+ y*math.sin(angle)
	transformedY = -x*math.sin(angle) + y*math.cos(angle)
	pair = [str(transformedX),str(transformedY)]
	return pair
	
def magnitude(x,y):
	magnitude = math.sqrt(x**2+y**2)
	return magnitude
		
		
		
	

