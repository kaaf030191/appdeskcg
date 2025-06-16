"""
generar proceduralmente un terreno en 3D tipo malla basado en una función matemática (usar el ruido senoidal)

agrégale árboles

qué es perlin?, de ser posible el caso, agrégalo a lo anterior

agregar rocas y animales

pero mantenlo en malla, además de que falta agregar aninales
"""

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from noise import pnoise2
import random

# Parámetros del terreno
terrain_size = 50
scale = 0.3
height_scale = 5.0
noise_scale = 0.1
angle = 0

# Cantidades
num_trees = 60
num_rocks = 30
num_animals = 10

tree_positions = []
rock_positions = []
animal_positions = []

def height(x, z):
	return pnoise2(x * noise_scale, z * noise_scale, octaves=4) * height_scale

def generate_positions():
	for _ in range(num_trees):
		x = random.uniform(-terrain_size, terrain_size) * scale
		z = random.uniform(-terrain_size, terrain_size) * scale
		y = height(x, z)
		tree_positions.append((x, y, z))

	for _ in range(num_rocks):
		x = random.uniform(-terrain_size, terrain_size) * scale
		z = random.uniform(-terrain_size, terrain_size) * scale
		y = height(x, z)
		rock_positions.append((x, y, z))

	for _ in range(num_animals):
		x = random.uniform(-terrain_size, terrain_size) * scale
		z = random.uniform(-terrain_size, terrain_size) * scale
		y = height(x, z)
		animal_positions.append((x, y, z))

# Dibujo de elementos
def draw_terrain():
	glColor3f(0.5, 0.9, 0.5)
	for z in range(-terrain_size, terrain_size):
		glBegin(GL_LINE_STRIP)
		for x in range(-terrain_size, terrain_size):
			y = height(x * scale, z * scale)
			glVertex3f(x * scale, y, z * scale)
			y2 = height(x * scale, (z+1) * scale)
			glVertex3f(x * scale, y2, (z+1) * scale)
		glEnd()

def draw_tree(x, y, z):
	glPushMatrix()
	glTranslatef(x, y, z)

	# Tronco
	glColor3f(0.6, 0.3, 0.1)
	glPushMatrix()
	glRotatef(-90, 1, 0, 0)
	glutWireCylinder(0.03, 0.4, 6, 6)
	glPopMatrix()

	# Copa
	glColor3f(0.0, 0.6, 0.0)
	glTranslatef(0, 0.4, 0)
	glRotatef(-90, 1, 0, 0)
	glutWireCone(0.15, 0.4, 6, 6)

	glPopMatrix()

def draw_rock(x, y, z):
	glPushMatrix()
	glColor3f(0.5, 0.5, 0.5)
	glTranslatef(x, y + 0.1, z)
	glScalef(0.2, 0.1, 0.2)
	glutWireSphere(1, 8, 8)
	glPopMatrix()

def draw_animal(x, y, z):
	glPushMatrix()
	glColor3f(1.0, 0.6, 0.2)  # naranja
	glTranslatef(x, y + 0.1, z)
	glScalef(0.15, 0.15, 0.3)
	glutWireSphere(1, 10, 10)
	glPopMatrix()

# OpenGL básico
def init():
	glClearColor(0.6, 0.85, 1.0, 1.0)
	glEnable(GL_DEPTH_TEST)

def display():
	global angle
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()
	gluLookAt(10, 10, 20, 0, 0, 0, 0, 1, 0)
	glRotatef(angle, 0, 1, 0)

	# Elementos
	draw_terrain()
	for pos in tree_positions:
		draw_tree(*pos)
	for pos in rock_positions:
		draw_rock(*pos)
	for pos in animal_positions:
		draw_animal(*pos)

	glutSwapBuffers()
	angle += 0.2

def reshape(w, h):
	glViewport(0, 0, w, h)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(45.0, float(w)/float(h), 1.0, 100.0)
	glMatrixMode(GL_MODELVIEW)

def main():
	glutInit()
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
	glutInitWindowSize(800, 600)
	glutCreateWindow(b"Terreno Procedural - Wireframe + Arboles + Rocas + Animales")
	init()
	generate_positions()
	glutDisplayFunc(display)
	glutIdleFunc(display)
	glutReshapeFunc(reshape)
	glutMainLoop()

if __name__ == "__main__":
	main()