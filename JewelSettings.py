from pygame.sprite import Group

class Settings(object):
	"""docstring for Settings"""
	def __init__(self):
		super().__init__()
		self.jewels = Group()
		self.isFirstIteration = True
		self.screenWidth = 600
		self.screenHeight = 600
		self.backgroundColor = (0, 0, 0)
		self.totalNumberOfImages = 7

		# Jewel settings
		self.jewelWidth = 30
		self.jewelHeight = 20
		self.jewelVerticalOrHorizontal = 1 # vertical = 0; Horizontal = 1
		self.colorOfJewels = 7
		self.jewelType = 1
		self.jewelSpeedFactor = self.jewelWidth
		self.jewelsLimit = 4
		self.jewelDirection = 1
		self.jewelMovingRight = False
		self.jewelMovingLeft = False
		self.anyJewelReachedEdge = False
		self.anyJewelReachedBottom = False
		self.numberOfJewelsInEachIteration = 0

		#self.bottomReachedJewelsAsaGroup = Group()
		self.probableXCoordinates = []
		self.listOfJewels = []


		