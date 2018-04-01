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

		self.shape = "rectangle"
	
		

	############################################
	def blitme(self):
		
		if self.jewelColor == 0:
			pygame.draw.rect(self.screen, (255, 0, 0), self.rect)
			
		elif self.jewelColor == 1:
			pygame.draw.rect(self.screen, (0, 0, 0), self.rect)
			
		elif self.jewelColor == 2:
			pygame.draw.rect(self.screen, (2, 0, 182), self.rect)
			
		elif self.jewelColor == 3:
			pygame.draw.rect(self.screen, (249, 158, 2), self.rect)
			


	############################################
	def update(self):

		screenRect = self.screen.get_rect()

		#if not self.settings.anyJewelReachedBottom and self.rect.bottom < screenRect.bottom - self.settings.jewelHeight:
		if self.rect.bottom <= screenRect.bottom - self.settings.jewelHeight:
			self.rect.y += 3
			#newrect = Rectangle(self.screen, self.settings)
			#newrect.rect.y = self.rect.y
			self.blitme()
		else:
			self.settings.anyJewelReachedBottom = True
			self.reachedBottom = True
			self.moveDown = False


	def draw(self, shapeOfTheJewel, colorOfTheJewel):
		pygame.draw.rect(self.screen, colorOfTheJewel, self.rect)




		