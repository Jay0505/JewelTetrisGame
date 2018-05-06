import sys
import pygame

from pygame.sprite import Group
from random import randint
from rectangle import Rectangle
from collisionVariables import Collision


################################# Settings #################################################
'''
-- Whenever a jewelGroup reached bottom, we have to create a new jewelGroup without disturbing the earlier jewelGroup which
reached the bottom of the screen.

-- So, before creating a new jewelGroup, we reset the important settings which are responsible for the behaviour and creation
of the jewels.
'''

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
	settings.numberOfJewels = 0
	del settings.listOfJewels[:]
	settings.count = 0




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
		#settings.jewelMovingLeft = False
		if settings.jewelDirection == -1:
			settings.jewelDirection = 1 

		determineRightOrLeftForEachJewel(settings)

	elif event.key == pygame.K_LEFT:
		settings.jewelMovingLeft = True
		#settings.jewelMovingRight = False
		if settings.jewelDirection == 1:
			settings.jewelDirection = -1

		determineRightOrLeftForEachJewel(settings)

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
	forwardJewels(settings, jewels, jewelType, currentJewelsGroup, screen) # move the jewels in the downward direction
	moveJewels(settings, screen, jewels, currentJewelsGroup) # move the jewels either right or left based upon the key pressed
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
	xCoordinate = determineTheXCoordinateOfTheNewlyFormedJewel(settings)
	# for number in range(numberOfJewels - 1, -1, -1):
	for number in range(numberOfJewels):
		rectangle = Rectangle(screen, settings)
		if number == 0:
			rectangle.rect.y = 0
		else:
			# We add '+1' to create some space between jewels so as to create a boundary between jewels
			# rectangle.rect.y = (number * rectangle.height) + (2 * number) 
			rectangle.rect.y = (number * rectangle.height)

		rectangle.myNumber = number
		rectangle.rect.x = xCoordinate
		settings.jewels.add(rectangle)
		settings.listOfJewels.append(rectangle)


############################################
def createHorizontallyAlignedJewels(settings, screen, jewelType, jewels):
	numberOfJewels = fixTheNumberOfJewelsToBeFormed(settings)
	settings.numberOfJewels = numberOfJewels
	yCoordinate = 0
	xCoordinate = determineTheXCoordinateOfTheNewlyFormedJewel(settings)
	for number in range(numberOfJewels):
		rectangle = Rectangle(screen, settings)
		if number == 0:
			rectangle.rect.x = xCoordinate 
		else:
			# We add '(2 * number)' to create some space between jewels so as to create a boundary between jewels
			#rectangle.rect.x = xCoordinate + (number * rectangle.width) + (2 * number)
			rectangle.rect.x = xCoordinate + (number * rectangle.width)
		rectangle.myNumber = number
		rectangle.rect.y = yCoordinate
		settings.jewels.add(rectangle)
		settings.listOfJewels.append(rectangle)



############################################
def fixTheNumberOfJewelsToBeFormed(settings):
	numberOfJewels = randint(1, settings.jewelsLimit)
	return numberOfJewels

############################################--------------------------------------------#####################################################

'''
-- This function is responsible for the downward movement of the jewel. Update is the method in the respective jewel class.
If we write jewels.update(), then the update method is applied on each and every jewel in the jewels group.
'''
def forwardJewels(settings, jewels, jewelType, currentJewelsGroup, screen):
	updateJewel(settings, currentJewelsGroup, screen)
	#if checkIfTheJewelGroupReachedBottom(settings):
		# print('before ' + str(len(settings.jewels)))
		# for jewel in settings.jewels.sprites():
		# 	checkIfThereAreThreeOrMoreSameJewelsAlignedImmediatelyNextToEachOtherLeftAndRight(jewel, settings, currentJewelsGroup, screen)

		# print('after ' + str(len(settings.jewels)))
		
	



