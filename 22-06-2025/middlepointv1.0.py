from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Parámetros de la circunferencia
radius = 10
x0, y0 = 0, 10

# Ventana
width, height = 500, 500

def init():
	glClearColor(1.0, 1.0, 1.0, 1.0)
	glColor3f(0.0, 0.0, 0.0)
	gluOrtho2D(-30, 30, -10, 40)  # Ajustado para ver toda la circunferencia

def draw_axes():
	glColor3f(0.7, 0.7, 0.7)
	glBegin(GL_LINES)
	# Eje X
	glVertex2f(-30, 0)
	glVertex2f(30, 0)
	# Eje Y
	glVertex2f(0, -10)
	glVertex2f(0, 40)
	glEnd()

def plot_point(x, y):
	glVertex2i(x, y)

def draw_circle_midpoint_octant():
	glColor3f(1.0, 0.0, 0.0)  # Rojo
	glBegin(GL_POINTS)

	x = 0
	y = radius
	p = 1 - radius

	while x <= y:
		# Dibujar solo puntos del primer octante (x positivo, y positivo)
		plot_point(x0 + x, y0 + y)

		x += 1
		if p < 0:
			p += 2 * x + 1
		else:
			y -= 1
			p += 2 * (x - y) + 1

	glEnd()

def display():
	glClear(GL_COLOR_BUFFER_BIT)
	draw_axes()
	draw_circle_midpoint_octant()
	glFlush()

glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(width, height)
glutInitWindowPosition(100, 100)
glutCreateWindow(b"Circunferencia - Primer Octante (Algoritmo Punto Medio)")
init()
glutDisplayFunc(display)
glutMainLoop()