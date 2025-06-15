"""
crear la curva Bezier cuadrático con 3 puntos en python con pyOpenGL.

agrega líneas dotted entre los puntos de control.

ahora añade interacción para mover los puntos con el mouse o con el teclado.

ahora crea una curva bezier cúbica con 4 puntos mediante Python y con pyOpenGL.

no olvides agregar el movimiento de los puntos con el mouse o teclado.
"""

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

# Lista de puntos de control (4 en total para curva cúbica)
control_points = np.array([
	[-0.8, -0.8],
	[-0.4,  0.8],
	[ 0.4,  0.8],
	[ 0.8, -0.8]
], dtype=np.float32)

selected_point = -1  # Índice del punto seleccionado (-1 = ninguno)
point_size = 0.05

# Bézier cúbica con 4 puntos
def bezier_cubic(t, P0, P1, P2, P3):
	return ((1 - t)**3) * P0 + 3 * ((1 - t)**2) * t * P1 + \
		3 * (1 - t) * t**2 * P2 + t**3 * P3

# Dibujar puntos de control
def draw_control_points():
	glPointSize(8)
	glColor3f(1.0, 0.0, 0.0)
	glBegin(GL_POINTS)
	for p in control_points:
		glVertex2f(p[0], p[1])
	glEnd()

# Dibujar líneas punteadas
def draw_dotted_lines():
	glEnable(GL_LINE_STIPPLE)
	glLineStipple(1, 0x00FF)
	glColor3f(0.0, 0.0, 0.0)
	glBegin(GL_LINE_STRIP)
	for p in control_points:
		glVertex2f(p[0], p[1])
	glEnd()
	glDisable(GL_LINE_STIPPLE)

# Dibujar curva Bézier
def draw_bezier_curve():
	glColor3f(0.0, 0.0, 1.0)
	glBegin(GL_LINE_STRIP)
	for i in range(101):
		t = i / 100.0
		pt = bezier_cubic(t, *control_points)
		glVertex2f(pt[0], pt[1])
	glEnd()

# Dibujo general
def display():
	glClear(GL_COLOR_BUFFER_BIT)
	draw_dotted_lines()
	draw_control_points()
	draw_bezier_curve()
	glFlush()

# Mouse: seleccionar punto
def mouse_click(button, state, x, y):
	global selected_point
	if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
		# Convertir coordenadas de ventana a mundo
		wx = (x / 300.0) - 1.0
		wy = 1.0 - (y / 300.0)
		for i, p in enumerate(control_points):
			if abs(p[0] - wx) < point_size and abs(p[1] - wy) < point_size:
				selected_point = i
				break

# Mouse: arrastrar punto
def mouse_drag(x, y):
	global selected_point
	if selected_point != -1:
		wx = (x / 300.0) - 1.0
		wy = 1.0 - (y / 300.0)
		control_points[selected_point] = [wx, wy]
		glutPostRedisplay()

# Teclado para mover punto seleccionado
def keyboard(key, x, y):
	global selected_point
	if selected_point == -1:
		return
	step = 0.02
	if key == b'w':
		control_points[selected_point][1] += step
	elif key == b's':
		control_points[selected_point][1] -= step
	elif key == b'a':
		control_points[selected_point][0] -= step
	elif key == b'd':
		control_points[selected_point][0] += step
	glutPostRedisplay()

# Setup
def main():
	glutInit()
	glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
	glutInitWindowSize(600, 600)
	glutCreateWindow(b"Curva Bezier cubica interactiva")

	glClearColor(1.0, 1.0, 1.0, 1.0)
	glMatrixMode(GL_PROJECTION)
	gluOrtho2D(-1.0, 1.0, -1.0, 1.0)

	glutDisplayFunc(display)
	glutMouseFunc(mouse_click)
	glutMotionFunc(mouse_drag)
	glutKeyboardFunc(keyboard)

	glutMainLoop()

if __name__ == "__main__":
	main()