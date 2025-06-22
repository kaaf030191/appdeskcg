from OpenGL.GL import *

def setup_light():
	glEnable(GL_LIGHT0)
	glLightfv(GL_LIGHT0, GL_POSITION, (1, 1, 1, 0))
	glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))

	glEnable(GL_LIGHT1)
	glLightfv(GL_LIGHT1, GL_POSITION, (-1, 1, -1, 0))
	glLightfv(GL_LIGHT1, GL_DIFFUSE, (0.5, 0.5, 0.7, 1))

	glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (0.2, 0.2, 0.2, 1))

	glEnable(GL_COLOR_MATERIAL)
	glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)