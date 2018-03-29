from pygame.sprite import Group

class Settings(object):
	"""docstring for Settings"""
	def __init__(self):
		super().__init__()
		self.jewels = Group()
		self.isFirstIteration = True
		self.screenWidth = 500
		self.screenHeight = 500
		self.backgroundColor = (120, 120, 120)

		# Jewel settings
		self.jewelVerticalOrHorizontal = 1 # vertical = 0; Horizontal = 1
		self.jewelType = 1
		self.jewelSpeedFactor = 1
		self.jewelsLimit = 4
		self.jewelDirection = 1
		self.jewelMovingRight = False
		self.jewelMovingLeft = False
		self.anyJewelReachedEdge = False
		self.anyJewelReachedBottom = False

		self.bottomReachedJewelsAsaGroup = Group()


		