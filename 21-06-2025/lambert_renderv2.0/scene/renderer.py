from .light import setup_light
from .mesh import Cube

class Renderer:
	def __init__(self):
		setup_light()
		self.obj = Cube()

	def draw(self):
		self.obj.draw()