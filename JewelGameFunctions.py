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
	settings.numberOfJewels = 0
	del settings.listOfJewels[:]



######################################## KEY EVENTS ###########################################

def checkEvents(settings, screen, jewels, currentJewelsGroup):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		elif event.type == pygame.KEYDOWN:
			keyDownEvents(settings, screen, event, jewels, currentJewelsGroup)

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
def keyDownEvents(settings, screen, event, jewels, currentJewelsGroup):
	if event.key == pygame.K_RIGHT:
		settings.jewelMovingRight = True
		if settings.jewelDirection == -1:
			settings.jewelDirection = 1 

	elif event.key == pygame.K_LEFT:
		settings.jewelMovingLeft = True
		if settings.jewelDirection == 1:
			settings.jewelDirection = -1

	elif event.key == pygame.K_UP:
		up = 1
		changeTheJewelPositionsAfterTheJewelsFormed(settings, screen, currentJewelsGroup, up)


	elif event.key == pygame.K_DOWN:
		down = 0
		changeTheJewelPositionsAfterTheJewelsFormed(settings, screen, currentJewelsGroup, down)


	



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


def determineTheProbableXCoordinatesForTheNewlyFormedJewels(settings):
	numberOfSegments = determineTheNumberOfSegmentsThatScreenCanBeDividedInto(settings)
	AcceptableXCoordinates = []
	for number in range(numberOfSegments):
		AcceptableXCoordinates.append((number * settings.jewelWidth))

	return AcceptableXCoordinates


def determineTheXCoordinateOfTheNewlyFormedJewel(settings):
	AcceptableXCoordinates = determineTheProbableXCoordinatesForTheNewlyFormedJewels(settings)
	numberOfSegments = determineTheNumberOfSegmentsThatScreenCanBeDividedInto(settings)
	indexOfTheXCoordinate = randint(0, numberOfSegments - 1)
	xCoordinate = AcceptableXCoordinates[indexOfTheXCoordinate]

	return xCoordinate


############################################
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
	checkEvents(settings, screen, jewels, currentJewelsGroup) # Checks for any key press or release events
	forwardJewels(settings, jewels, jewelType, currentJewelsGroup) # move the jewels in the downward direction
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
	xCoordinate = determineTheXCoordinateOfTheNewlyFormedJewel(settings)
	
	for number in range(numberOfJewels):
		rectangle = Rectangle(screen, settings)
		if number == 0:
			rectangle.rect.y = yCoordinate
		else:
			# We add '+1' to create some space between jewels so as to create a boundary between jewels
			# rectangle.rect.y = (number * rectangle.height) + (2 * number) 
			rectangle.rect.y = (number * rectangle.height)
		rectangle.rect.x = xCoordinate
		settings.jewels.add(rectangle)
		settings.listOfJewels.append(rectangle)


############################################
def createHorizontallyAlignedJewels(settings, screen, jewelType, jewels):
	numberOfJewels = fixTheNumberOfJewelsToBeFormed(settings)
	settings.numberOfJewels = numberOfJewels
	xCoordinate = determineTheXCoordinateOfTheNewlyFormedJewel(settings)
	for number in range(numberOfJewels):
		rectangle = Rectangle(screen, settings)
		if number == 0:
			rectangle.rect.x = xCoordinate 
		else:
			# We add '(2 * number)' to create some space between jewels so as to create a boundary between jewels
			#rectangle.rect.x = xCoordinate + (number * rectangle.width) + (2 * number)
			rectangle.rect.x = xCoordinate + (number * rectangle.width)

		settings.jewels.add(rectangle)
		settings.listOfJewels.append(rectangle)


############################################
def fixTheNumberOfJewelsToBeFormed(settings):
	numberOfJewels = randint(1, settings.jewelsLimit)
	return numberOfJewels


############################################
'''
-- This function is responsible for the downward movement of the jewel. Update is the method in the respective jewel class.
If we write jewels.update(), then the update method is applied on each and every jewel in the jewels group.
'''
def forwardJewels(settings, jewels, jewelType, currentJewelsGroup):
	changeTheSettingsOfTheJewelsIfCollided(settings, currentJewelsGroup)

	for jewel in settings.jewels.sprites():
		if jewel.moveDown and not jewel.reachedBottom:
			if settings.anyJewelReachedBottom and settings.jewelVerticalOrHorizontal == 0:
				break
			else:
				jewel.update()



