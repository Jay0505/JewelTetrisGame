import sys
import pygame

from pygame.sprite import Group
from random import randint
from rectangle import Rectangle



######################################## KEY EVENTS ###########################################

def checkEvents(settings, screen, jewels):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		elif event.type == pygame.KEYDOWN:
			keyDownEvents(settings, screen, event,jewels)

		elif event.type == pygame.KEYUP:
			keyUpEvents(settings, screen, event, jewels)

########
'''
-- If the user presses the right arrow key down, then the jewels should move right, in other words the x-coordinate
should increase. Therefore, we check for the settings.jewelDirection variable for whether it is positive or negative.
If it is negative and the key pressed is right arrow, we change the direction value to a positive value.

-- If the user presses the left arrow key down, then the jewels should move left, in other words the x-coordinate
should decrease. Therefore, we check for the settings.jewelDirection variable for whether it is positive or negative.
If it is positive and the key pressed is left arrow, we change the direction value to a negative value.

-- Also, we change the jewelMovingRight to True if the right arrow key pressed likewise we set jewelMovingLeft to True
if the left arrow key is pressed.

'''
def keyDownEvents(settings, screen, event, jewels):
	if event.key == pygame.K_RIGHT:
		settings.jewelMovingRight = True
		if settings.jewelDirection == -1:
			settings.jewelDirection = 1 

	elif event.key == pygame.K_LEFT:
		if settings.jewelDirection == 1:
			settings.jewelDirection = -1

		settings.jewelMovingLeft = True



#########
'''
-- If the left arrow key is released, then we set the jewelMovingLeft to false likewise if the right arrow key is 
just released, we set the jewelMovingRight to false.
'''

def keyUpEvents(settings, screen, event, jewels):
	if event.key == pygame.K_LEFT:
		settings.jewelMovingLeft = False

	elif event.key == pygame.K_RIGHT:
		settings.jewelMovingRight = False





####################### JEWEL FUNCTIONS ########################################################

def createJewelGroup(settings, screen, jewelType, jewelVerticalOrHorizontal, jewels):
	if jewelVerticalOrHorizontal == 1:
		createHorizontallyAlignedJewels(settings, screen, jewelType, jewels)
	else:
		settings.jewelVerticalOrHorizontal = 0
		createVerticallyAlignedJewels(settings, screen, jewelType, jewels)

#########

def createVerticallyAlignedJewels(settings, screen, jewelType, jewels):
	numberOfJewels = fixTheNumberOfJewelsToBeFormed(settings)
	yCoordinate = 0
	xCoordinate = 250
	for number in range(numberOfJewels - 1, -1, -1):
		rectangle = Rectangle(screen, settings)
		if number == 0:
			rectangle.rect.y = yCoordinate
		else:
			# We add '+1' to create some space between jewels so as to create a boundary between jewels
			rectangle.rect.y = (number * rectangle.height) + (2 * number) 
		rectangle.rect.x = xCoordinate
		jewels.add(rectangle)


def createHorizontallyAlignedJewels(settings, screen, jewelType, jewels):
	numberOfJewels = fixTheNumberOfJewelsToBeFormed(settings)
	xCoordinate = 250
	for number in range(numberOfJewels):
		rectangle = Rectangle(screen, settings)
		if number == 0:
			rectangle.rect.x = xCoordinate 
		else:
			# We add '+1' to create some space between jewels so as to create a boundary between jewels
			rectangle.rect.x = xCoordinate + (number * rectangle.width) + (2 * number)

		jewels.add(rectangle)

def fixTheNumberOfJewelsToBeFormed(settings):
	numberOfJewels = randint(1, settings.jewelsLimit)
	print(numberOfJewels)
	return numberOfJewels

'''
-- This function is responsible for the downward movement of the jewel. Update is the method in the respective jewel class.
If we write jewels.update(), then the update method is applied on each and every jewel in the jewels group.
'''
def forwardJewels(settings, jewels, jewelType):
	# if settings.jewelVerticalOrHorizontal == 1:
	# 	jewels.update()
	# else:
	# 	for jewel in jewels.sprites():
	# 		jewel.rect.y += 2
	jewels.update()

#########

def moveJewels(settings, screen, jewels):
	didJewelGroupReachedBottom = checkIfTheJewelGroupReachedBottom(jewels)
	if not didJewelGroupReachedBottom:
		screenRect = screen.get_rect()
		anyJewelAtTheEdge = anyJewelReachedEdge(settings, screen, jewels)
		isMovingRightOrLeft = settings.jewelMovingRight or settings.jewelMovingLeft

		for jewel in jewels.sprites():
			if isMovingRightOrLeft and (not anyJewelAtTheEdge):
				jewel.rect.x += (3 * settings.jewelDirection)

				
############	

def anyJewelReachedEdge(settings, screen, jewels):
	screenRect = screen.get_rect()
	returnValue = False
	for jewel in jewels.sprites():
		if jewel.rect.right >= screenRect.right:
			if settings.jewelDirection != -1:
				returnValue = True
				break

		elif jewel.rect.left <= 0:
			if settings.jewelDirection != 1:
				returnValue = True
				break

	return returnValue


def checkIfTheJewelGroupReachedBottom(jewels):
	for jewel in jewels.sprites():
		if jewel.settings.anyJewelReachedBottom:
			return True


def groupTheBottomReachedJewelsIntoOne(jewels, settings):
	for jewel in jewels.sprites():
		settings.bottomReachedJewelsAsaGroup.add(jewel)
	jewels.empty()
	
			

########################### SCREEN UPDATES ####################################################

def updateScreen(settings, screen, jewelType, jewels):
	screen.fill(settings.backgroundColor)
	if jewelType == 1:
		for rectangle in jewels.sprites():
			rectangle.blitme()
	pygame.time.delay(100)
	pygame.display.flip()
	# if not checkIfTheJewelGroupReachedBottom(jewels):
	# 	screen.fill(settings.backgroundColor)
	# 	if jewelType == 1:
	# 		for rectangle in jewels.sprites():
	# 			rectangle.blitme()
	# 	pygame.time.delay(100)
	# else:
	# 	groupTheBottomReachedJewelsIntoOne(jewels, settings)

	# pygame.display.flip()



