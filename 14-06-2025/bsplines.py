"""
ejemplo de aplicación de la curva b-splines en carretera, aplicando pyOpenGL de python.

genera algo más comprensible y mejóralo visualmente, tiene errores y una recta no tiene punto de control.
"""

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

# Puntos de control
control_points = np.array([
	[-0.9, -0.8],
	[-0.6, -0.3],
	[-0.3,  0.3],
	[ 0.0,  0.7],
	[ 0.3,  0.3],
	[ 0.6, -0.3],
	[ 0.9, -0.7]
], dtype=np.float32)

selected_point = -1
point_radius = 0.04

# B-spline cúbica uniforme
def de_boor(i, k, t, knots):
	if k == 0:
		return 1.0 if knots[i] <= t < knots[i + 1] else 0.0
	denom1 = knots[i + k] - knots[i]
	denom2 = knots[i + k + 1] - knots[i + 1]
	term1 = ((t - knots[i]) / denom1) * de_boor(i, k - 1, t, knots) if denom1 else 0
	term2 = ((knots[i + k + 1] - t) / denom2) * de_boor(i + 1, k - 1, t, knots) if denom2 else 0
	return term1 + term2

def b_spline(t, degree=3):
	n = len(control_points) - 1
	k = degree
	knots = np.concatenate(([0] * (k + 1), np.linspace(0, 1, n - k + 1), [1] * (k + 1)))
	point = np.zeros(2)
	for i in range(len(control_points)):
		b = de_boor(i, k, t, knots)
		point += b * control_points[i]
	return point

# Dibujar curva
def draw_b_spline():
	glColor3f(0.2, 0.2, 0.8)
	glLineWidth(5)
	glBegin(GL_LINE_STRIP)
	for t in np.linspace(0, 1, 200):
		p = b_spline(t)
		glVertex2f(p[0], p[1])
	glEnd()
	glLineWidth(1)

# Dibuja los puntos y etiquetas
def draw_control_points():
	glPointSize(10)
	for i, p in enumerate(control_points):
		glColor3f(1.0, 0.0, 0.0)
		glBegin(GL_POINTS)
		glVertex2f(p[0], p[1])
		glEnd()
		draw_label(f"P{i}", p[0], p[1] + 0.05)

def draw_label(text, x, y):
	glColor3f(0.1, 0.1, 0.1)
	glRasterPos2f(x, y)
	for ch in text:
		glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(ch))

def draw_dotted_lines():
	glEnable(GL_LINE_STIPPLE)
	glLineStipple(1, 0x0F0F)
	glColor3f(0.5, 0.5, 0.5)
	glBegin(GL_LINE_STRIP)
	for p in control_points:
		glVertex2f(p[0], p[1])
	glEnd()
	glDisable(GL_LINE_STIPPLE)

# Display principal
def display():
	glClear(GL_COLOR_BUFFER_BIT)
	draw_dotted_lines()
	draw_control_points()
	draw_b_spline()
	glFlush()

# Conversión de pantalla a coordenadas OpenGL
def screen_to_gl(x, y):
	w, h = glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT)
	return (x / w) * 2 - 1, 1 - (y / h) * 2

# Mouse
def mouse_click(button, state, x, y):
	global selected_point
	if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
		mx, my = screen_to_gl(x, y)
		for i, p in enumerate(control_points):
			if abs(p[0] - mx) < point_radius and abs(p[1] - my) < point_radius:
				selected_point = i
				break

def mouse_drag(x, y):
	global selected_point
	if selected_point != -1:
		mx, my = screen_to_gl(x, y)
		control_points[selected_point] = [mx, my]
		glutPostRedisplay()

# Teclado
def keyboard(key, x, y):
	global selected_point
	step = 0.02
	if selected_point == -1:
		return
	if key == b'w':
		control_points[selected_point][1] += step
	elif key == b's':
		control_points[selected_point][1] -= step
	elif key == b'a':
		control_points[selected_point][0] -= step
	elif key == b'd':
		control_points[selected_point][0] += step
	glutPostRedisplay()

# Configuración
def main():
	glutInit()
	glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
	glutInitWindowSize(800, 600)
	glutCreateWindow(b"Carretera con curva B-spline interactiva")

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