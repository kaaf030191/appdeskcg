from OpenGL.GL import *

class Cube:
	def __init__(self):
		self.vertices = [
			[1, 1, -1], [1, -1, -1], [-1, -1, -1], [-1, 1, -1],
			[1, 1, 1], [1, -1, 1], [-1, -1, 1], [-1, 1, 1]
		]
		self.faces = [
			(0, 1, 2, 3), (3, 2, 6, 7),
			(7, 6, 5, 4), (4, 5, 1, 0),
			(0, 3, 7, 4), (1, 2, 6, 5)
		]
		self.normals = [
			(0, 0, -1), (0, -1, 0),
			(0, 0, 1), (0, 1, 0),
			(1, 0, 0), (-1, 0, 0)
		]

	def draw(self):
		glBegin(GL_QUADS)
		for i, face in enumerate(self.faces):
			glNormal3fv(self.normals[i])
			for vertex in face:
				glColor3f(0.6, 0.3 + i * 0.1, 0.8 - i * 0.1)
				glVertex3fv(self.vertices[vertex])
		glEnd()