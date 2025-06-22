import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

def iniciar_luz():
	glEnable(GL_LIGHTING)
	glEnable(GL_LIGHT0)

	luz_direccion = [1.0, 0.0, 0.0, 0.0]  # Luz direccional desde la derecha
	luz_difusa = [1.0, 1.0, 1.0, 1.0]
	luz_ambiente = [0.2, 0.2, 0.2, 1.0]

	glLightfv(GL_LIGHT0, GL_POSITION, luz_direccion)
	glLightfv(GL_LIGHT0, GL_DIFFUSE, luz_difusa)
	glLightModelfv(GL_LIGHT_MODEL_AMBIENT, luz_ambiente)

	glEnable(GL_COLOR_MATERIAL)
	glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

def dibujar_cubo():
	vertices = [
		[1, 1, -1], [1, -1, -1], [-1, -1, -1], [-1, 1, -1],
		[1, 1, 1], [1, -1, 1], [-1, -1, 1], [-1, 1, 1]
	]
	caras = [
		(0, 1, 2, 3), (4, 5, 1, 0),
		(7, 6, 5, 4), (3, 2, 6, 7),
		(4, 0, 3, 7), (1, 5, 6, 2)
	]
	normales = [
		(0, 0, -1), (1, 0, 0), (0, 0, 1),
		(0, 0, -1), (0, 1, 0), (0, -1, 0)
	]

	glBegin(GL_QUADS)
	for i, cara in enumerate(caras):
		glNormal3fv(normales[i % len(normales)])
		glColor3f(0.6, 0.3 + i * 0.1, 0.8 - i * 0.1)
		for v in cara:
			glVertex3fv(vertices[v])
	glEnd()

def main():
	pygame.init()
	display = (800, 600)
	pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
	pygame.display.set_caption("Cubo Rotando con Iluminación")

	glClearColor(1, 1, 1, 1)  # Fondo blanco
	glEnable(GL_DEPTH_TEST)

	gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
	glTranslatef(0, 0, -7)

	iniciar_luz()

	rot_x, rot_y = 20, 30
	velocidad_x, velocidad_y = 0.3, 0.5

	ejecutando = True
	while ejecutando:
		for evento in pygame.event.get():
			if evento.type == QUIT:
				ejecutando = False
			elif evento.type == KEYDOWN:
				if evento.key == K_ESCAPE:
					ejecutando = False

		# Rotación automática
		rot_x += velocidad_x
		rot_y += velocidad_y

		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		glPushMatrix()
		glRotatef(rot_x, 1, 0, 0)
		glRotatef(rot_y, 0, 1, 0)
		dibujar_cubo()
		glPopMatrix()

		pygame.display.flip()
		pygame.time.wait(10)

	pygame.quit()

if __name__ == "__main__":
	main()