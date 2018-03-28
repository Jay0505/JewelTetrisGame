import sys
import pygame

from JewelSettings import Settings
#from NewValuesForNewJewels import CurrentIterationSettings as CIT
import JewelGameFunctions as jgf
from pygame.sprite import Group
from random import randint

def run_game():

	pygame.init()
	settings = Settings()
	jewels = Group() # At each iteration, formed jewels will be termed as one group
	screen = pygame.display.set_mode((settings.screenWidth, settings.screenHeight))
	screen.fill((150, 150, 150))

	jewelType = randint(1, settings.jewelType)
	jewelVerticalORHorizontal = randint(0, settings.jewelVerticalOrHorizontal)
	jgf.createJewelGroup(settings, screen, jewelType, jewelVerticalORHorizontal, jewels)

	while True:
		jgf.checkEvents(settings, screen, jewels) # Checks for any key press or release events
		jgf.forwardJewels(settings, jewels, jewelType) # move the jewels in the downward direction
		jgf.moveJewels(settings, screen, jewels) # move the jewels either right or left based upon the key pressed
		jgf.updateScreen(settings, screen, jewelType, jewels) # updates the screen with the latest positions of the jewels

#####################################

def createAnEmptyJewelGroup(cit):
	cit.currentJewelsGroup = Group()
	#return jewels


def determineJewelType(settings, cit):
	cit.currentJewelType = randint(1, settings.jewelType)
	#return jewelType


#####################################	

def determineVerticallyOrHorizontallyAlignedJewels(settings, cit):
	cit.currentJewelVerticalORHorizontal = randint(0, settings.jewelVerticalOrHorizontal)
	#return jewelVerticalORHorizontal


####################################

def determineJewelTypeAlignmentAndThenCreateJewelGroup(settings, screen):
	#jewels = createAnEmptyJewelGroup()
	# CIT.currentJewelType = determineJewelType(settings)
	# CIT.currentJewelVerticalORHorizontal = determineVerticallyOrHorizontallyAlignedJewels(settings)
	cit = CIT(settings)
	createAnEmptyJewelGroup()
	determineJewelType(settings)
	determineVerticallyOrHorizontallyAlignedJewels(settings)
	jgf.createJewelGroup(settings, screen, CIT.currentJewelType, CIT.currentJewelVerticalORHorizontal, CIT.currentJewelsGroup)

def resetAllTheSettings(settings):
	# Jewel settings
	settings.jewelVerticalOrHorizontal = 1 # vertical = 0; Horizontal = 1
	settings.jewelType = 1
	settings.jewelsLimit = 4
	settings.jewelDirection = 1
	settings.jewelMovingRight = False
	settings.jewelMovingLeft = False
	settings.anyJewelReachedEdge = False
	settings.anyJewelReachedBottom = False



run_game()




