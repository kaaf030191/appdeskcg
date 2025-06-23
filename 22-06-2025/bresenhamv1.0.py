"""
Trazar una línea de Bresenham básico teniendo los puntos (22,14) y (32,20). Mediante python con pyopengl.
"""

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Tamaño de la ventana
window_width = 640
window_height = 480

# Puntos de la línea (22,14) a (32,20)
x0, y0 = 22, 14
x1, y1 = 32, 20

def bresenham_line(x0, y0, x1, y1):
	"""Algoritmo de Bresenham para trazar una línea"""
	points = []

	dx = abs(x1 - x0)
	dy = abs(y1 - y0)
	sx = 1 if x0 < x1 else -1
	sy = 1 if y0 < y1 else -1
	err = dx - dy

	while True:
		points.append((x0, y0))
		if x0 == x1 and y0 == y1:
			break
		e2 = 2 * err
		if e2 > -dy:
			err -= dy
			x0 += sx
		if e2 < dx:
			err += dx
			y0 += sy

	return points

def draw():
	glClear(GL_COLOR_BUFFER_BIT)
	glColor3f(1.0, 1.0, 1.0)

	# Obtener puntos de la línea
	line_points = bresenham_line(x0, y0, x1, y1)

	glBegin(GL_POINTS)
	for x, y in line_points:
		# Normalizar a [-1, 1] para OpenGL
		nx = (x / (window_width / 2)) - 1
		ny = (y / (window_height / 2)) - 1
		glVertex2f(nx, ny)
	glEnd()

	glFlush()

def init():
	glClearColor(0.0, 0.0, 0.0, 1.0)  # Fondo negro
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluOrtho2D(-1.0, 1.0, -1.0, 1.0)  # Coordenadas normalizadas

def main():
	glutInit()
	glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
	glutInitWindowSize(window_width, window_height)
	glutCreateWindow(b"Linea de Bresenham - PyOpenGL")
	init()
	glutDisplayFunc(draw)
	glutMainLoop()

if __name__ == "__main__":
	main()