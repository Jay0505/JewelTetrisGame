class Collision(object):
	"""docstring for Collision"""
	def __init__(self):
		super(Collision, self).__init__()
		self.collisionDirection = " "
		self.incrementOrDecrement = 1 # 1 - Increment the value, -1 to decrement the value
		self.variableCoordinate = 0
		self.nonVariableCoordinate = 0
		self.boundaryValue = 0
		self.collisionSpeedFactor = 0

		
		