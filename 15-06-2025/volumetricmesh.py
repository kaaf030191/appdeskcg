"""
crear un modelo geométrico volumétrico con python y pyopengl

muéstralo en forma de malla
"""

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

angle = 0.0  # Ángulo de rotación

def init():
	glEnable(GL_DEPTH_TEST)
	glEnable(GL_LIGHTING)
	glEnable(GL_LIGHT0)
	glEnable(GL_COLOR_MATERIAL)
	glClearColor(1.0, 1.0, 1.0, 1.0)

	# Luz blanca en posición (1, 1, 1)
	glLightfv(GL_LIGHT0, GL_POSITION, [1.0, 1.0, 1.0, 0.0])

def display():
	global angle
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()

	# Cámara
	gluLookAt(0, 0, 6, 0, 0, 0, 0, 1, 0)

	# Rotación
	glRotatef(angle, 0, 1, 0)

	# Dibujar malla de esfera
	glColor3f(0.0, 0.0, 0.0)
	glLineWidth(1.5)

	quad = gluNewQuadric()
	gluQuadricDrawStyle(quad, GLU_LINE)  # ← Dibujo en malla
	gluSphere(quad, 1.5, 20, 20)

	glutSwapBuffers()
	angle += 0.5

def reshape(w, h):
	glViewport(0, 0, w, h)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(45, w / h, 1, 100)
	glMatrixMode(GL_MODELVIEW)

def timer(value):
	glutPostRedisplay()
	glutTimerFunc(16, timer, 0)

def main():
	glutInit()
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
	glutInitWindowSize(600, 600)
	glutCreateWindow(b"Esfera 3D en forma de malla (wireframe)")
	init()
	glutDisplayFunc(display)
	glutReshapeFunc(reshape)
	glutTimerFunc(0, timer, 0)
	glutMainLoop()

if __name__ == "__main__":
	main()