"""
Trazar una línea de Bresenham básico teniendo los puntos (22,14) y (32,20). Mediante python con pyopengl.
"""

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

def bresenham_line(x0, y0, x1, y1):
	"""Implementación del algoritmo de Bresenham para trazar líneas"""
	points = []
	dx = abs(x1 - x0)
	dy = abs(y1 - y0)
	steep = dy > dx
	
	if steep:
		x0, y0 = y0, x0
		x1, y1 = y1, x1
		dx, dy = dy, dx
	
	if x0 > x1:
		x0, x1 = x1, x0
		y0, y1 = y1, y0
	
	error = dx // 2
	y_step = 1 if y0 < y1 else -1
	y = y0
	
	for x in range(x0, x1 + 1):
		coord = (y, x) if steep else (x, y)
		points.append(coord)
		error -= dy
		if error < 0:
			y += y_step
			error += dx
	
	return points

def draw_line(points, color=(1.0, 1.0, 1.0)):
	"""Dibuja los puntos de la línea en OpenGL"""
	glColor3f(*color)
	glPointSize(3.0)
	glBegin(GL_POINTS)
	for x, y in points:
		# Escalamos las coordenadas para que sean visibles en la ventana
		glVertex2f(x * 0.05 - 1.5, y * 0.05 - 1.0)
	glEnd()

def main():
	pygame.init()
	display = (800, 600)
	pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
	pygame.display.set_caption("Algoritmo de Bresenham - Línea (22,14) a (32,20)")
	
	gluOrtho2D(-2, 2, -2, 2)
	
	# Puntos de inicio y fin
	x0, y0 = 22, 14
	x1, y1 = 32, 20
	
	# Calculamos los puntos de la línea
	line_points = bresenham_line(x0, y0, x1, y1)
	
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				return
		
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		
		# Dibujamos la línea
		draw_line(line_points)
		
		# Dibujamos los puntos inicial y final en rojo
		draw_line([(x0, y0), (x1, y1)], color=(1.0, 0.0, 0.0))
		
		pygame.display.flip()
		pygame.time.wait(100)

if __name__ == "__main__":
	main()