############################################
def changeTheSettingsOfTheJewelsIfCollided(settings, currentJewelsGroup):
	collidedJewels = checkForTheCollisionsBetweenJewels(settings.jewels, currentJewelsGroup)
	if len(collidedJewels) != 0: # If a collision happened, then both jewels would be copied as a key pair into collided Jewels dictionary
		
		if settings.jewelVerticalOrHorizontal == 0: # if they are aligned vertically
			settings.anyJewelReachedBottom = True
			setVerticallyAlignedJewelsReachedBottomToTrue(settings.jewels)
		else:
			for movingJewel, stationaryJewel in collidedJewels.items():
				movingJewel.moveDown = False
				movingJewel.reachedBottom = True




############################################
'''
-- This function is used to change the positions of the jewels when UP arrow key is pressed.
-- 
'''
def changeTheJewelPositionsAfterTheJewelsFormed(settings, screen, currentJewelsGroup, upOrDown):

	if upOrDown == 1:
		changeTheJewelPositionsWhenUpArrowKeyPressed(settings, screen, currentJewelsGroup)

	if upOrDown == 0:
		changeTheJewelPositionsWhenDownArrowKeyPressed(settings, screen, currentJewelsGroup)
	

############################################
'''
-- If the up arrow key pressed, then change the positions of the jewels in the clockwise direction. In other words, jewel at 
index 1 should be move to index 0, index 2 to index 1, index 3 to index 2 ......index 0 to index n - 1

-- 'n' being number of jewels in the list
'''

def changeTheJewelPositionsWhenUpArrowKeyPressed(settings, screen, currentJewelsGroup):
	numberOfJewels = len(settings.listOfJewels)
	jewels = settings.listOfJewels

	indexOneRectangleshape = jewels[0].shape
	colorOfTheJewelInRGB = jewels[0].jewelColor
	screenOfTheIndexOneJewel = jewels[0].screen
	for index in range(1, numberOfJewels):
		screen = jewels[index].screen
		shape = jewels[index].shape
		colorValueInRGB = jewels[index].jewelColor
		drawTheShapeAtTheNewCoordinates(screen, jewels[index - 1], shape, colorValueInRGB)

	drawTheShapeAtTheNewCoordinates(screenOfTheIndexOneJewel, jewels[numberOfJewels - 1], indexOneRectangleshape, colorOfTheJewelInRGB)
	updateScreen(settings, screen, 1, settings.jewels, currentJewelsGroup)



############################################
'''
-- If the up arrow key pressed, then change the positions of the jewels in the clockwise direction. In other words, jewel at 
index n should be move to index n - 1, index n - 1 to index n - 2, index n - 2 to index n - 3 ......index n  to index 0

-- 'n' being number of jewels in the list
'''

def changeTheJewelPositionsWhenDownArrowKeyPressed(settings, screen, currentJewelsGroup):
	numberOfJewels = len(settings.listOfJewels)
	jewels = settings.listOfJewels

	lastRectangleshape = jewels[numberOfJewels - 1].shape
	colorOfThelastJewel = jewels[numberOfJewels - 1].jewelColor
	screenOfTheLastJewel = jewels[numberOfJewels - 1].screen
	for index, jewel in reversed(list(enumerate(jewels))):
		if index != numberOfJewels - 1:
			screen = jewels[index].screen
			shape = jewels[index].shape
			colorValueInRGB = jewels[index].jewelColor
			drawTheShapeAtTheNewCoordinates(screen, jewels[index + 1], shape, colorValueInRGB)

	drawTheShapeAtTheNewCoordinates(screenOfTheLastJewel, jewels[0], lastRectangleshape, colorOfThelastJewel)
	updateScreen(settings, screen, 1, settings.jewels, currentJewelsGroup)


def drawTheShapeAtTheNewCoordinates(screen, jewel, shapeOfTheJewel, colorOfTheJewelInRGB):
	if shapeOfTheJewel == "rectangle":
		jewel.jewelColor = colorOfTheJewelInRGB
		jewel.shape = shapeOfTheJewel
	


############################################
'''
-- If the jewels are vertically aligned and there are already some jewels at the bottom and had been added to the currenJewelsGroup.

-- Now, if one of the moving jewels collided with the stationary jewels at the bottom, then the movement of the jewels should be stopped.

-- Not only the movement of the collided jewel, since they all are vertically aligned, if the very bottom is stopped then the movement of
all the jewels above it should also be stopped.

-- Therefore, if the jewels are vertially aligned and if the bottom jewel reached bottom or collied with another stationary jewel, then
moveDown and reachedBottom attributes of all the jewels in that group are set to False and True respectively.
'''

