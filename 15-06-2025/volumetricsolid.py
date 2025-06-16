"""
crear un modelo geométrico volumétrico sólido de una tetera con python y pyopengl
"""

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

# Rotación
angle = 0.0

def init():
	glEnable(GL_DEPTH_TEST)
	glEnable(GL_LIGHTING)
	glEnable(GL_LIGHT0)

	# Luz ambiental y difusa
	glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
	glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
	glLightfv(GL_LIGHT0, GL_POSITION, [1.0, 1.0, 2.0, 0.0])

	# Material
	glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, [0.4, 0.5, 0.8, 1.0])

	glClearColor(1.0, 1.0, 1.0, 1.0)

def display():
	global angle
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()

	# Cámara
	gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)

	glRotatef(angle, 0, 1, 0)

	# Dibujar tetera sólida
	glutSolidTeapot(1.0)

	# Ejemplos de formas en malla
	# glutWireTeapot(1.0)
	# glutWireCube(1.0)
	# glutWireSphere(1, 20, 20)
	# glutWireTorus(0.2, 0.8, 20, 20)
	# glutWireOctahedron()
	# glutWireIcosahedron()

	glutSwapBuffers()
	angle += 0.5

def reshape(width, height):
	glViewport(0, 0, width, height)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(45, width / float(height), 1.0, 100.0)
	glMatrixMode(GL_MODELVIEW)

def timer(value):
	glutPostRedisplay()
	glutTimerFunc(16, timer, 0)

def main():
	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
	glutInitWindowSize(600, 600)
	glutCreateWindow(b"Tetera Solida - PyOpenGL")
	init()
	glutDisplayFunc(display)
	glutReshapeFunc(reshape)
	glutTimerFunc(0, timer, 0)
	glutMainLoop()

if __name__ == "__main__":
	main()