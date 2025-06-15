"""
crear la curva Bezier cuadrático con 3 puntos en python con pyOpenGL.

agrega líneas dotted entre los puntos de control.

ahora añade interacción para mover los puntos con el mouse o con el teclado.

ahora crea una curva bezier cúbica con 4 puntos mediante Python y con pyOpenGL.

no olvides agregar el movimiento de los puntos con el mouse o teclado.
"""

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np

# Tamaño ventana
width, height = 600, 600

# 4 puntos de control: P0, P1, P2, P3
control_points = np.array([
	[-0.8, -0.8],
	[-0.4,  0.8],
	[ 0.4, -0.8],
	[ 0.8,  0.8]
], dtype=float)

num_segments = 100
selected_point = -1  # Ningún punto seleccionado
mouse_drag = False

def bezier_cubic(t, P0, P1, P2, P3):
	return ((1 - t)**3 * P0 +
			3 * (1 - t)**2 * t * P1 +
			3 * (1 - t) * t**2 * P2 +
			t**3 * P3)

def draw_curve():
	glColor3f(0.0, 0.0, 1.0)
	glLineWidth(2)
	glBegin(GL_LINE_STRIP)
	for i in range(num_segments + 1):
		t = i / num_segments
		point = bezier_cubic(t, *control_points)
		glVertex2f(point[0], point[1])
	glEnd()

def draw_control_points():
	glPointSize(8)
	glColor3f(1.0, 0.0, 0.0)
	glBegin(GL_POINTS)
	for p in control_points:
		glVertex2f(p[0], p[1])
	glEnd()

	glColor3f(0.5, 0.5, 0.5)
	glEnable(GL_LINE_STIPPLE)
	glLineStipple(1, 0x00FF)
	glBegin(GL_LINE_STRIP)
	for p in control_points:
		glVertex2f(p[0], p[1])
	glEnd()
	glDisable(GL_LINE_STIPPLE)

def display():
	glClear(GL_COLOR_BUFFER_BIT)
	draw_control_points()
	draw_curve()
	glFlush()

def reshape(w, h):
	global width, height
	width, height = w, h
	glViewport(0, 0, w, h)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluOrtho2D(-1, 1, -1, 1)

def teclado(key, x, y):
	global selected_point
	if key in [b'1', b'2', b'3', b'4']:
		selected_point = int(key) - 1
	glutPostRedisplay()

def teclas_especiales(key, x, y):
	global control_points
	if selected_point == -1:
		return
	delta = 0.02
	if key == GLUT_KEY_LEFT:
		control_points[selected_point][0] -= delta
	elif key == GLUT_KEY_RIGHT:
		control_points[selected_point][0] += delta
	elif key == GLUT_KEY_UP:
		control_points[selected_point][1] += delta
	elif key == GLUT_KEY_DOWN:
		control_points[selected_point][1] -= delta
	glutPostRedisplay()

def mouse_click(button, state, x, y):
	global selected_point, mouse_drag
	if state == GLUT_DOWN:
		gl_x = (x / width) * 2 - 1
		gl_y = ((height - y) / height) * 2 - 1
		for i, p in enumerate(control_points):
			if np.linalg.norm(p - [gl_x, gl_y]) < 0.1:
				selected_point = i
				mouse_drag = True
				break
	else:
		mouse_drag = False

def mouse_move(x, y):
	global control_points
	if selected_point != -1 and mouse_drag:
		gl_x = (x / width) * 2 - 1
		gl_y = ((height - y) / height) * 2 - 1
		control_points[selected_point] = [gl_x, gl_y]
		glutPostRedisplay()

def init():
	glClearColor(1, 1, 1, 1)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluOrtho2D(-1, 1, -1, 1)

# Inicialización
glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(width, height)
glutCreateWindow(b"Curva Bezier Cubica con Interaccion")
init()

# Callbacks
glutDisplayFunc(display)
glutReshapeFunc(reshape)
glutKeyboardFunc(teclado)
glutSpecialFunc(teclas_especiales)
glutMouseFunc(mouse_click)
glutMotionFunc(mouse_move)

glutMainLoop()