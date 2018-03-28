from JewelSettings import Settings
from pygame.sprite import Group


class CurrentIterationSettings(settings):
	"""docstring for CurrentIterationSettings"""
	def __init__(self):
		super().__init__()
		self.currentJewelType = Settings.jewelType
		self.currentJewelsGroup = 	Group()
		self.currentJewelVerticalOrHorizontal = Settings.jewelVerticalOrHorizontal