############################################
def updateJewel(settings, currentJewelsGroup, screen):
	
	for jewel in settings.jewels.sprites():
		if jewel.moveDown and not jewel.reachedBottom:
			# if count == 0:
			# 	print('center ' + str(jewel.rect.center) + ' x ' + str(jewel.rect.x) + ' y ' + str(jewel.rect.y))
			jewel.update()
			checkCollisionOfEachJewelWithCurrentJewelsGroup(jewel, settings, currentJewelsGroup, screen)
			if len(settings.jewels) == 0:
				settings.allTheJewelsReachedBottom = True

'''
-- A collision between two entities is determined by comparing the rect attributes (xCoordinate and yCoordinate) of both the entities

-- In our case, two jewels are said to be collided if they both have same rect attributes. Now let us say, we have two jewels moving downwards
and the co-ordinates of those jewels are (100, 200), (100, 220) (height of each jewel is 20). Now, these two jewels are affixed to each other like
the jewels in our game which are affixed vertically when they are vertically aligned.

-- Let us suppose that, JewelA has co-ordinates (100, 200) and JewelB has co-ordinates (100, 220). let us say, we have a jewel which has already
reached bottom and stationed at the co-ordinates (100, 300) and lets call this jewel, JewelC

-- Now, we say, JewelB is collided with JewelC on when they both have same rect attributes. In other words, when the jewelA and JewelB are moving
downwards and when both JewelB and JewelC are perfectly interposed with each other. In this case, JewelB and JewelC - (100, 300) 
																											 JewelA - (100, 280)

-- But, in our game, when a jewel is collided with each other, the movement of the jewels should be stopped and ideally after a collision is detected,
the co-ordinates of the three jewels should be as following:
					JewelC - (100, 300)
					JewelB - (100, 280)
					JewelA - (100, 260) But, both JewelC and JewelB are interposed and JewelA is 20 steps (which is equal to height of the jewels) than
					it should be.

-- To rectify this error, the bottom of the moving Jewels is decremented by the speed factor (or height of the jewel, both are equal in our game). 
  			Before collision                        AfterCollision
  			JewelC - (100, 300)						JewelC - (100, 300)
													JewelB - (100, 300)
													JewelA - (100, 280)
			JewelB - (100, 220)
			JewelA - (100, 200)

		but after decrementing the bottom by the speed factor, the co-ordinates would be JewelC (100, 300), JewelB (100, 280) and JewelA (100, 260) 
		Thus creating the required effect (moving jewels immediately stopping when collided with any stationed jewel)
'''			

def checkCollisionOfEachJewelWithCurrentJewelsGroup(jewel, settings, currentJewelsGroup, screen): # Vertical Collisions
	collidedJewelsList = pygame.sprite.spritecollide(jewel, currentJewelsGroup, False)
	if len(collidedJewelsList) != 0:
		
		if settings.jewelVerticalOrHorizontal == 0:
			bottom = collidedJewelsList[0].rect.top
			changeTheSettingsOfTheJewelsCollidedWhenVerticallyAligned(settings, bottom)
		else:
			jewel.moveDown = False
			jewel.reachedBottom = True
			jewel.movingRight = False
			jewel.movingLeft = False
			#jewel.rect.bottom = collidedJewelsList[0].rect.top
			jewel.rect.bottom -= settings.jewelSpeedFactor
			jewel.blitme()

		checkIfThereAreThreeOrMoreSameJewelsAlignedImmediatelyNextToEachOtherUpAndDown(jewel, collidedJewelsList[0], settings, currentJewelsGroup, screen)
		#print('length of setting jewels ' + str(len(settings.jewels)))

			#currentJewelsGroup.add(jewel)
			#settings.jewels.remove(jewel)





def detectCollisionsBetweenJewelsWhenMovingSidewards(jewel, currentJewelsGroup):
	collidedJewelsList = pygame.sprite.spritecollide(jewel, currentJewelsGroup, False)
	return collidedJewelsList
	


def change_The_Settings_Of_Vertically_Aligned_Jewels_Collided_When_Moving_Sidewards(settings):
	for jewel in settings.jewels.sprites():
		if jewel.positionChanged:
			jewel.rect.x -= (settings.jewelDirection * settings.jewelWidth)


