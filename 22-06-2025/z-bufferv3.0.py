"""
Genera un código en python con PyOpenGL (Un ejemplo visual) donde se muestre 2 cubos que se solapan y donde el Z-buffer decide cuál se ve. "Aplica técnica de resterización Z-Buffer".
"""

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

angle = 0.0  # Rotación animada

def init():
	glEnable(GL_DEPTH_TEST)  # Activar Z-buffer
	glClearColor(0.1, 0.1, 0.1, 1.0)  # Fondo gris oscuro
	glShadeModel(GL_SMOOTH)

def draw_cube(x, y, z, color):
	glPushMatrix()
	glTranslatef(x, y, z)
	glColor3f(*color)
	glutSolidCube(1.5)
	glPopMatrix()

def display():
	global angle
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Borrar color y profundidad

	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	gluLookAt(3, 3, 6, 0, 0, 0, 0, 1, 0)

	glRotatef(angle, 0, 1, 0)  # Rotar escena
	draw_cube(0.5, 0, 0, (1.0, 0.0, 0.0))  # Cubo rojo
	draw_cube(-0.5, 0, 0, (0.0, 0.0, 1.0))  # Cubo azul

	glutSwapBuffers()

def idle():
	global angle
	angle += 0.3
	glutPostRedisplay()

def reshape(width, height):
	glViewport(0, 0, width, height)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(45.0, width / float(height or 1), 0.1, 100.0)

def main():
	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
	glutInitWindowSize(800, 600)
	glutCreateWindow(b"Cubos con Z-buffer (PyOpenGL)")

	init()
	glutDisplayFunc(display)
	glutReshapeFunc(reshape)
	glutIdleFunc(idle)
	glutMainLoop()

if __name__ == "__main__":
	main()