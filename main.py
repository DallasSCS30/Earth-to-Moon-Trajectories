##-------------------------------------------------------------------
## Earth to Moon Trajectory Computer
## Dallas Spendelow
## November 8, 2018
## This program computes Earth-to-Moon trajectories numerically,
## rotating coordinates (rotating with the moon).
##-------------------------------------------------------------------

## We need to do some math, as well as store files on the OS.
## We also need to use our other modules. Note: 'plot.py' will
## be imported only when we need it. 
import math
from settings import *
from physics import *
import os 


## A celestial body class. Has a radius, mu (gravitational parameter),
## a colour, and a position.
class CelestialBody:

    def __init__(self,radius,mu,colour,xPosition,yPosition):
        self.radius = radius
        self.mu = mu
        self.colour = colour
        self.xPosition = xPosition
        self.yPosition = yPosition

## The class for the spacecraft. It has certain properties like position,
## velocity, and acceleration. 
class Spacecraft:
    
    ## Vocabulary: The 'antipode' is an imaginary line from the Earth to the Moon's
    ## position at arrival. 
    def __init__(self):
        ## How far behind the antipode is the moon? About 40
        self.moonLeadAngle = math.radians(float(input("Enter Moon's lead angle (degrees): ")))    
        ## What is the spacecraft's distance from the center of the Earth. 
        self.position = float(input("Enter initial position (metres): "))      
        ## What is the spacecraft's angle ahead of the antipode. About 20
        self.positionAngle = math.radians(float(input("Enter position angle(degrees): ")))
        self.positionAngle += 3.1415926535
        ## How fast is the spacecraft going? 10,800 - 10,900
        self.velocity = float(input("Enter initial velocity (m/s): "))        
        ## At what angle above horizontal is this velocity directed at? 7-8 .
        self.flightPathAngle = math.radians(float(input("Enter flight path angle (degrees): ")))

        self.positionX = self.position*math.cos(self.positionAngle)
        self.positionY = self.position*math.sin(self.positionAngle)
        
        self.velocityAngle = 1.571 + self.positionAngle - self.flightPathAngle
        self.velocityX = self.velocity*math.cos(self.velocityAngle)
        self.velocityY = self.velocity*math.sin(self.velocityAngle)
	

## Both the Earth and the Moon are celestial bodies.
Earth = CelestialBody(6378140,3.986005E14,BLUE,0,0)
Moon = CelestialBody(1738000,4.902E12,GRAY,384400000,0)

## The spacecraft is a spacecraft. 
spacecraft = Spacecraft()


## Open the output file, and set constants.
outputFile = open("trajectory.txt","w+")


timeStep = 1      ## How many seconds per iteration.
maximumIterations = 300000    ## How many iterations
currentIteration = 0    ## Current iteration


running = True

## The following block takes the initial conditions, and processes them
## so they can be used to start iterating.

## Spacecraft's position relative to Earth and Moon. 
Earth.spacecraftPositionX = spacecraft.positionX
Earth.spacecraftPositionY = spacecraft.positionY
Moon.spacecraftPositionX = spacecraft.positionX - Moon.xPosition
## Since moon is on x axis, the spacecraft's y position relative to Earth
## is also the y position relative to the moon. 
Moon.spacecraftPositionY = Earth.spacecraftPositionY

Earth.positionMagnitude = magnitude(Earth.spacecraftPositionX,Earth.spacecraftPositionY)
Moon.positionMagnitude = magnitude(Moon.spacecraftPositionX,Moon.spacecraftPositionY)

## Spacecraft's acceleration. 
xAcceleration = calculateAcceleration(Earth.mu,Moon.mu,Earth.positionMagnitude,Moon.positionMagnitude,Earth.spacecraftPositionX,Moon.spacecraftPositionX)
yAcceleration = calculateAcceleration(Earth.mu,Moon.mu,Earth.positionMagnitude,Moon.positionMagnitude,Earth.spacecraftPositionY,Moon.spacecraftPositionY)
magnitudeAcceleration = magnitude(xAcceleration,yAcceleration)


while running:
	if currentIteration > maximumIterations:
		running = False               ## Stop program when finished
		
	##print(spacecraft.velocityX,spacecraft.velocityY)
	
	## Update positions. The moon's position is not used. Future versions may display
        ## closest approach to the moon.
	## Note: All calculations are done in an inertial frame of reference, and transformed to
	## rotating coordinates.
	Earth.spacecraftPositionX = calculatePosition(Earth.spacecraftPositionX,spacecraft.velocityX,timeStep)
	Earth.spacecraftPositionY = calculatePosition(Earth.spacecraftPositionY,spacecraft.velocityY,timeStep)
	Earth.positionMagnitude = magnitude(Earth.spacecraftPositionX,Earth.spacecraftPositionY)

	Moon.spacecraftPositionX = calculatePosition(Moon.spacecraftPositionX,spacecraft.velocityX,timeStep)
	Moon.spacecraftPositionY = calculatePosition(Moon.spacecraftPositionY,spacecraft.velocityY,timeStep)
	Moon.positionMagnitude = magnitude(Moon.spacecraftPositionX,Moon.spacecraftPositionY)
        
        ## Transforms the pair of (x,y) to rotating coordinates.
	coordinatePair = transformCoordinates(Earth.spacecraftPositionX,Earth.spacecraftPositionY,-spacecraft.moonLeadAngle)

        ## Writes the pair to the text file.
	outputFile.write(coordinatePair[0])
	outputFile.write(",")
	outputFile.write(coordinatePair[1])
	outputFile.write("\n")
	
	## Update spacecraft's velocity and acceleration.	
	spacecraft.velocityX = calculateVelocity(spacecraft.velocityX,xAcceleration,timeStep)
	spacecraft.velocityY = calculateVelocity(spacecraft.velocityY,yAcceleration,timeStep)
	spacecraft.velocityMagnitude = magnitude(spacecraft.velocityX,spacecraft.velocityY)

	xAcceleration = calculateAcceleration(Earth.mu,Moon.mu,Earth.positionMagnitude,Moon.positionMagnitude,Earth.spacecraftPositionX,Moon.spacecraftPositionX)
	yAcceleration = calculateAcceleration(Earth.mu,Moon.mu,Earth.positionMagnitude,Moon.positionMagnitude,Earth.spacecraftPositionY,Moon.spacecraftPositionY)
	magnitudeAcceleration = magnitude(xAcceleration,yAcceleration)

        ## The moon has, meanwhile, rotated through an angle of 0.00015 degrees/second.
	## The coordinate system, thus, has also rotated. 
	spacecraft.moonLeadAngle -= math.radians(0.00015*timeStep)

        ## The end of an iteration. Count up.
	currentIteration += 1 


## We are done writing to the text file.	
outputFile.close()

## Now use the plot module to plot the points.
import plot