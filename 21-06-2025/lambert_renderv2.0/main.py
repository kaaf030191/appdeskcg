import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from scene.renderer import Renderer

def main():
	pygame.init()
	display = (800, 600)
	pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
	pygame.display.set_caption("Cubo con Iluminación Lambertiana")

	glClearColor(1, 1, 1, 1)
	glEnable(GL_DEPTH_TEST)
	glEnable(GL_LIGHTING)
	glShadeModel(GL_SMOOTH)

	glMatrixMode(GL_PROJECTION)
	gluPerspective(45, display[0]/display[1], 0.1, 100.0)
	glMatrixMode(GL_MODELVIEW)
	glTranslatef(0, 0, -7)

	renderer = Renderer()
	rot_x = rot_y = 0

	running = True
	while running:
		for e in pygame.event.get():
			if e.type == QUIT:
				running = False
			elif e.type == KEYDOWN:
				if e.key == K_ESCAPE:
					running = False
				elif e.key == K_LEFT:
					rot_y -= 5
				elif e.key == K_RIGHT:
					rot_y += 5
				elif e.key == K_UP:
					rot_x -= 5
				elif e.key == K_DOWN:
					rot_x += 5

		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		glPushMatrix()
		glRotatef(rot_x, 1, 0, 0)
		glRotatef(rot_y, 0, 1, 0)
		renderer.draw()
		glPopMatrix()
		pygame.display.flip()
		pygame.time.wait(10)

	pygame.quit()

if __name__ == "__main__":
	main()