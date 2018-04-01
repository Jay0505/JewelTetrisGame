import sys
import pygame

from turtle import *
from random import randint
from pygame.sprite import Group
#from pygame.Surface import *


class Rectangle(object):
	"""docstring for rectangle"""
	def __init__(self):
		super(Rectangle, self).__init__()
		self.color = "Blue"



def drawUsingPygame():
	pygame.init()
	screen = pygame.display.set_mode((500, 500))
	screen.fill((255, 255, 255))

	rectangle = Rectangle()
	rectangle = pygame.draw.rect(screen, (0, 184, 148), (100, 100, 70, 70))
	print(screen.get_at((100, 100)))
	
	pygame.display.flip()

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()


drawUsingPygame()