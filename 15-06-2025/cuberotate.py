"""
crear un cubo con 8 puntos en python con pyOpenGL en el plano X, Y y Z

dale bordes a las vértices para ver mejor la perspectiva

dale colores a cada cara

ahora agrega los ejes X, Y y Z

agrégale rotación, pero con la función de matriz T(tx, ty, tx) 4x4 y que los ejes se mantenga quitos
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

def apply_translation(tx, ty, tz):
	T = np.array([
		[1.0, 0.0, 0.0, tx],
		[0.0, 1.0, 0.0, ty],
		[0.0, 0.0, 1.0, tz],
		[0.0, 0.0, 0.0, 1.0]
	], dtype=np.float32)
	glMultMatrixf(T.T)

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

	# Cámara
	gluLookAt(5, 5, 10, 0, 0, 0, 0, 1, 0)

	# Dibujar ejes fijos
	draw_axes()

	# Aplicar rotación solo al cubo
	glPushMatrix()
	glRotatef(angle_x, 1, 0, 0)
	glRotatef(angle_y, 0, 1, 0)
	glRotatef(angle_z, 0, 0, 1)
	draw_cube()
	glPopMatrix()

	glutSwapBuffers()

def update(value):
	global angle_x, angle_y, angle_z
	angle_x += 0.5
	angle_y += 0.6
	angle_z += 0.4
	glutPostRedisplay()
	glutTimerFunc(16, update, 0)

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
	glutCreateWindow(b"Cubo 3D - Rotacion sin afectar ejes")
	init()
	glutDisplayFunc(display)
	glutReshapeFunc(reshape)
	glutTimerFunc(0, update, 0)
	glutMainLoop()

if __name__ == "__main__":
	main()