def change_The_Settings_Of_Horizontally_Aligned_Jewels_Collided_When_Moving_Sidewards(settings):
	
	for jewel in settings.jewels.sprites():
		if not jewel.reachedBottom:
			jewel.rect.x -= (settings.jewelDirection * settings.jewelWidth)


		
		


def changeTheSettingsOfTheJewelsCollidedWhenVerticallyAligned(settings, bottom):
	settings.anyJewelReachedBottom = True
	for jewel in settings.jewels.sprites():
		jewel.moveDown = False
		jewel.reachedBottom = True
		jewel.movingRight = False
		jewel.movingLeft = False
		jewel.rect.bottom -= settings.jewelSpeedFactor
		jewel.blitme()

		

############################################--------------------------------------------#####################################################
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
	




############################################--------------------------------------------#####################################################

def moveJewels(settings, screen, jewels, currentJewelsGroup):
	didJewelGroupReachedBottom = checkIfTheJewelGroupReachedBottom(settings)
	if not didJewelGroupReachedBottom:
		screenRect = screen.get_rect()
		anyJewelAtTheEdge = anyJewelReachedEdge(settings, screen, jewels)
		isMovingRightOrLeft = settings.jewelMovingRight or settings.jewelMovingLeft

		for jewel in settings.jewels.sprites():
			if isMovingRightOrLeft and (not anyJewelAtTheEdge) and (jewel.movingRight or jewel.movingLeft):
				jewel.rect.x += (settings.jewelWidth * settings.jewelDirection)
				jewel.positionChanged = True
				collidedJewelsList = detectCollisionsBetweenJewelsWhenMovingSidewards(jewel, currentJewelsGroup)
				if len(collidedJewelsList) != 0:
					if settings.jewelVerticalOrHorizontal == 0:
						change_The_Settings_Of_Vertically_Aligned_Jewels_Collided_When_Moving_Sidewards(settings)

					else:
						change_The_Settings_Of_Horizontally_Aligned_Jewels_Collided_When_Moving_Sidewards(settings)	
						


def determineRightOrLeftForEachJewel(settings):
	if settings.jewelDirection == 1:
		for jewel in settings.jewels.sprites():
			if not jewel.reachedBottom:
				jewel.movingRight = True
				jewel.movingLeft = False
	else:
		for jewel in settings.jewels.sprites():
			if not jewel.reachedBottom:
				jewel.movingLeft = True
				jewel.movingRight = False


def whenCollidedSetTheAppropriateRightOrLeftValuesForJewels(settings, collidedJewels):
	if len(collidedJewels) != 0:
		if settings.jewelVerticalOrHorizontal == 1: # if horizontally aligned
			if settings.jewelDirection == 1:
				for jewel in settings.jewels.sprites():
					jewel.movingRight = False
			else:
				for jewel in settings.jewels.sprites():
					jewel.movingLeft = False

		else:									    # If vertically aligned
			for movingJewel, stationaryJewels in collidedJewels.items():
				if movingJewel.movingRight:
					movingJewel.movingRight = False
				else:
					movingJewel.movingLeft = False
				

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

	if len(settings.jewels) != 0:
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

	else:
		if settings.allTheJewelsReachedBottom:
			return True



############################################
def groupTheBottomReachedJewelsIntoOne(settings, currentJewelsGroup):
	for jewel in settings.jewels.sprites():
		currentJewelsGroup.add(jewel)

	settings.jewels.empty()




##########################--------------------------------------------######################################################

def checkIfThereAreThreeOrMoreSameJewelsAlignedImmediatelyNextToEachOtherUpAndDown(movingJewel, stationaryJewel, settings, currentJewelsGroup, screen):
	
	movingJewelTupleList = []
	stationaryJewelTupleList = []
	up = "up"
	down = "down"
	
	#movingJewelCenter = movingJewel.rect.center
	movingJewelTupleList.append((movingJewel.rect.x, movingJewel.rect.y))
	
	listOfMatchedJewelsUp = checkIfThereAreThreeOrMoreMatchedJewels(movingJewel, settings, currentJewelsGroup, screen, up)
	listOfMatchedJewelsDown = checkIfThereAreThreeOrMoreMatchedJewels(movingJewel, settings, currentJewelsGroup, screen, down)
	

	if (len(listOfMatchedJewelsUp) != 0 or  len(listOfMatchedJewelsDown) != 0) and (len(listOfMatchedJewelsDown) + len(listOfMatchedJewelsUp) >= 2):
		
		removeAJewelFromTheGroupSpecifiedInTheList(listOfMatchedJewelsUp, settings.jewels)
		removeAJewelFromTheGroupSpecifiedInTheList(listOfMatchedJewelsDown, currentJewelsGroup)


		removeAJewelFromTheGroupSpecifiedInTheList(movingJewelTupleList, settings.jewels)


