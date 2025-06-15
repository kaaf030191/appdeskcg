"""
crear un triángulo en 2D cuyos vértices deben de estar en una matriz. mediante python con OpenGL.

agregar al código la transformación geométrica de traslación, usando el teclado. El código debe tener matriz de traslación.

debe poder moverse varias veces y ser continuo de acuerdo a la posición del momento.

en el código, cambiar la matriz de traslación por matriz de escalado en 2D. consideresolo escalado de aumentar y disminuir.
"""

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import numpy as np

# Vértices originales en coordenadas homogéneas (x, y, 1)
original_vertices = np.array([
	[-0.5, -0.5, 1.0],  # Vértice inferior izquierdo
	[ 0.5, -0.5, 1.0],  # Vértice inferior derecho
	[ 0.0,  0.5, 1.0]   # Vértice superior
], dtype=np.float32)

# Vértices transformados (estado actual)
transformed_vertices = original_vertices.copy()

# Factor de escalado
scale_up = 1.1     # Aumentar tamaño en 10%
scale_down = 0.9   # Disminuir tamaño en 10%

# Función para aplicar escalado acumulativo
def apply_scaling(sx, sy):
	global transformed_vertices

	# Matriz de escalado homogénea 3x3
	scaling_matrix = np.array([
		[sx,  0.0, 0.0],  # Escala en x
		[0.0, sy,  0.0],  # Escala en y
		[0.0, 0.0, 1.0]   # Homogénea
	], dtype=np.float32)

	# Aplicamos el escalado a los vértices transformados
	transformed_vertices = np.dot(transformed_vertices, scaling_matrix.T)

	glutPostRedisplay()  # Redibuja la ventana

# Dibuja el triángulo en su estado actual
def draw_triangle():
	glClear(GL_COLOR_BUFFER_BIT)

	glBegin(GL_TRIANGLES)

	for vertex in transformed_vertices:
		glVertex2f(vertex[0], vertex[1])
	glEnd()

	glFlush()

# Manejador de teclas especiales
def special_keys(key, x, y):
	if key == GLUT_KEY_UP:
		apply_scaling(scale_up, scale_up)       # Escala hacia arriba
	elif key == GLUT_KEY_DOWN:
		apply_scaling(scale_down, scale_down)   # Escala hacia abajo

# Inicialización de OpenGL
def main():
	glutInit()
	glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
	glutInitWindowSize(500, 500)
	glutCreateWindow(b"Escalado acumulativo del Triangulo 2D")

	glClearColor(1.0, 1.0, 1.0, 1.0)  # Fondo blanco
	glColor3f(0.0, 0.0, 1.0)          # Triángulo azul

	glMatrixMode(GL_PROJECTION)
	gluOrtho2D(-1, 1, -1, 1)          # Coordenadas 2D

	glutDisplayFunc(draw_triangle)
	glutSpecialFunc(special_keys)

	glutMainLoop()

if __name__ == "__main__":
	main()