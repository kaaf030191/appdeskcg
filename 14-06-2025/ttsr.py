"""
crear un triángulo en 2D cuyos vértices deben de estar en una matriz. mediante python con OpenGL.

agregar al código la transformación geométrica de traslación, usando el teclado. El código debe tener matriz de traslación.

debe poder moverse varias veces y ser continuo de acuerdo a la posición del momento.

en el código, cambiar la matriz de traslación por matriz de escalado en 2D. consideresolo escalado de aumentar y disminuir.

en el código, cambiar la matriz de escalado por matriz de rotación en 2D. considere la rotación en sentido horario y antihorario.

genearar un triángulo que del cuadrante ingerior izquierdo sea rojo, en cuadrante inferior derecho sea zul y los cuadrantes superiores sea verde, además, ese objeto debe rotar, hacer el escalado y la traslación, incorporado las matrices correspondientes de acuerdo a los casos anteriores.
"""

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import numpy as np
import math

# Triángulo con 3 vértices en (x, y, 1) - coordenadas homogéneas
original_vertices = np.array([
	[-0.5, -0.5, 1.0],  # Inferior izquierdo (cuadrante III)
	[ 0.5, -0.5, 1.0],  # Inferior derecho  (cuadrante IV)
	[ 0.0,  0.5, 1.0]   # Superior (cuadrantes I y II)
], dtype=np.float32)

# Estado actual (transformado)
transformed_vertices = original_vertices.copy()

# Colores RGB por vértice (asociado a cada vértice)
colors = [
	(1.0, 0.0, 0.0),  # Rojo (izquierda)
	(0.0, 0.0, 1.0),  # Azul (derecha)
	(0.0, 1.0, 0.0)   # Verde (arriba)
]

# Parámetros de transformación
angle_step = math.radians(5)
scale_up = 1.1
scale_down = 0.9
move_step = 0.05

# Aplicar matriz de transformación general
def apply_transformation(matrix):
	global transformed_vertices
	transformed_vertices = np.dot(transformed_vertices, matrix.T)
	glutPostRedisplay()

# ROTACIÓN
def rotate(theta):
	cos_t = math.cos(theta)
	sin_t = math.sin(theta)
	rotation_matrix = np.array([
		[cos_t, -sin_t, 0.0],
		[sin_t,  cos_t, 0.0],
		[0.0,     0.0,  1.0]
	], dtype=np.float32)
	apply_transformation(rotation_matrix)

# ESCALADO
def scale(sx, sy):
	scaling_matrix = np.array([
		[sx,  0.0, 0.0],
		[0.0, sy,  0.0],
		[0.0, 0.0, 1.0]
	], dtype=np.float32)
	apply_transformation(scaling_matrix)

# TRASLACIÓN
def translate(dx, dy):
	translation_matrix = np.array([
		[1.0, 0.0, dx],
		[0.0, 1.0, dy],
		[0.0, 0.0, 1.0]
	], dtype=np.float32)
	apply_transformation(translation_matrix)

# Dibuja los ejes X (rojo) y Y (azul)
def draw_axes():
	glLineWidth(2.0)
	glBegin(GL_LINES)

	# Eje X (horizontal, rojo)
	glColor3f(1.0, 0.0, 0.0)
	glVertex2f(-1.0, 0.0)
	glVertex2f(1.0, 0.0)

	# Eje Y (vertical, azul)
	glColor3f(0.0, 0.0, 1.0)
	glVertex2f(0.0, -1.0)
	glVertex2f(0.0, 1.0)

	glEnd()

# Dibuja el triángulo y los ejes
def draw_triangle():
	glClear(GL_COLOR_BUFFER_BIT)

	draw_axes()  # Primero dibujamos los ejes

	glBegin(GL_TRIANGLES)
	for i, vertex in enumerate(transformed_vertices):
		glColor3f(*colors[i])              # Color asociado al vértice
		glVertex2f(vertex[0], vertex[1])   # Coordenadas (x, y)
	glEnd()

	glFlush()

# Teclas especiales: rotación
def special_keys(key, x, y):
	if key == GLUT_KEY_LEFT:
		rotate(angle_step)         # Rotar antihorario
	elif key == GLUT_KEY_RIGHT:
		rotate(-angle_step)        # Rotar horario

# Teclas normales: escala y traslación
def keyboard(key, x, y):
	key = key.decode('utf-8').lower()
	if key == 'w':
		scale(scale_up, scale_up)      # Escalar hacia arriba
	elif key == 's':
		scale(scale_down, scale_down)  # Escalar hacia abajo
	elif key == 'a':
		translate(-move_step, 0.0)     # Mover a la izquierda
	elif key == 'd':
		translate(move_step, 0.0)      # Mover a la derecha
	elif key == 'q':
		translate(0.0, move_step)      # Mover hacia arriba
	elif key == 'z':
		translate(0.0, -move_step)     # Mover hacia abajo

# Inicialización
def main():
	glutInit()
	glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
	glutInitWindowSize(600, 600)
	glutCreateWindow(b"Triangulo 2D con ejes y transformaciones")

	glClearColor(1.0, 1.0, 1.0, 1.0)   # Fondo blanco
	glMatrixMode(GL_PROJECTION)
	gluOrtho2D(-1, 1, -1, 1)          # Vista ortográfica 2D

	# Vincular funciones
	glutDisplayFunc(draw_triangle)
	glutSpecialFunc(special_keys)     # Flechas
	glutKeyboardFunc(keyboard)        # Letras

	glutMainLoop()

if __name__ == "__main__":
	main()