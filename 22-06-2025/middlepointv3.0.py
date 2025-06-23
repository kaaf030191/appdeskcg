import OpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Parámetros de la circunferencia
RADIUS = 10
CENTER_X_DISPLAY = 0  # Centro de la circunferencia para la visualización
CENTER_Y_DISPLAY = 10 # Centro de la circunferencia para la visualización

def draw_point(x, y):
	"""Dibuja un punto en las coordenadas dadas."""
	glBegin(GL_POINTS)
	glVertex2f(x, y)
	glEnd()

def plot_circle_points(x_center, y_center, x, y):
	"""
	Dibuja los 8 puntos simétricos de la circunferencia,
	trasladando cada punto al centro deseado.
	Aquí solo necesitamos el primer octante para el primer cuadrante.
	"""
	# Primer cuadrante
	# (x, y) -> (x_center + x, y_center + y)
	# (y, x) -> (x_center + y, y_center + x)
	draw_point(x_center + x, y_center + y)
	draw_point(x_center + y, y_center + x)

def midpoint_circle_algorithm():
	"""
	Implementa el algoritmo de punto medio para dibujar una circunferencia.
	Genera puntos para un círculo centrado en (0,0) y luego los traslada
	al centro deseado para la visualización.
	"""
	x = 0
	y = RADIUS
	p = 1 - RADIUS  # Parámetro de decisión inicial

	# Dibuja el primer octante de la circunferencia (de x=0 hasta x=y)
	while x <= y:
		plot_circle_points(CENTER_X_DISPLAY, CENTER_Y_DISPLAY, x, y)
		x += 1
		if p < 0:
			p += 2 * x + 1
		else:
			y -= 1
			p += 2 * (x - y) + 1

def display():
	"""Función de callback para dibujar."""
	glClear(GL_COLOR_BUFFER_BIT)
	glColor3f(1.0, 1.0, 1.0)  # Color blanco para la circunferencia y ejes

	# Dibujar ejes X e Y
	glBegin(GL_LINES)
	# Eje X
	glVertex2f(-20.0, 0.0)
	glVertex2f(20.0, 0.0)
	# Eje Y
	glVertex2f(0.0, -5.0) # Ajustado para que el eje Y se vea un poco más abajo del centro (0,10)
	glVertex2f(0.0, 25.0)
	glEnd()

	midpoint_circle_algorithm()
	glFlush()

def init():
	"""Inicialización de OpenGL."""
	glClearColor(0.0, 0.0, 0.0, 1.0)  # Color de fondo negro
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	# Define la ventana de visualización: (izquierda, derecha, abajo, arriba)
	# Ajustado para que la circunferencia con centro (0,10) y radio 10 sea visible.
	gluOrtho2D(-25.0, 25.0, -5.0, 25.0) # Se extiende un poco más allá para ver los ejes

def main():
	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
	glutInitWindowSize(600, 600)  # Tamaño de la ventana
	glutInitWindowPosition(100, 100) # Posición de la ventana en la pantalla
	glutCreateWindow(b"Circunferencia con Algoritmo de Punto Medio") # Título de la ventana
	init()
	glutDisplayFunc(display)
	glutMainLoop()

if __name__ == "__main__":
	main()