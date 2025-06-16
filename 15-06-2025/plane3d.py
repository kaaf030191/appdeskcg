"""
generar proceduralmente un terreno en 3D tipo malla basado en una función matemática (usar el ruido senoidal)

agrégale árboles
"""

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
import random

# Parámetros del terreno
terrain_size = 50
scale = 0.3
amplitude = 2.0
frequency = 0.3
angle = 0

# Lista de posiciones para árboles (generados aleatoriamente)
num_trees = 30
tree_positions = []

def height(x, z):
	"""Altura del terreno en base a sin/cos"""
	return math.sin(x * frequency) * math.cos(z * frequency) * amplitude

def generate_tree_positions():
	"""Genera coordenadas aleatorias para árboles"""
	for _ in range(num_trees):
		x = random.uniform(-terrain_size, terrain_size) * scale
		z = random.uniform(-terrain_size, terrain_size) * scale
		y = height(x, z)
		tree_positions.append((x, y, z))

def draw_tree(x, y, z):
	"""Dibuja un árbol en (x, y, z)"""
	glPushMatrix()
	glTranslatef(x, y, z)

	# Tronco
	glColor3f(0.5, 0.25, 0.1)
	glPushMatrix()
	glRotatef(-90, 1, 0, 0)
	quad = gluNewQuadric()
	gluCylinder(quad, 0.05, 0.05, 0.5, 8, 8)
	glPopMatrix()

	# Copa
	glColor3f(0.0, 0.6, 0.0)
	glTranslatef(0, 0.5, 0)
	glRotatef(-90, 1, 0, 0)
	glutSolidCone(0.2, 0.5, 8, 8)
	glPopMatrix()

def draw_terrain():
	"""Dibuja el terreno como malla"""
	glColor3f(0.3, 0.7, 0.3)
	for z in range(-terrain_size, terrain_size):
		glBegin(GL_LINE_STRIP)
		for x in range(-terrain_size, terrain_size):
			y1 = height(x * scale, z * scale)
			glVertex3f(x * scale, y1, z * scale)
			y2 = height(x * scale, (z + 1) * scale)
			glVertex3f(x * scale, y2, (z + 1) * scale)
		glEnd()

def init():
	glClearColor(0.5, 0.8, 1.0, 1.0)
	glEnable(GL_DEPTH_TEST)
	glEnable(GL_COLOR_MATERIAL)
	glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

def display():
	global angle
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()

	gluLookAt(10, 10, 20, 0, 0, 0, 0, 1, 0)
	glRotatef(angle, 0, 1, 0)

	draw_terrain()

	# Dibujar árboles
	for pos in tree_positions:
		draw_tree(*pos)

	glutSwapBuffers()
	angle += 0.2

def reshape(w, h):
	glViewport(0, 0, w, h)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(45.0, float(w) / float(h), 1.0, 100.0)
	glMatrixMode(GL_MODELVIEW)

def main():
	glutInit()
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
	glutInitWindowSize(800, 600)
	glutCreateWindow(b"Terreno 3D Procedural con Arboles")
	init()
	generate_tree_positions()
	glutDisplayFunc(display)
	glutIdleFunc(display)
	glutReshapeFunc(reshape)
	glutMainLoop()

if __name__ == "__main__":
	main()