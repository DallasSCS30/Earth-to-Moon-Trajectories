##-------------------------------------------------------------------
## Physics Module 
## Dallas Spendelow
## November 8, 2018
## This module does physics for the trajectory computer program.
##-------------------------------------------------------------------

## We need to do some math. 
import math

## Calculates acceleration using the equation of two-body motion. Actually,
## it considers both the Earth and Moon gravity, so it is three-body
## (spacecraft included as well).
def calculateAcceleration(mu1,mu2,position1,position2,component1,component2):
	acceleration = -mu1/position1**3*component1 - mu2/position2**3*component2
	return acceleration
	
## final velocity = initial velocity + acceleration times time.	
def calculateVelocity(initialVelocity,acceleration,timeStep):
	velocity = initialVelocity + acceleration*timeStep
	return velocity
	
## initial position + velocity times time. Because we assume a constant
## velocity for each time interval, this is how it is done, not 1/2at^2.
def calculatePosition(initialPosition,velocity,timeStep):
	position = initialPosition + velocity*timeStep 
	return position

## Transform coordinates through an angle.
def transformCoordinates(x,y,angle):
	pair = []
	transformedX = x*math.cos(angle)+ y*math.sin(angle)
	transformedY = -x*math.sin(angle) + y*math.cos(angle)
	pair = [str(transformedX),str(transformedY)]
	return pair
	
## Calculate the magnitude of a vector.
def magnitude(x,y):
	magnitude = math.sqrt(x**2+y**2)
	return magnitude