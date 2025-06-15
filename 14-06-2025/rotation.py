"""
crear un triángulo en 2D cuyos vértices deben de estar en una matriz. mediante python con OpenGL.

agregar al código la transformación geométrica de traslación, usando el teclado. El código debe tener matriz de traslación.

debe poder moverse varias veces y ser continuo de acuerdo a la posición del momento.

en el código, cambiar la matriz de traslación por matriz de escalado en 2D. consideresolo escalado de aumentar y disminuir.

en el código, cambiar la matriz de escalado por matriz de rotación en 2D. considere la rotación en sentido horario y antihorario.
"""

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import numpy as np
import math

# Vértices originales en coordenadas homogéneas (x, y, 1)
original_vertices = np.array([
	[-0.5, -0.5, 1.0],  # Vértice inferior izquierdo
	[ 0.5, -0.5, 1.0],  # Vértice inferior derecho
	[ 0.0,  0.5, 1.0]   # Vértice superior
], dtype=np.float32)

# Estado actual de los vértices transformados
transformed_vertices = original_vertices.copy()

# Ángulo de rotación en radianes (5 grados)
angle_step = math.radians(5)

# Función que aplica rotación acumulativa
def apply_rotation(theta):
	global transformed_vertices

	cos_theta = math.cos(theta)
	sin_theta = math.sin(theta)

	# Matriz de rotación homogénea 3x3
	rotation_matrix = np.array([
		[cos_theta, -sin_theta, 0.0],
		[sin_theta,  cos_theta, 0.0],
		[0.0,        0.0,       1.0]
	], dtype=np.float32)

	# Aplicar rotación sobre los vértices actuales
	transformed_vertices = np.dot(transformed_vertices, rotation_matrix.T)

	glutPostRedisplay()  # Redibujar ventana

# Función para dibujar el triángulo
def draw_triangle():
	glClear(GL_COLOR_BUFFER_BIT)

	glBegin(GL_TRIANGLES)
	for vertex in transformed_vertices:
		glVertex2f(vertex[0], vertex[1])
	glEnd()

	glFlush()

# Manejador de teclas especiales
def special_keys(key, x, y):
	if key == GLUT_KEY_LEFT:
		apply_rotation(angle_step)        # Rotar en sentido antihorario
	elif key == GLUT_KEY_RIGHT:
		apply_rotation(-angle_step)       # Rotar en sentido horario

# Configuración de ventana y OpenGL
def main():
	glutInit()
	glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
	glutInitWindowSize(500, 500)
	glutCreateWindow(b"Rotacion acumulativa del Triangulo 2D")

	glClearColor(1.0, 1.0, 1.0, 1.0)  # Fondo blanco
	glColor3f(0.0, 0.0, 1.0)          # Triángulo azul

	glMatrixMode(GL_PROJECTION)
	gluOrtho2D(-1, 1, -1, 1)          # Coordenadas 2D

	glutDisplayFunc(draw_triangle)
	glutSpecialFunc(special_keys)

	glutMainLoop()

if __name__ == "__main__":
	main()