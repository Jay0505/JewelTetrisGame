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

		self.movingRight = False
		self.movingLeft = False
		self.moveDown = True
		self.reachedBottom = False
		self.jewelColor = randint(0, self.settings.colorOfJewels - 1)
		self.myNumber = 0

		self.shape = "rectangle"
		self.positionChanged = False
		self.jewelColorInRGB = (0, 0, 0)
		self.jewelName = " "

	
		

	############################################
	def blitme(self):
		
		if self.jewelColor == 0:
			pygame.draw.rect(self.screen, (9, 132, 227), self.rect)
			self.jewelColorInRGB = (9, 132, 227)
			self.jewelName = "Blue"
			
		elif self.jewelColor == 1:
			pygame.draw.rect(self.screen, (214, 48, 49), self.rect)
			self.jewelColorInRGB = (214, 48, 49)
			self.jewelName = "Red"
			
		elif self.jewelColor == 2:
			pygame.draw.rect(self.screen, (85, 239, 196), self.rect)
			self.jewelColorInRGB = (85, 239, 196)
			self.jewelName = "Green"
		elif self.jewelColor == 3:
			pygame.draw.rect(self.screen, (234, 181, 67), self.rect)
			self.jewelColorInRGB =(234, 181, 67)
			self.jewelName = "Yellow"
			


	############################################
	def update(self):

		screenRect = self.screen.get_rect()

		'''
		-- Since all the jewels are in a group, after every downward (forward) movement of the jewels, we have to check if the next forward step
		would make the jewel go out of the screen. For that reason, after incrementing the jewel's bottom and blitting it on the screen, we check 
		if the next forward step would make the jewel go out of the screen. If yes, we make the reached bottom to True and moveDown to False. If not, 
		we will make the jewel move.
		'''
		if self.rect.bottom <= screenRect.bottom and not self.settings.anyJewelReachedBottom:
			self.rect.bottom += self.settings.jewelSpeedFactor
			self.blitme()

			if self.rect.bottom +  self.settings.jewelSpeedFactor > screenRect.bottom:
				'''
				-- In case of jewels vertically aligned and If one jewel's next step would make it to go out of the screen, we would make the 
				anyJewelReachedBottom to true because, if one jewel reached bottom (the bottom one) then all the jewels above it should not move
				any more further.
				'''
				if self.settings.jewelVerticalOrHorizontal == 0:
					self.settings.anyJewelReachedBottom = True
					self.reachedBottom = True
					self.moveDown = False
				else:
					self.reachedBottom = True
					self.moveDown = False
		
		
		