def checkIfThereAreThreeOrMoreSameJewelsAlignedImmediatelyNextToEachOtherLeftAndRight(movingJewel, settings, currentJewelsGroup, screen):
	right = "right"
	left = "left"

	movingJewelTupleList = []
	movingJewelTupleList.append((movingJewel.rect.x, movingJewel.rect.y))

	listOfMatchedJewelsLeft = checkIfThereAreThreeOrMoreMatchedJewels(movingJewel, settings, currentJewelsGroup, screen, left)
	listOfMatchedJewelsRight = checkIfThereAreThreeOrMoreMatchedJewels(movingJewel, settings, currentJewelsGroup, screen, right)

	if (len(listOfMatchedJewelsLeft) != 0 or  len(listOfMatchedJewelsRight) != 0) and (len(listOfMatchedJewelsLeft) + len(listOfMatchedJewelsRight) >= 2):
		removeAJewelFromTheGroupSpecifiedInTheListLeftOrRight(listOfMatchedJewelsLeft, settings.jewels, currentJewelsGroup)
		removeAJewelFromTheGroupSpecifiedInTheListLeftOrRight(listOfMatchedJewelsRight, settings.jewels, currentJewelsGroup)


		removeAJewelFromTheGroupSpecifiedInTheList(movingJewelTupleList, settings.jewels)


def checkIfThereAreThreeOrMoreMatchedJewels(movingJewel, settings, currentJewelsGroup, screen, direction):

	collisionVariables = Collision()
	listOfCoordinates = []
	setTheCollisionDirectionValue(collisionVariables, direction)
	setTheValuesForVariableAndNonVariableCoordinates(collisionVariables, movingJewel)
	setTheIncrementOrDecrementValueForCollisionClass(collisionVariables)
	setTheCollisionSpeedFactor(collisionVariables, settings)
	setTheBoundaryValue(collisionVariables, screen)

	if collisionVariables.collisionDirection == "left":
		listOfCoordinates = checkForTheSameJewelsUpOrLeft(collisionVariables, movingJewel, settings, currentJewelsGroup, screen)

	elif collisionVariables.collisionDirection == "right":
		listOfCoordinates =  checkForTheSameJewelsDownOrRight(collisionVariables, movingJewel, settings, currentJewelsGroup, screen)

	elif collisionVariables.collisionDirection == "up":
		listOfCoordinates =  checkForTheSameJewelsUpOrLeft(collisionVariables, movingJewel, settings, currentJewelsGroup, screen)

	elif collisionVariables.collisionDirection == "down":
		listOfCoordinates =  checkForTheSameJewelsDownOrRight(collisionVariables, movingJewel, settings, currentJewelsGroup, screen)

	return listOfCoordinates


############################################
def setTheCollisionDirectionValue(collisionVariables, direction):
	if direction == "left":
		collisionVariables.collisionDirection = "left"
	elif direction == "right":
		collisionVariables.collisionDirection = "right"
	elif direction == "up":
		collisionVariables.collisionDirection = "up"
	elif direction == "down":
		collisionVariables.collisionDirection = "down"


			
############################################
def setTheValuesForVariableAndNonVariableCoordinates(collisionVariables, movingJewel):
	startXCoordinate = movingJewel.rect.x
	startYCoordinate = movingJewel.rect.y

	if collisionVariables.collisionDirection == "left" or collisionVariables.collisionDirection == "right":
		collisionVariables.variableCoordinate = startXCoordinate
		collisionVariables.nonVariableCoordinate = startYCoordinate


	elif collisionVariables.collisionDirection == "up" or collisionVariables.collisionDirection == "down":
		collisionVariables.variableCoordinate = startYCoordinate
		collisionVariables.nonVariableCoordinate = startXCoordinate



