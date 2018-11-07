## Plot Module

import pygame
from settings import *


class Earth(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((6378000//SCALE*2,6378000//SCALE*2))
		self.image.fill(BLACK)
		pygame.draw.circle(self.image, (BLUE), (6378000//SCALE,6378000//SCALE), 6378000//SCALE)
		self.rect = self.image.get_rect()
		self.rect.center = (33000000//SCALE,HEIGHT/2)
		
class Moon(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((1738000//SCALE*2,1738000//SCALE*2))
		self.image.fill(BLACK)
		pygame.draw.circle(self.image, (GRAY), (1738000//SCALE,1738000//SCALE), 1738000//SCALE)
		self.rect = self.image.get_rect()
		self.rect.center = (417000000//SCALE,HEIGHT/2)


class Point(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((1,1))
		self.image.fill(WHITE)
		self.rect = self.image.get_rect()
		self.rect.x = x//SCALE + 33000000//SCALE
		self.rect.y = y//SCALE + HEIGHT/2 

		
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Trajectory")
screen.fill(BLACK)
clock = pygame.time.Clock()
clock.tick(FPS)

allSprites = pygame.sprite.Group()
Earth = Earth()
allSprites.add(Earth)

Moon = Moon()
allSprites.add(Moon)

plotFile = open("C:\\Users\\Dallas\Desktop\\trajectory.txt", "r")
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

allSprites.draw(screen)
pygame.display.flip()

running = True

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

pygame.quit()



