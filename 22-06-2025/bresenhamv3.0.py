"""
Trazar una línea de Bresenham básico teniendo los puntos (22,14) y (32,20). Mediante python con pyopengl.
"""

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

def bresenham_line(x0, y0, x1, y1):
	"""
	Implementación del algoritmo de Bresenham para trazar una línea.
	Retorna una lista de tuplas (x, y) que representan los píxeles de la línea.
	"""
	points = []
	dx = abs(x1 - x0)
	dy = abs(y1 - y0)
	sx = 1 if x0 < x1 else -1
	sy = 1 if y0 < y1 else -1
	err = dx - dy

	x, y = x0, y0

	while True:
		points.append((x, y))
		if x == x1 and y == y1:
			break
		e2 = 2 * err
		if e2 > -dy:
			err -= dy
			x += sx
		if e2 < dx:
			err += dx
			y += sy
	return points

def draw_points(points):
	"""
	Dibuja los puntos dados usando GL_POINTS.
	"""
	glPointSize(3.0)  # Tamaño de los puntos
	glBegin(GL_POINTS)
	for x, y in points:
		glVertex2f(x, y)
	glEnd()

def main():
	pygame.init()
	display = (800, 600)
	pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
	pygame.display.set_caption("Línea de Bresenham")

	# Configuración para una proyección 2D ortográfica
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	# Los píxeles irán de (0,0) a (800,600) en el espacio de la ventana
	gluOrtho2D(0, display[0], 0, display[1])
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()

	# Puntos de inicio y fin de la línea
	p1 = (22, 14)
	p2 = (32, 20)

	# Calcular los píxeles de la línea con Bresenham
	line_pixels = bresenham_line(p1[0], p1[1], p2[0], p2[1])

	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		glClear(GL_COLOR_BUFFER_BIT)
		glColor3f(1.0, 1.0, 1.0)  # Color blanco para la línea

		# Dibuja los puntos calculados por Bresenham
		draw_points(line_pixels)

		# Opcional: Dibuja los puntos inicial y final con un color diferente
		glColor3f(1.0, 0.0, 0.0) # Rojo
		glPointSize(5.0)
		glBegin(GL_POINTS)
		glVertex2f(p1[0], p1[1])
		glVertex2f(p2[0], p2[1])
		glEnd()

		pygame.display.flip()
		pygame.time.wait(10)

	pygame.quit()

if __name__ == "__main__":
	main()