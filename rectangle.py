import pygame
from pygame.sprite import Sprite
from random import randint

class Rectangle(Sprite):
	"""docstring for Rectangle"""
	def __init__(self, screen, settings):
		super().__init__()
		self.screen = screen
		self.settings = settings
		self.width = 30
		self.height = 20
		rectangleImage = pygame.image.load('images/rectangle.bmp')
		self.image = pygame.transform.scale(rectangleImage, (self.settings.jewelWidth, self.settings.jewelHeight))

		self.rect = self.image.get_rect()

		self.x = float(self.rect.x)
		self.y = float(self.rect.y)
		self.centerX = float(self.rect.centerx)
		self.centerY = float(self.rect.centery)

		self.movingRight = True
		self.movingLeft = True
		self.moveDown = True
		self.reachedBottom = False
		self.jewelColor = randint(0, self.settings.colorOfJewels - 1)
		self.imageNumber = randint(0, self.settings.totalNumberOfImages - 1)

		self.shape = "rectangle"
	
		

	############################################
	def blitme(self):
		
		if self.jewelColor == 0: # splash-blue
			pygame.draw.rect(self.screen, (9, 132, 227), self.rect)
			
		elif self.jewelColor == 1: # mintleaf
			pygame.draw.rect(self.screen, (0, 184, 148), self.rect)
			
		elif self.jewelColor == 2: # faded poster
			pygame.draw.rect(self.screen, (129, 236, 236), self.rect)
			
		elif self.jewelColor == 3: # orange-ville
			pygame.draw.rect(self.screen, (225, 112, 85), self.rect)

		elif self.jewelColor == 4: # peri-vinkle
			pygame.draw.rect(self.screen, (156, 136, 255), self.rect)

		elif self.jewelColor == 5: # riseNshine
			pygame.draw.rect(self.screen, (251, 197, 49), self.rect)

		elif self.jewelColor == 6: # white
			pygame.draw.rect(self.screen, (245, 246, 250), self.rect)

		# if self.imageNumber == 0:
		# 	rectangleImage = pygame.image.load('images/blueCircles.bmp')
		# 	self.image = pygame.transform.scale(rectangleImage, (self.settings.jewelWidth, self.settings.jewelHeight))

		# elif self.imageNumber == 1:
		# 	rectangleImage = pygame.image.load('images/coloredCircles.bmp')
		# 	self.image = pygame.transform.scale(rectangleImage, (self.settings.jewelWidth, self.settings.jewelHeight))

		# elif self.imageNumber == 2:
		# 	rectangleImage = pygame.image.load('images/coloredLove.bmp')
		# 	self.image = pygame.transform.scale(rectangleImage, (self.settings.jewelWidth, self.settings.jewelHeight))

		# elif self.imageNumber == 3:
		# 	rectangleImage = pygame.image.load('images/paperBoats.bmp')
		# 	self.image = pygame.transform.scale(rectangleImage, (self.settings.jewelWidth, self.settings.jewelHeight))

		# elif self.imageNumber == 4:
		# 	rectangleImage = pygame.image.load('images/pathang.bmp')
		# 	self.image = pygame.transform.scale(rectangleImage, (self.settings.jewelWidth, self.settings.jewelHeight))

		# elif self.imageNumber == 5:
		# 	rectangleImage = pygame.image.load('images/plate.bmp')
		# 	self.image = pygame.transform.scale(rectangleImage, (self.settings.jewelWidth, self.settings.jewelHeight))

		# elif self.imageNumber == 6:
		# 	rectangleImage = pygame.image.load('images/whiteBulb.bmp')
		# 	self.image = pygame.transform.scale(rectangleImage, (self.settings.jewelWidth, self.settings.jewelHeight))

		# self.screen.blit(self.image, self.rect)


	############################################
	def update(self):

		screenRect = self.screen.get_rect()

		#if not self.settings.anyJewelReachedBottom and self.rect.bottom < screenRect.bottom - self.settings.jewelHeight:
		if self.rect.bottom <= screenRect.bottom - self.settings.jewelHeight:
			self.rect.y += 8
			#newrect = Rectangle(self.screen, self.settings)
			#newrect.rect.y = self.rect.y
			self.blitme()
		else:
			self.settings.anyJewelReachedBottom = True
			self.reachedBottom = True
			self.moveDown = False


	def draw(self, shapeOfTheJewel, colorOfTheJewel):
		pygame.draw.rect(self.screen, colorOfTheJewel, self.rect)




		