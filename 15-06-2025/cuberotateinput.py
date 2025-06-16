"""
crear un cubo con 8 puntos en python con pyOpenGL en el plano X, Y y Z

dale bordes a las vértices para ver mejor la perspectiva

dale colores a cada cara

ahora agrega los ejes X, Y y Z

agrégale rotación, pero con la función de matriz T(tx, ty, tx) 4x4 y que los ejes se mantenga quitos

cambiar rotación para que se haga por teclado

aplica la rotación con matrices
"""

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np

# Ángulos de rotación
angle_x = 0
angle_y = 0
angle_z = 0

# Vértices del cubo
vertices = [
	[-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
	[-1, -1,  1], [1, -1,  1], [1, 1,  1], [-1, 1,  1]
]

# Caras y aristas del cubo
caras = [
	[0, 1, 2, 3], [4, 5, 6, 7],
	[0, 1, 5, 4], [3, 2, 6, 7],
	[1, 2, 6, 5], [0, 3, 7, 4]
]
aristas = [
	[0, 1], [1, 2], [2, 3], [3, 0],
	[4, 5], [5, 6], [6, 7], [7, 4],
	[0, 4], [1, 5], [2, 6], [3, 7]
]

# Colores
colores = [
	(1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0),
	(1.0, 1.0, 0.0), (1.0, 0.0, 1.0), (0.0, 1.0, 1.0)
]

def rotation_matrix_x(angle):
	rad = np.radians(angle)
	return np.array([
		[1, 0, 0, 0],
		[0, np.cos(rad), -np.sin(rad), 0],
		[0, np.sin(rad),  np.cos(rad), 0],
		[0, 0, 0, 1]
	], dtype=np.float32)

def rotation_matrix_y(angle):
	rad = np.radians(angle)
	return np.array([
		[np.cos(rad), 0, np.sin(rad), 0],
		[0, 1, 0, 0],
		[-np.sin(rad), 0, np.cos(rad), 0],
		[0, 0, 0, 1]
	], dtype=np.float32)

def rotation_matrix_z(angle):
	rad = np.radians(angle)
	return np.array([
		[np.cos(rad), -np.sin(rad), 0, 0],
		[np.sin(rad),  np.cos(rad), 0, 0],
		[0, 0, 1, 0],
		[0, 0, 0, 1]
	], dtype=np.float32)

def draw_cube():
	glBegin(GL_QUADS)
	for i, cara in enumerate(caras):
		glColor3fv(colores[i])
		for v in cara:
			glVertex3fv(vertices[v])
	glEnd()

	glColor3f(0.0, 0.0, 0.0)
	glLineWidth(2.0)
	glBegin(GL_LINES)
	for a in aristas:
		for v in a:
			glVertex3fv(vertices[v])
	glEnd()

def draw_axes():
	glLineWidth(3.0)
	glBegin(GL_LINES)
	glColor3f(1.0, 0.0, 0.0); glVertex3f(0, 0, 0); glVertex3f(2, 0, 0)  # X
	glColor3f(0.0, 1.0, 0.0); glVertex3f(0, 0, 0); glVertex3f(0, 2, 0)  # Y
	glColor3f(0.0, 0.0, 1.0); glVertex3f(0, 0, 0); glVertex3f(0, 0, 2)  # Z
	glEnd()

	# Letras
	glColor3f(1.0, 0.0, 0.0); glRasterPos3f(2.1, 0, 0); glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord('X'))
	glColor3f(0.0, 1.0, 0.0); glRasterPos3f(0, 2.1, 0); glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord('Y'))
	glColor3f(0.0, 0.0, 1.0); glRasterPos3f(0, 0, 2.1); glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord('Z'))

def display():
	global angle_x, angle_y, angle_z

	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()

	gluLookAt(5, 5, 10, 0, 0, 0, 0, 1, 0)

	draw_axes()

	glPushMatrix()

	Rx = rotation_matrix_x(angle_x)
	Ry = rotation_matrix_y(angle_y)
	Rz = rotation_matrix_z(angle_z)

	# Aplicar rotación: Z * Y * X
	glMultMatrixf(Rz.T)
	glMultMatrixf(Ry.T)
	glMultMatrixf(Rx.T)

	draw_cube()
	glPopMatrix()

	glutSwapBuffers()

def keyboard(key, x, y):
	global angle_x, angle_y, angle_z
	step = 5  # grados

	if key == b'x': angle_x += step
	elif key == b'y': angle_y += step
	elif key == b'z': angle_z += step
	elif key == b'X': angle_x -= step
	elif key == b'Y': angle_y -= step
	elif key == b'Z': angle_z -= step

	glutPostRedisplay()

def init():
	glEnable(GL_DEPTH_TEST)
	glClearColor(0.95, 0.95, 0.95, 1.0)

def reshape(w, h):
	glViewport(0, 0, w, h)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(45, w / h, 0.1, 100.0)
	glMatrixMode(GL_MODELVIEW)

def main():
	glutInit()
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
	glutInitWindowSize(600, 600)
	glutCreateWindow(b"Cubo 3D - Rotacion con matrices")
	init()
	glutDisplayFunc(display)
	glutReshapeFunc(reshape)
	glutKeyboardFunc(keyboard)
	glutMainLoop()

if __name__ == "__main__":
	main()