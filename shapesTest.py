import sys
import pygame

from turtle import *
from random import randint
from pygame.sprite import Group

def drawUsingTurtles():
	canvas = Screen()
	canvas.setup(400, 400)

	sarah = Turtle()

	for i in range(5):
		sarah.forward(50)
		sarah.left(90)

	canvas.exitonclick

def drawUsingPygame():
	pygame.init()
	screen = pygame.display.set_mode((500, 500))
	screen.fill((255, 255, 255))

	# rect1 = Rect(randint(0, 461), randint(0, 453), 60, 48)
	

	rectangles = Group
	rectangle = pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(5, 5, 60, 48))
	rectangles.add(rectangle)

	rectangle2 = pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(10, 10, 60, 48))
	rectangles.add(rectangle2)

	rectangles.update(onRectangles)
	# rectangle.y = randint(0, 453)
	# # rectangle2 = pygame.draw.rect(screen, (125, 125, 125), pygame.Rect(10, 20, 50, 20))
	# # ship1 = pygame.image.load('images/ship.bmp')
	# # ship2 = pygame.image.load('images/ship.bmp')

	# # ship1_rect = ship1.get_rect()
	# # ship2Rect = ship2.get_rect()
	# # screenRect = screen.get_rect()

	# # x1Coordinate = randint(0, 461)
	# # x2Coordinate = randint(0, 461)
	# # ship1_rect.x = x1Coordinate
	# # ship2Rect.x = x1Coordinate

	# # y1Coordinate = randint(0, 453)
	# # y2Coordinate = randint(0, 453)

	# # ship1_rect.y = y1Coordinate
	# # ship2Rect.y = y1Coordinate + ship1_rect.height

	# # print(ship1_rect.width)
	# # print(ship2Rect.width)
	# # print(ship1_rect.height)

	# # screen.blit(ship1, ship1_rect)
	# # screen.blit(ship2, ship2Rect)
	# print(rectangle.x)
	# print(rectangle.y)

	pygame.display.flip()

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

def onRectangles(rectangles):
	for rectangle in rectangles.sprites():
		rectangle.width += 20

	print("increased")

drawUsingPygame()