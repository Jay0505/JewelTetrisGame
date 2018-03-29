import sys
import pygame

from pygame.sprite import Group
from random import randint
from rectangle import Rectangle


################################# Settings #################################################
'''
-- Whenever a jewelGroup reached bottom, we have to create a new jewelGroup without disturbing the earlier jewelGroup which
reached the bottom of the screen.

-- So, before creating a new jewelGroup, we reset the important settings which are responsible for the behaviour and creation
of the jewels.
'''
def resetAllTheSettings(settings):
	# Jewel settings
	settings.jewels.empty()
	settings.jewelVerticalOrHorizontal = 1 # vertical = 0; Horizontal = 1
	settings.jewelType = 1
	settings.jewelsLimit = 4
	settings.jewelDirection = 1
	settings.jewelMovingRight = False
	settings.jewelMovingLeft = False
	settings.anyJewelReachedEdge = False
	settings.anyJewelReachedBottom = False



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


def determineJewelType(settings):
	settings.jewelType = randint(1, settings.jewelType)

	
############################################
def determineVerticallyOrHorizontallyAlignedJewels(settings):
	settings.jewelVerticalOrHorizontal = randint(0, settings.jewelVerticalOrHorizontal)
	

############################################
def determineJewelTypeAlignmentAndThenCreateJewelGroup(settings, screen):

	determineJewelType(settings)
	determineVerticallyOrHorizontallyAlignedJewels(settings)
	createJewelGroup(settings, screen)

############################################
def funcResponsibleForMovementOfJewelsAndScreenUpdate(settings, currentJewelsGroup, screen):
	jewelType = settings.jewelType
	jewelVerticalOrHorizontal = settings.jewelVerticalOrHorizontal
	jewels = settings.jewels
	checkEvents(settings, screen, jewels) # Checks for any key press or release events
	forwardJewels(settings, jewels, jewelType) # move the jewels in the downward direction
	moveJewels(settings, screen, jewels) # move the jewels either right or left based upon the key pressed
	updateScreen(settings, screen, jewelType, jewels, currentJewelsGroup) # updates the screen with the latest positions of the jewels

############################################
def funcResponsibleForCreationAndMovementOfJewels(settings, currentJewelsGroup, screen):
	determineJewelTypeAlignmentAndThenCreateJewelGroup(settings, screen)
	funcResponsibleForMovementOfJewelsAndScreenUpdate(settings, currentJewelsGroup, screen)


############################################
def createJewelGroup(settings, screen):
	jewelType = settings.jewelType
	jewelVerticalOrHorizontal = settings.jewelVerticalOrHorizontal
	jewels = settings.jewels
	if jewelVerticalOrHorizontal == 1:
		createHorizontallyAlignedJewels(settings, screen, jewelType, jewels)
	else:
		settings.jewelVerticalOrHorizontal = 0
		createVerticallyAlignedJewels(settings, screen, jewelType, jewels)


############################################
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


############################################
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


############################################
def fixTheNumberOfJewelsToBeFormed(settings):
	numberOfJewels = randint(1, settings.jewelsLimit)
	return numberOfJewels


############################################
'''
-- This function is responsible for the downward movement of the jewel. Update is the method in the respective jewel class.
If we write jewels.update(), then the update method is applied on each and every jewel in the jewels group.
'''
def forwardJewels(settings, jewels, jewelType):
	jewels.update()


############################################
def moveJewels(settings, screen, jewels):
	didJewelGroupReachedBottom = checkIfTheJewelGroupReachedBottom(jewels)
	if not didJewelGroupReachedBottom:
		screenRect = screen.get_rect()
		anyJewelAtTheEdge = anyJewelReachedEdge(settings, screen, jewels)
		isMovingRightOrLeft = settings.jewelMovingRight or settings.jewelMovingLeft

		for jewel in jewels.sprites():
			if isMovingRightOrLeft and (not anyJewelAtTheEdge):
				jewel.rect.x += (3 * settings.jewelDirection)

				

############################################
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

############################################
def checkIfTheJewelGroupReachedBottom(jewels):
	for jewel in jewels.sprites():
		if jewel.settings.anyJewelReachedBottom:
			return True


############################################
def groupTheBottomReachedJewelsIntoOne(settings, currentJewelsGroup):
	for jewel in settings.jewels.sprites():
		currentJewelsGroup.add(jewel)
	
			

######################################################## SCREEN UPDATES ####################################################

'''
-- To give the notion of a free movement of jewels, after jewels making a movement (either downwards or sidewards) we fill the 
screen again with the background color.

-- During that time, jewels which were present earlier would be cleared and we would be offered a clear empty screen.

-- To prevent the game from this, after filling the screen with backgroud color, we blit (draw) the jewels in the jewelsGroup with 
the recent and updated co-ordinates using blit method

-- whenever a jewelGroup reached the bottom, they would be saved in the currentJewelsGroup present in NewValuesForNewJewels class

-- pygame.display.flip() method updates the screen with the recent updates.
'''

def updateScreen(settings, screen, jewelType, jewels, currentJewelsGroup):
	screen.fill(settings.backgroundColor)
	if jewelType == 1:
		for rectangle in jewels.sprites():
			rectangle.blitme()

		if len(currentJewelsGroup) != 0:
			for rectangle in currentJewelsGroup.sprites():
				rectangle.blitme()

	pygame.time.delay(100)
	pygame.display.flip()




