import pygame
from pygame.sprite import Sprite

class Rectangle(Sprite):
	"""docstring for Rectangle"""
	def __init__(self, screen, settings):
		super().__init__()
		self.screen = screen
		self.settings = settings
		self.width = 30
		self.height = 20
		rectangleImage = pygame.image.load('images/rectangle.bmp')
		self.image = pygame.transform.scale(rectangleImage, (self.width, self.height))

		self.rect = self.image.get_rect()

		self.x = float(self.rect.x)
		self.y = float(self.rect.y)
		self.centerX = float(self.rect.centerx)
		self.centerY = float(self.rect.centery)

		self.movingRight = False
		self.movingLeft = False
		

	############################################
	def blitme(self):
		#self.screen.blit(self.image, self.rect)
		pygame.draw.rect(self.screen, (230, 230, 230), self.rect)


	############################################
	def update(self):

		screenRect = self.screen.get_rect()

		if (not self.settings.anyJewelReachedBottom) and self.rect.bottom < screenRect.bottom:
			self.rect.y += 3
			newrect = Rectangle(self.screen, self.settings)
			newrect.rect.y = self.rect.y
			newrect.blitme()
		else:
			self.settings.anyJewelReachedBottom = True




		