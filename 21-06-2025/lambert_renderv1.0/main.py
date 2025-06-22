"""
Técnicas de renderización (modelo de iluminación: lambertiano) mediante python con pyopengl.

Genéralo con una estructura de archivos, sombras y demás.

Si, agrega lo que mencionas, además, empaqueta todo en un zip, para poder descargarlo y ejecutarlo.
"""

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from scene.renderer import Renderer

def main():
	pygame.init()
	display = (800, 600)
	pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
	pygame.display.set_caption("Iluminación Lambertiana - PyOpenGL")

	glClearColor(0.9, 0.9, 0.9, 1.0)
	glEnable(GL_DEPTH_TEST)
	glEnable(GL_LIGHTING)

	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(45, display[0]/display[1], 0.1, 100.0)

	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	glTranslatef(0, -2, -20)

	renderer = Renderer()

	rot_x, rot_y = 20, 30

	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				return
			elif event.type == KEYDOWN:
				if event.key == K_LEFT: rot_y -= 5
				if event.key == K_RIGHT: rot_y += 5
				if event.key == K_UP: rot_x -= 5
				if event.key == K_DOWN: rot_x += 5

		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

		glPushMatrix()
		glRotatef(rot_x, 1, 0, 0)
		glRotatef(rot_y, 0, 1, 0)
		renderer.draw()
		glPopMatrix()

		pygame.display.flip()
		pygame.time.wait(10)

if __name__ == "__main__":
	main()