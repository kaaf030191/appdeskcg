"""
hacer una carretera interactiva o unir varios tramos para simular una vía real más extensa mediante Python con pyOpenGL.

ahora agrégale interactividad para mover los puntos con el mouse o teclado.

no funciona, falta que permite arrastrar los puntos con el mouse o con el teclado.

agrega etiqueta de datos a cada punto.
"""

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

control_points = [
	[-0.9, -0.7],
	[-0.6, -0.2],
	[-0.3,  0.2],
	[ 0.0,  0.0],
	[ 0.3, -0.2],
	[ 0.4,  0.4],
	[ 0.6,  0.7],
	[ 0.9,  0.3]
]
control_points = np.array(control_points, dtype=np.float32)

selected_point = -1
point_radius = 0.04

def bezier_cubic(t, P0, P1, P2, P3):
	return ((1 - t) ** 3) * P0 + 3 * ((1 - t) ** 2) * t * P1 + \
		3 * (1 - t) * t ** 2 * P2 + t ** 3 * P3

def draw_points():
	glPointSize(10)
	glColor3f(1.0, 0.0, 0.0)
	glBegin(GL_POINTS)
	for p in control_points:
		glVertex2f(p[0], p[1])
	glEnd()

def draw_labels():
	glColor3f(0.0, 0.0, 0.0)
	for i, (x, y) in enumerate(control_points):
		label = f"P{i}"
		glRasterPos2f(x + 0.03, y + 0.03)
		for ch in label:
			glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(ch))

def draw_dotted_lines():
	glEnable(GL_LINE_STIPPLE)
	glLineStipple(1, 0x00FF)
	glColor3f(0.0, 0.0, 0.0)
	glBegin(GL_LINE_STRIP)
	for p in control_points:
		glVertex2f(p[0], p[1])
	glEnd()
	glDisable(GL_LINE_STIPPLE)

def draw_bezier_road():
    glColor3f(0.2, 0.2, 0.2)
    glLineWidth(5)
    glBegin(GL_LINE_STRIP)
    last_pt = None
    for i in range(0, len(control_points) - 3, 3):
        P0, P1, P2, P3 = control_points[i], control_points[i+1], control_points[i+2], control_points[i+3]
        for t in np.linspace(0, 1, 50):
            pt = bezier_cubic(t, P0, P1, P2, P3)
            glVertex2f(pt[0], pt[1])
            last_pt = pt
    glEnd()

    # Si hay un último punto suelto (ej. P7), conecta una línea directa
    if last_pt is not None and len(control_points) % 3 != 1:
        glColor3f(0.2, 0.2, 0.2)
        glBegin(GL_LINES)
        glVertex2f(last_pt[0], last_pt[1])
        glVertex2f(control_points[-1][0], control_points[-1][1])
        glEnd()

    glLineWidth(1)


def display():
	glClear(GL_COLOR_BUFFER_BIT)
	draw_dotted_lines()
	draw_points()
	draw_labels()
	draw_bezier_road()
	glFlush()

def screen_to_gl(x, y):
	w, h = glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT)
	gl_x = (x / w) * 2 - 1
	gl_y = 1 - (y / h) * 2
	return gl_x, gl_y

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

def main():
	glutInit()
	glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
	glutInitWindowSize(600, 600)
	glutCreateWindow(b"Carretera Bezier Interactiva")

	glClearColor(1, 1, 1, 1)
	glMatrixMode(GL_PROJECTION)
	gluOrtho2D(-1, 1, -1, 1)

	glutDisplayFunc(display)
	glutMouseFunc(mouse_click)
	glutMotionFunc(mouse_drag)
	glutKeyboardFunc(keyboard)

	glutMainLoop()

if __name__ == "__main__":
	main()