def setVerticallyAlignedJewelsReachedBottomToTrue(jewels):
	for jewel in jewels.sprites():
		jewel.moveDown = False
		jewel.reachedBottom = True


############################################
def moveJewels(settings, screen, jewels):
	didJewelGroupReachedBottom = checkIfTheJewelGroupReachedBottom(settings)
	if not didJewelGroupReachedBottom:
		screenRect = screen.get_rect()
		anyJewelAtTheEdge = anyJewelReachedEdge(settings, screen, jewels)
		isMovingRightOrLeft = settings.jewelMovingRight or settings.jewelMovingLeft

		for jewel in jewels.sprites():
			if isMovingRightOrLeft and (not anyJewelAtTheEdge):
				jewel.rect.x += (settings.jewelWidth * settings.jewelDirection)

				

############################################
def anyJewelReachedEdge(settings, screen, jewels):
	screenRect = screen.get_rect()
	returnValue = False
	for jewel in jewels.sprites():
		if jewel.rect.right > screenRect.right - settings.jewelWidth:
			if settings.jewelDirection != -1:
				returnValue = True
				break

		elif jewel.rect.left < settings.jewelWidth:
			if settings.jewelDirection != 1:
				returnValue = True
				break

	return returnValue

############################################
def checkIfTheJewelGroupReachedBottom(settings):
	reachedBottom = False
	numberOfJewelsReachedBottomIfHorizontallyAligned = 0

	if settings.jewelVerticalOrHorizontal == 0:
		for jewel in settings.jewels.sprites():
			if jewel.reachedBottom:
				reachedBottom = True
				break

		return reachedBottom

	else:
		for jewel in settings.jewels.sprites():
			if jewel.reachedBottom:
				numberOfJewelsReachedBottomIfHorizontallyAligned += 1

		if len(settings.jewels) == numberOfJewelsReachedBottomIfHorizontallyAligned:
			reachedBottom = True
		
		return reachedBottom



############################################
def groupTheBottomReachedJewelsIntoOne(settings, currentJewelsGroup):
	for jewel in settings.jewels.sprites():
		currentJewelsGroup.add(jewel)



############################################
def checkForTheCollisionsBetweenJewels(jewels, currentJewelsGroup):
	collidedJewelsDictionary = pygame.sprite.groupcollide(jewels, currentJewelsGroup, False, False)
	#print(type(collidedJewelsDictionary))
	return collidedJewelsDictionary


############################################
def alignTheJewelsProperly(collidedJewels, settings):
	for movingJewel, stationaryJewel in collidedJewels.items():
		if movingJewel.x != stationaryJewel.x:
			if abs(movingJewel.rect.x - stationaryJewel.rect.x) <= settings.jewelWidth / 2:
				movingJewel.rect.x = stationaryJewel.rect.x
			else:
				if movingJewel.rect.x > stationaryJewel.rect.x:
					movingJewel.rect.x = stationaryJewel.rect.x + settings.jewelWidth
				else:
					movingJewel.rect.x = stationaryJewel.rect.x - settings.jewelWidth


def checkIfThereAreMoreThanThreeSameJewelsAreAlignedImmediatelyToEachOther(collidedJewels, settings, currentJewelsGroup):
	for movingJewel, stationaryJewel in collidedJewels.items():
		if movingJewel.jewelColor == stationaryJewel.jewelColor:



def checkForSameJewelsHorizontally(movingJewel, stationaryJewel, settings):
	print('')
	listOfCoordinates = []
	colorOfTheJewel = movingJewel.jewelColorInRGB
	startXCoordinateUp = movingJewel.rect.x
	startYCoordinateUp = movingJewel.rect.y

	startXCoordinateDown = stationaryJewel.rect.x
	startYCoordinateUpDown = stationaryJewel.rect.y

	colorAtTheNewRect = (0, 0, 0)

	while colorOfTheJewel == colorAtTheNewRect:
		listOfCoordinates.append((startXCoordinateUp + settings.jewelHeight))




def checkForSamejewelsVertically():
	print('')

			

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



############################################
def determineTheNumberOfSegmentsThatScreenCanBeDividedInto(settings):
	numberOfSegments = int((settings.screenWidth)  / settings.jewelWidth)
	return numberOfSegments	


			





