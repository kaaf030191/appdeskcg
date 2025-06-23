"""
Genera un código en python con PyOpenGL (Un ejemplo visual) donde se muestre 2 cubos que se solapan y donde el Z-buffer decide cuál se ve. "Aplica técnica de resterización Z-Buffer".
"""

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

def draw_cube():
	# Define los vértices de un cubo
	vertices = (
		(1, 1, 1), (1, 1, -1), (1, -1, -1), (1, -1, 1),
		(-1, 1, 1), (-1, 1, -1), (-1, -1, -1), (-1, -1, 1)
	)

	# Define las aristas que conectan los vértices
	edges = (
		(0, 1), (0, 3), (0, 4), (1, 2), (1, 5), (2, 3),
		(2, 6), (3, 7), (4, 5), (4, 7), (5, 6), (6, 7)
	)

	# Define las caras para rellenar el cubo
	surfaces = (
		(0, 1, 2, 3),  # Cara frontal
		(4, 5, 6, 7),  # Cara trasera
		(0, 4, 7, 3),  # Cara derecha
		(1, 5, 6, 2),  # Cara izquierda
		(0, 1, 5, 4),  # Cara superior
		(3, 2, 6, 7)   # Cara inferior
	)

	glBegin(GL_QUADS)
	for surface in surfaces:
		for vertex in surface:
			glVertex3fv(vertices[vertex])
	glEnd()

def main():
	pygame.init()
	display = (800, 600)
	pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

	# Habilita el Z-buffer (depth testing)
	glEnable(GL_DEPTH_TEST)

	gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

	# Posiciona la cámara
	glTranslatef(0.0, 0.0, -10)

	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Limpia el búfer de color y el Z-buffer

		# --- Primer Cubo (Rojo) ---
		glPushMatrix() # Guarda la matriz actual
		glTranslatef(-1.0, 0.0, -1.0) # Posiciona el cubo rojo
		glColor3f(1.0, 0.0, 0.0) # Color rojo
		draw_cube()
		glPopMatrix() # Restaura la matriz anterior

		# --- Segundo Cubo (Azul) ---
		glPushMatrix() # Guarda la matriz actual
		glTranslatef(1.0, 0.0, 1.0) # Posiciona el cubo azul
		glColor3f(0.0, 0.0, 1.0) # Color azul
		draw_cube()
		glPopMatrix() # Restaura la matriz anterior

		pygame.display.flip()
		pygame.time.wait(10)

	pygame.quit()

if __name__ == "__main__":
	main()