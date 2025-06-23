"""
Trazar una línea de Bresenham básico teniendo los puntos (22,14) y (32,20). Mediante python con pyopengl.
"""

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Puntos inicial y final
x0, y0 = 0, 0
x1, y1 = 20000, 20560

def init():
	glClearColor(1, 1, 1, 1)  # Fondo blanco
	glColor3f(0, 0, 0)        # Color negro para la línea
	glPointSize(5)            # Tamaño de punto para mejor visibilidad
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluOrtho2D(0, 50, 0, 50)  # Coordenadas ortográficas 2D
	glMatrixMode(GL_MODELVIEW)

def bresenham_line(x0, y0, x1, y1):
	dx = abs(x1 - x0)
	dy = abs(y1 - y0)
	sx = 1 if x0 < x1 else -1
	sy = 1 if y0 < y1 else -1
	err = dx - dy

	while True:
		glBegin(GL_POINTS)
		glVertex2i(x0, y0)
		glEnd()

		if x0 == x1 and y0 == y1:
			break
		e2 = 2 * err
		if e2 > -dy:
			err -= dy
			x0 += sx
		if e2 < dx:
			err += dx
			y0 += sy

def display():
	glClear(GL_COLOR_BUFFER_BIT)
	bresenham_line(x0, y0, x1, y1)
	glFlush()

def main():
	glutInit()
	glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
	glutInitWindowSize(500, 500)
	glutInitWindowPosition(100, 100)
	glutCreateWindow(b"Bresenham Line (22,14) to (32,20)")
	init()
	glutDisplayFunc(display)
	glutMainLoop()

if __name__ == "__main__":
	main()