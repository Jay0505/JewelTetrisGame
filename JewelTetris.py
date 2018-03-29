import sys
import pygame

from JewelSettings import Settings
import JewelGameFunctions as jgf
from pygame.sprite import Group
from random import randint

def run_game():

	redFlag = False
	pygame.init()

	settings = Settings()

	currentJewelsGroup = Group()
	screen = pygame.display.set_mode((settings.screenWidth, settings.screenHeight))
	screen.fill((150, 150, 150))

	while True:

		if settings.isFirstIteration:

			settings.isFirstIteration = False
			jgf.funcResponsibleForCreationAndMovementOfJewels(settings, currentJewelsGroup, screen)

		else:
			if jgf.checkIfTheJewelGroupReachedBottom(settings.jewels):
				
				jgf.groupTheBottomReachedJewelsIntoOne(settings, currentJewelsGroup)
				jgf.resetAllTheSettings(settings)
				jgf.funcResponsibleForCreationAndMovementOfJewels(settings, currentJewelsGroup, screen)

			else:

				jgf.funcResponsibleForMovementOfJewelsAndScreenUpdate(settings, currentJewelsGroup, screen)


run_game()