############################################
def setTheIncrementOrDecrementValueForCollisionClass(collisionVariables):
	if collisionVariables.collisionDirection == "left" or collisionVariables.collisionDirection == "up":
		collisionVariables.incrementOrDecrement = -1

	if collisionVariables.collisionDirection == "right" or collisionVariables.collisionDirection == "down":
		collisionVariables.incrementOrDecrement = 1


############################################
def setTheCollisionSpeedFactor(collisionVariables, settings):
	if collisionVariables.collisionDirection == "left" or collisionVariables.collisionDirection == "right":
		collisionVariables.collisionSpeedFactor = settings.jewelWidth

	if collisionVariables.collisionDirection == "up" or collisionVariables.collisionDirection == "down":
		collisionVariables.collisionSpeedFactor = settings.jewelHeight


############################################
def setTheBoundaryValue(collisionVariables, screen):
	screenRect = screen.get_rect()

	if collisionVariables.collisionDirection == "left" or collisionVariables.collisionDirection == "up":
		collisionVariables.boundaryValue = screenRect.top

	if collisionVariables.collisionDirection == "right" or collisionVariables.collisionDirection == "down":
		collisionVariables.boundaryValue = screenRect.right

	

############################################
def addTheValuesToTheListAsATuple(listOfCoordinates, valueAtTheIndexZero, valueAtTheIndexOne):
	listOfCoordinates.append((valueAtTheIndexZero, valueAtTheIndexOne))
	return listOfCoordinates

def getColorAtParticularCoordinatesUpOrDown(screen, xCoordinate, yCoordinate, jewels):
	colorOfTheJewel = getTheColorOfTheJewel(screen, xCoordinate, yCoordinate, jewels)
	return colorOfTheJewel

def getColorAtParticularCoordinatesRightOrLeft(screen, xCoordinate, yCoordinate, currentJewelsGroup, movingJewelsGroup):
	'''
	First search for the jewel in moving jewels group. If found, it returns the color of the jewel. If not found, it return "Black"
	then search for the jewel in current jewels group
	'''

	colorOfTheJewel = getTheColorOfTheJewel(screen, xCoordinate, yCoordinate, movingJewelsGroup)
	if colorOfTheJewel == "Black":
		colorOfTheJewel = getTheColorOfTheJewel(screen, xCoordinate, yCoordinate, currentJewelsGroup)

	return colorOfTheJewel

def getTheColorOfTheJewel(screen, xCoordinate, yCoordinate, jewels):
	found = False
	for jewel in jewels.sprites():
		if jewel.rect.x == xCoordinate and jewel.rect.y == yCoordinate:
			found = True
			return jewel.jewelName

	if not found:
		return "Black"

	


############################################
def checkForTheSameJewelsUpOrLeft(collisionVariables, movingJewel, settings, currentJewelsGroup, screen):
	
	listOfCoordinatesOfJewelsMatched = []
	variableCoordinate = collisionVariables.variableCoordinate - collisionVariables.collisionSpeedFactor
	nonVariableCoordinate = collisionVariables.nonVariableCoordinate
	colorOfTheJewel = movingJewel.jewelName


	while variableCoordinate >= collisionVariables.boundaryValue:

		colorAtTheNewRect = ()
		tempCoordinate = variableCoordinate

		if collisionVariables.collisionDirection == "left":
			colorAtTheNewRect = getColorAtParticularCoordinatesRightOrLeft(screen, tempCoordinate, nonVariableCoordinate, currentJewelsGroup, settings.jewels)
		if collisionVariables.collisionDirection == "up":
			colorAtTheNewRect = getColorAtParticularCoordinatesUpOrDown(screen, nonVariableCoordinate, tempCoordinate, settings.jewels)

		
		variableCoordinate -= collisionVariables.collisionSpeedFactor
		if colorOfTheJewel == colorAtTheNewRect:
			
			if collisionVariables.collisionDirection == "left":
				listOfCoordinatesOfJewelsMatched.append((tempCoordinate, nonVariableCoordinate))
			elif collisionVariables.collisionDirection == "up":
				listOfCoordinatesOfJewelsMatched.append((nonVariableCoordinate, tempCoordinate))

		else:
			break

	return listOfCoordinatesOfJewelsMatched


