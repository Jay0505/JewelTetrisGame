from pygame.sprite import Group

class Settings(object):
	"""docstring for Settings"""
	def __init__(self):
		super().__init__()
		self.jewels = Group()
		self.isFirstIteration = True
		self.screenWidth = 720
		self.screenHeight = 720
		self.backgroundColor = (250, 250, 250)

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
		self.allTheJewelsReachedBottom = False
 
		
		self.probableXCoordinates = []
		self.listOfJewels = []


		