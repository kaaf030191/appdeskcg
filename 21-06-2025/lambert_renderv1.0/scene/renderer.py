
from .light import setup_light
from .mesh import SurfaceMesh

class Renderer:
    def __init__(self):
        setup_light()
        self.mesh = SurfaceMesh()

    def draw(self):
        self.mesh.draw()
