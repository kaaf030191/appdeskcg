"""
crear un cubo con 8 puntos en python con pyOpenGL en el plano X, Y y Z.

dale bordes a las vértices para ver mejor la perspectiva.

dale colores a cada cara.

ahora agrega los ejes X, Y y Z.

agrégale traslación, pero con la función de matriz T(tx, ty, tx) 4x4.

que permita mover con las teclas y los ejes deben mantenerse en su lugar.

dale una perspectiva donde se note que es un cubo en 3D.
"""

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np

# Vértices del cubo
vertices = [
	[-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
	[-1, -1,  1], [1, -1,  1], [1, 1,  1], [-1, 1,  1]
]

# Caras del cubo
caras = [
	[0, 1, 2, 3], [4, 5, 6, 7],
	[0, 1, 5, 4], [3, 2, 6, 7],
	[1, 2, 6, 5], [0, 3, 7, 4]
]

# Aristas (bordes del cubo)
aristas = [
	[0, 1], [1, 2], [2, 3], [3, 0],
	[4, 5], [5, 6], [6, 7], [7, 4],
	[0, 4], [1, 5], [2, 6], [3, 7]
]

# Colores para cada cara
colores = [
	(1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0),
	(1.0, 1.0, 0.0), (1.0, 0.0, 1.0), (0.0, 1.0, 1.0)
]

# Posición del cubo
cube_pos = [0.0, 0.0, 0.0]

def apply_translation(tx, ty, tz):
	T = np.array([
		[1.0, 0.0, 0.0, tx],
		[0.0, 1.0, 0.0, ty],
		[0.0, 0.0, 1.0, tz],
		[0.0, 0.0, 0.0, 1.0]
	], dtype=np.float32)
	glMultMatrixf(T.T)

def draw_cube():
	# Caras con color
	glBegin(GL_QUADS)
	for i, cara in enumerate(caras):
		glColor3fv(colores[i])
		for v in cara:
			glVertex3fv(vertices[v])
	glEnd()

	# Bordes
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
	glColor3f(1.0, 0.0, 0.0); glVertex3f(0, 0, 0); glVertex3f(2, 0, 0)
	glColor3f(0.0, 1.0, 0.0); glVertex3f(0, 0, 0); glVertex3f(0, 2, 0)
	glColor3f(0.0, 0.0, 1.0); glVertex3f(0, 0, 0); glVertex3f(0, 0, 2)
	glEnd()

	# Letras
	glColor3f(1.0, 0.0, 0.0); glRasterPos3f(2.1, 0, 0); glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord('X'))
	glColor3f(0.0, 1.0, 0.0); glRasterPos3f(0, 2.1, 0); glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord('Y'))
	glColor3f(0.0, 0.0, 1.0); glRasterPos3f(0, 0, 2.1); glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord('Z'))

def display():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()

	# Vista inclinada para dar perspectiva
	gluLookAt(5, 5, 10,  0, 0, 0,  0, 1, 0)

	draw_axes()

	glPushMatrix()
	apply_translation(*cube_pos)
	draw_cube()
	glPopMatrix()

	glutSwapBuffers()

def keyboard(key, x, y):
	step = 0.2
	if key == b'w': cube_pos[1] += step
	elif key == b's': cube_pos[1] -= step
	elif key == b'd': cube_pos[0] += step
	elif key == b'a': cube_pos[0] -= step
	elif key == b'q': cube_pos[2] -= step
	elif key == b'e': cube_pos[2] += step
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
	glutInitWindowSize(700, 700)
	glutCreateWindow(b"Cubo 3D sin rotacion - PyOpenGL")
	init()
	glutDisplayFunc(display)
	glutKeyboardFunc(keyboard)
	glutReshapeFunc(reshape)
	glutMainLoop()

if __name__ == "__main__":
	main()