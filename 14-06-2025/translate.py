"""
crear un triángulo en 2D cuyos vértices deben de estar en una matriz. mediante python con OpenGL.

agregar al código la transformación geométrica de traslación, usando el teclado. El código debe tener matriz de traslación.

debe poder moverse varias veces y ser continuo de acuerdo a la posición del momento.
"""

# Importamos las funciones necesarias de las bibliotecas OpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Usamos numpy para manejar matrices y vectores de forma eficiente
import numpy as np

# Vértices originales del triángulo en coordenadas homogéneas (x, y, 1)
# Esto permite usar matrices 3x3 para transformaciones 2D (traslación, rotación, escala)
original_vertices = np.array([
	[-0.5, -0.5, 1.0],  # Vértice inferior izquierdo
	[ 0.5, -0.5, 1.0],  # Vértice inferior derecho
	[ 0.0,  0.5, 1.0]   # Vértice superior central
], dtype=np.float32)

# Copia de los vértices, que se actualizarán con cada transformación
transformed_vertices = original_vertices.copy()

# Tamaño del paso de movimiento al presionar una tecla
step = 0.05

# Función que aplica una traslación (dx, dy) acumulativa a los vértices
def apply_translation(dx, dy):
	global transformed_vertices

	# Creamos una matriz de traslación homogénea 3x3
	# Esta matriz desplaza el objeto en el plano 2D
	translation_matrix = np.array([
		[1.0, 0.0, dx],  # Suma dx a la coordenada x
		[0.0, 1.0, dy],  # Suma dy a la coordenada y
		[0.0, 0.0, 1.0]  # Mantiene el valor homogéneo (para que sea compatible con matriz)
	], dtype=np.float32)

	# Aplicamos la matriz de traslación a los vértices actuales
	# Se usa la transpuesta porque OpenGL espera vectores fila
	transformed_vertices = np.dot(transformed_vertices, translation_matrix.T)

	# Indicamos a OpenGL que debe redibujar la pantalla
	glutPostRedisplay()

# Función que se encarga de dibujar el triángulo en pantalla
def draw_triangle():
	# Limpia el búfer de color (borra lo que había antes)
	glClear(GL_COLOR_BUFFER_BIT)

	# Comienza a dibujar un triángulo
	glBegin(GL_TRIANGLES)

	for vertex in transformed_vertices:
		# Dibujamos solo las coordenadas x e y (ignoramos el 1 homogéneo)
		glVertex2f(vertex[0], vertex[1])
	glEnd()

	# Fuerza el renderizado inmediato
	glFlush()

# Manejador de teclas especiales como las flechas del teclado
def special_keys(key, x, y):
	if key == GLUT_KEY_LEFT:
		apply_translation(-step, 0.0)  # Mueve a la izquierda
	elif key == GLUT_KEY_RIGHT:
		apply_translation(step, 0.0)   # Mueve a la derecha
	elif key == GLUT_KEY_UP:
		apply_translation(0.0, step)   # Mueve hacia arriba
	elif key == GLUT_KEY_DOWN:
		apply_translation(0.0, -step)  # Mueve hacia abajo

# Función principal: configura la ventana y el contexto de OpenGL
def main():
	glutInit()  # Inicializa GLUT
	glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)  # Usamos un solo búfer y color RGB
	glutInitWindowSize(500, 500)  # Define el tamaño de la ventana en píxeles
	glutCreateWindow(b"Traslacion acumulativa del Triangulo 2D")  # Crea la ventana (b = byte string sin caracteres especiales)

	# Color de fondo: blanco (RGBA)
	glClearColor(1.0, 1.0, 1.0, 1.0)

	# Color del triángulo: azul (RGB)
	glColor3f(0.0, 0.0, 1.0)

	# Configura el sistema de coordenadas 2D
	glMatrixMode(GL_PROJECTION)       # Cambia a la matriz de proyección
	gluOrtho2D(-1, 1, -1, 1)          # Proyección ortográfica 2D de -1 a 1 en X y Y

	# Asignamos funciones de dibujo y manejo de teclado
	glutDisplayFunc(draw_triangle)    # Función de dibujo
	glutSpecialFunc(special_keys)     # Función para teclas especiales (flechas)

	# Inicia el bucle principal de eventos
	glutMainLoop()

# Ejecuta la función principal si el archivo se ejecuta directamente
if __name__ == "__main__":
	main()