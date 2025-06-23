"""
Genera un código en python con PyOpenGL (Un ejemplo visual) donde se muestre 2 cubos que se solapan y donde el Z-buffer decide cuál se ve. "Aplica técnica de resterización Z-Buffer".
"""

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

# Configuración de la ventana
WIDTH, HEIGHT = 800, 600

# Ángulos de rotación
angle1, angle2 = 0, 0

def init():
	glEnable(GL_DEPTH_TEST)  # Habilita Z-Buffer
	glDepthFunc(GL_LESS)      # Fragmentos más cercanos ocultan los lejanos
	glClearColor(0.1, 0.1, 0.1, 1.0)
	glMatrixMode(GL_PROJECTION)
	gluPerspective(45, (WIDTH/HEIGHT), 0.1, 50.0)
	glMatrixMode(GL_MODELVIEW)

def draw_cube():
	vertices = [
		[ 1, -1, -1], [ 1,  1, -1], [-1,  1, -1], [-1, -1, -1],
		[ 1, -1,  1], [ 1,  1,  1], [-1,  1,  1], [-1, -1,  1]
	]
	
	edges = (
		(0,1), (1,2), (2,3), (3,0),
		(4,5), (5,6), (6,7), (7,4),
		(0,4), (1,5), (2,6), (3,7)
	)
	
	glBegin(GL_LINES)
	for edge in edges:
		for vertex in edge:
			glVertex3fv(vertices[vertex])
	glEnd()

def display():
	global angle1, angle2
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Limpia buffers
	
	# Cubo 1 (más cercano)
	glLoadIdentity()
	glTranslatef(-1.0, 0.0, -5.0)
	glRotatef(angle1, 1, 1, 1)
	glColor3f(0.8, 0.2, 0.2)  # Rojo
	draw_cube()
	
	# Cubo 2 (más lejano, solapado parcialmente)
	glLoadIdentity()
	glTranslatef(1.0, 0.0, -7.0)  # Mayor valor Z = más lejos
	glRotatef(angle2, -1, -1, 1)
	glColor3f(0.2, 0.6, 0.8)  # Azul
	draw_cube()
	
	glutSwapBuffers()
	angle1 = (angle1 + 0.5) % 360
	angle2 = (angle2 + 0.3) % 360

def main():
	glutInit()
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
	glutInitWindowSize(WIDTH, HEIGHT)
	glutCreateWindow(b"Cubos con Z-Buffer")
	glutDisplayFunc(display)
	glutIdleFunc(display)  # Animación continua
	init()
	glutMainLoop()

if __name__ == "__main__":
	main()