############################################
def checkForTheSameJewelsDownOrRight(collisionVariables, movingJewel, settings, currentJewelsGroup, screen):
	
	listOfCoordinatesOfJewelsMatched = []
	variableCoordinate = collisionVariables.variableCoordinate + collisionVariables.collisionSpeedFactor
	nonVariableCoordinate = collisionVariables.nonVariableCoordinate
	colorOfTheJewel = movingJewel.jewelName

	while variableCoordinate < collisionVariables.boundaryValue:
	
		tempCoordinate = variableCoordinate
		colorAtTheNewRect = ()
		trimmedColorAtTheNewRect = ()
		if collisionVariables.collisionDirection == "right":
			colorAtTheNewRect = getColorAtParticularCoordinatesRightOrLeft(screen, tempCoordinate, nonVariableCoordinate, currentJewelsGroup, settings.jewels)
		if collisionVariables.collisionDirection == "down":
			colorAtTheNewRect = getColorAtParticularCoordinatesUpOrDown(screen, nonVariableCoordinate, tempCoordinate, currentJewelsGroup)
		
		
		variableCoordinate += collisionVariables.collisionSpeedFactor
		if colorOfTheJewel == colorAtTheNewRect:
		
			if collisionVariables.collisionDirection == "right":
				listOfCoordinatesOfJewelsMatched.append((tempCoordinate, nonVariableCoordinate))
			elif collisionVariables.collisionDirection == "down":
				listOfCoordinatesOfJewelsMatched.append((nonVariableCoordinate, tempCoordinate))

		else:
			break

	return listOfCoordinatesOfJewelsMatched


	

############################################
def removeAJewelFromTheGroupSpecifiedInTheListUpOrDown(listOfCoordinates, jewels):
	removeAJewelFromTheGroupSpecifiedInTheList(listOfCoordinates, jewels)

def removeAJewelFromTheGroupSpecifiedInTheListLeftOrRight(listOfCoordinates, movingJewelsGroup, currentJewelsGroup):
	IsJewelRemoved = removeAJewelFromTheGroupSpecifiedInTheList(listOfCoordinates, movingJewelsGroup)
	if not IsJewelRemoved:
		removeAJewelFromTheGroupSpecifiedInTheList(listOfCoordinates, currentJewelsGroup)


def removeAJewelFromTheGroupSpecifiedInTheList(listOfCoordinates, jewels):
	removed = False
	if len(listOfCoordinates) != 0:
		for xyTuple in listOfCoordinates:
			removed = getTheJewelAtAParticularCoordinates(xyTuple[0], xyTuple[1], jewels)

	return removed


############################################
def getTheJewelAtAParticularCoordinates(Xcoordinate, Ycoordinate, jewels):
	found = False
	for jewel in jewels.sprites():
		if jewel.rect.x == Xcoordinate and jewel.rect.y == Ycoordinate:
			jewels.remove(jewel)
			found = True
			return found

	if not found:
		return False

############################################
def trimTheRGBColorValue(RGBColorTuple):
	return setTheColorValue((RGBColorTuple[0], RGBColorTuple[1], RGBColorTuple[2]))
			

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
		if len(settings.jewels) != 0:
			for rectangle in jewels.sprites():
				rectangle.blitme()

		if len(currentJewelsGroup) != 0:
			for rectangle in currentJewelsGroup.sprites():
				rectangle.blitme()

	pygame.time.delay(150)
	pygame.display.flip()

