"""
crear la curva Bezier cuadrático con 3 puntos en python con pyOpenGL.

agrega líneas dotted entre los puntos de control.

ahora añade interacción para mover los puntos con el mouse o con el teclado.
"""

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

# Puntos de control
control_points = np.array([
	[-0.8, -0.8],
	[ 0.0,  0.8],
	[ 0.8, -0.8]
], dtype=np.float32)

selected_index = None        # Índice del punto seleccionado (0, 1 o 2)
dragging = False             # Flag para saber si se está arrastrando
point_radius = 0.05          # Radio de detección para click
move_step = 0.05             # Paso de movimiento con teclado

# Función Bézier cuadrática
def bezier_quadratic(t, P0, P1, P2):
	return ((1 - t)**2) * P0 + 2 * (1 - t) * t * P1 + (t**2) * P2

# Dibuja los puntos de control
def draw_control_points():
	glPointSize(8.0)
	glColor3f(1.0, 0.0, 0.0)
	glBegin(GL_POINTS)
	for pt in control_points:
		glVertex2f(pt[0], pt[1])
	glEnd()

# Dibuja líneas punteadas entre puntos
def draw_dotted_lines():
	glEnable(GL_LINE_STIPPLE)
	glLineStipple(1, 0x00FF)
	glColor3f(0.0, 0.0, 0.0)
	glBegin(GL_LINE_STRIP)
	for pt in control_points:
		glVertex2f(pt[0], pt[1])
	glEnd()
	glDisable(GL_LINE_STIPPLE)

# Dibuja la curva Bézier
def draw_bezier_curve():
	glColor3f(0.0, 0.0, 1.0)
	glBegin(GL_LINE_STRIP)
	for i in range(101):
		t = i / 100.0
		pt = bezier_quadratic(t, *control_points)
		glVertex2f(pt[0], pt[1])
	glEnd()

def display():
	glClear(GL_COLOR_BUFFER_BIT)
	draw_dotted_lines()
	draw_control_points()
	draw_bezier_curve()
	glFlush()

# Detecta si el click está cerca de un punto
def get_point_at(x, y):
	for i, pt in enumerate(control_points):
		if np.linalg.norm(pt - np.array([x, y])) < point_radius:
			return i
	return None

# Convierte coordenadas de ventana a mundo
def screen_to_world(x, y):
	width = glutGet(GLUT_WINDOW_WIDTH)
	height = glutGet(GLUT_WINDOW_HEIGHT)
	world_x = (x / width) * 2 - 1
	world_y = -((y / height) * 2 - 1)
	return world_x, world_y

# Manejo del mouse
def mouse(button, state, x, y):
	global selected_index, dragging
	if button == GLUT_LEFT_BUTTON:
		world_x, world_y = screen_to_world(x, y)
		if state == GLUT_DOWN:
			selected_index = get_point_at(world_x, world_y)
			dragging = selected_index is not None
		elif state == GLUT_UP:
			dragging = False

# Mueve el punto con el mouse
def motion(x, y):
	global control_points
	if dragging and selected_index is not None:
		world_x, world_y = screen_to_world(x, y)
		control_points[selected_index] = [world_x, world_y]
		glutPostRedisplay()

# Teclado normal: mover el punto seleccionado
def keyboard(key, x, y):
	global control_points, selected_index
	key = key.decode('utf-8').lower()
	if key in ['1', '2', '3']:
		selected_index = int(key) - 1
	elif selected_index is not None:
		if key == 'w':
			control_points[selected_index][1] += move_step
		elif key == 's':
			control_points[selected_index][1] -= move_step
		elif key == 'a':
			control_points[selected_index][0] -= move_step
		elif key == 'd':
			control_points[selected_index][0] += move_step
		glutPostRedisplay()

# Inicialización
def main():
	glutInit()
	glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
	glutInitWindowSize(600, 600)
	glutCreateWindow(b"Curva Bezier Interactiva con PyOpenGL")

	glClearColor(1.0, 1.0, 1.0, 1.0)
	glMatrixMode(GL_PROJECTION)
	gluOrtho2D(-1, 1, -1, 1)

	glutDisplayFunc(display)
	glutKeyboardFunc(keyboard)
	glutMouseFunc(mouse)
	glutMotionFunc(motion)

	glutMainLoop()

if __name__ == "__main__":
	main()