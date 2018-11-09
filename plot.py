##-------------------------------------------------------------------
## Plot Module
## Dallas Spendelow
## November 8, 2018
## This module plots the calculated trajectory using pyGame.
##-------------------------------------------------------------------

import pygame
from settings import *

## Class for a point. Has an x and a y.
class Point(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((1,1))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x//SCALE + 33000000//SCALE
        self.rect.y = y//SCALE + HEIGHT/2 

## Class for a planet (or moon). Needs a radius, colour, and center position.
class Planet(pygame.sprite.Sprite):
    def __init__(self, radius, colour, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((radius//SCALE*2,radius//SCALE*2))
        self.image.fill(BLACK)
        pygame.draw.circle(self.image, (colour), (radius//SCALE,radius//SCALE), radius//SCALE)
        self.rect = self.image.get_rect()
        self.rect.center = (center//SCALE,HEIGHT/2)        

## Initialize pyGame. 
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Trajectory")
screen.fill(BLACK)
clock = pygame.time.Clock()
clock.tick(FPS)

## Create Earth and Moon
allSprites = pygame.sprite.Group()
Earth = Planet(6378000, BLUE, 33000000)
allSprites.add(Earth)

Moon = Planet(1738000, GRAY, 417000000)     ## Or moon. 
allSprites.add(Moon)

## Open the text file and plot every point.
## Add each point to sprites and close when done.
plotFile = open("trajectory.txt", "r")
for line in plotFile:
	line = plotFile.readline()
	line = line.rstrip("\n")
	pointList = line.split(",")

	xCoord = float(pointList[0])
	yCoord = -float(pointList[1])
	
	##print(xCoord,yCoord)

	point = Point(xCoord,yCoord)
	allSprites.add(point)
plotFile.close()	

## Draw trajectory
allSprites.draw(screen)
pygame.display.flip()

running = True

## Check for a window exit and quit pyGame. 
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

pygame.quit()