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
		self.myNumber = 0

		self.shape = "rectangle"

	
		

	############################################
	def blitme(self):
		
		if self.jewelColor == 0:
			pygame.draw.rect(self.screen, (9, 132, 227), self.rect)
			
		elif self.jewelColor == 1:
			pygame.draw.rect(self.screen, (214, 48, 49), self.rect)
			
		elif self.jewelColor == 2:
			pygame.draw.rect(self.screen, (85, 239, 196), self.rect)
			
		elif self.jewelColor == 3:
			pygame.draw.rect(self.screen, (234, 181, 67), self.rect)
			


	############################################
	def update(self):

		screenRect = self.screen.get_rect()

		
		if self.rect.bottom <= screenRect.bottom and not self.settings.anyJewelReachedBottom:
			self.rect.bottom += 10
			self.blitme()

			if self.rect.bottom +  10 > screenRect.bottom:
				if self.settings.jewelVerticalOrHorizontal == 0:
					self.settings.anyJewelReachedBottom = True
					self.reachedBottom = True
					self.moveDown = False
				else:
					self.reachedBottom = True
					self.moveDown = False
		
		
		