def moveJewelsDownIfAfterTheRemovalOfMatchedJewels(currentJewelsGroup, settings, screen):
	nextPositionEmptyJewel = findTheJewelWhoseNextPositionIsEmptyDownwards(currentJewelsGroup, screen, settings)

	moveJewels = Group()
	if nextPositionEmptyJewel != -1:
		xCoordinate = nextPositionEmptyJewel.rect.x
		yCoordinate = nextPositionEmptyJewel.rect.y
		moveJewels = findTheJewelsThatHasToBeMovedDownAfterACollision(moveJewels, nextPositionEmptyJewel, screen, settings, currentJewelsGroup)
		lastYCoordinateWhereThereIsAnEmptyRect = findTheYCoordinateAtWhichTheRectIsEmpty(xCoordinate, yCoordinate, screen)
		differenceBetweenYCoordinates = lastYCoordinateWhereThereIsAnEmptyRect - yCoordinate

		for jewel in moveJewels.sprites():
			jewel.rect.y = differenceBetweenYCoordinates + jewel.rect.y

		
def findTheJewelWhoseNextPositionIsEmptyDownwards(currentJewelsGroup, screen, settings):
	FoundAnyJewel = False
	for jewel in currentJewelsGroup.sprites():
		if jewel.rect.y + settings.jewelSpeedFactor < screen.get_rect().right:
			colorOfTheNextJewel = screen.get_at((jewel.rect.x, jewel.rect.y + settings.jewelSpeedFactor))
			if colorOfTheNextJewel == settings.colorOfTheEmptyRect:
				FoundAnyJewel = True
				return jewel

	if not FoundAnyJewel:
		return -1

def findTheJewelsThatHasToBeMovedDownAfterACollision(moveJewels, nextPositionEmptyJewel, screen, settings, currentJewelsGroup):
	xCoordinate = nextPositionEmptyJewel.rect.x
	yCoordinate = nextPositionEmptyJewel.rect.y - settings.jewelSpeedFactor

	moveJewels.add(nextPositionEmptyJewel)
	while xCoordinate >= screen.get_rect().top and yCoordinate >= screen.get_rect().top:
		colorAtTheNewRect = screen.get_at((xCoordinate, yCoordinate))

		if colorAtTheNewRect != settings.colorOfTheEmptyRect:
			jewel = returnJewelAtParticularPosition(xCoordinate, yCoordinate, currentJewelsGroup)
			print('jewel x ' + str(jewel.rect.x) + ' y - ' + str(jewel.rect.y))
			moveJewels.add(jewel)

		yCoordinate -= settings.jewelSpeedFactor

	print('escaped 1')
	return moveJewels



def returnJewelAtParticularPosition(xCoordinate, yCoordinate, currentJewelsGroup):
	for jewel in currentJewelsGroup.sprites():
		if jewel.rect.x == xCoordinate and jewel.rect.y == yCoordinate:
			return jewel





def findTheYCoordinateAtWhichTheRectIsEmpty(xCoordinate, yCoordinate, screen):
	tempCoordinate = yCoordinate + 20
	color = "Black"
	while  color == "Black" and tempCoordinate < screen.get_rect().right:
		IsNextPositionWithinTheBoundary, colorInRGB = getTheColorOfTheNextPosition(xCoordinate, tempCoordinate, screen)
		if IsNextPositionWithinTheBoundary and colorInRGB == (250, 250, 250, 255):
			tempCoordinate += 20
		else:
			color = "NotBlack"

	print('escaped 2')
	return tempCoordinate - 20


def getTheColorOfTheNextPosition(xCoordinate, yCoordinate, screen):
	boundaryValue = screen.get_rect().right
	IsNextPositionWithinTheBoundary = True
	if xCoordinate  < boundaryValue and yCoordinate < boundaryValue:
		return IsNextPositionWithinTheBoundary, screen.get_at((xCoordinate, yCoordinate))

	else:
		IsNextPositionWithinTheBoundary = False
		return IsNextPositionWithinTheBoundary, (0, 0, 0, 0)


############################################
def determineTheNumberOfSegmentsThatScreenCanBeDividedInto(settings):
	numberOfSegments = int((settings.screenWidth)  / settings.jewelWidth)
	return numberOfSegments	


			





