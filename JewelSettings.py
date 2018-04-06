from pygame.sprite import Group

class Settings(object):
	"""docstring for Settings"""
	def __init__(self):
		super().__init__()
		self.jewels = Group()
		self.isFirstIteration = True
		self.screenWidth = 480
		self.screenHeight = 480
		self.backgroundColor = (0, 0, 0)

		# Jewel settings
		self.jewelWidth = 30
		self.jewelHeight = 20
		self.jewelVerticalOrHorizontal = 1 # vertical = 0; Horizontal = 1
		self.colorOfJewels = 4
		self.jewelType = 1
		self.jewelSpeedFactor = 20
		self.jewelsLimit = 4
		self.jewelDirection = 1   # 1 - moving right i.e. value of x-coordinate should increase / -1 corresponds to moving left, therefore x should decrease
		self.jewelMovingRight = False
		self.jewelMovingLeft = False
		self.anyJewelReachedEdge = False
		self.anyJewelReachedBottom = False
		self.numberOfJewelsInEachIteration = 0
 
		
		self.probableXCoordinates = []
		self.listOfJewels = []


		