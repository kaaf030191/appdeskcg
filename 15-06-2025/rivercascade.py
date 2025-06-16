"""
crea una función procedural 3D para representar el fuego, con python y pyopenGL

debe ser con partículas, corrige esa parte

varía este último código y genera un río

cambia los colores, y genera más realismo

cambiarlo por mallas

ponlo en modo de malla

generar una cascada

ahora genera la cascada pero con partículas
"""

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random
import sys

# Configuración de partículas
NUM_PARTICULAS = 1000
ALTURA_INICIAL = 5.0
VELOCIDAD_CAIDA = 0.08
RADIO_PARTICULA = 0.05

# Lista de partículas [x, y, z, velocidad_y]
particulas = []

def init_particles():
	for _ in range(NUM_PARTICULAS):
		x = random.uniform(-1.5, 1.5)
		y = random.uniform(0, ALTURA_INICIAL)
		z = random.uniform(-1.0, 1.0)
		vel_y = random.uniform(0.02, VELOCIDAD_CAIDA)
		particulas.append([x, y, z, vel_y])

def init():
	glClearColor(0.1, 0.1, 0.2, 1.0)
	glEnable(GL_DEPTH_TEST)
	glPointSize(3.0)

	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

	glEnable(GL_LIGHTING)
	glEnable(GL_LIGHT0)
	glLightfv(GL_LIGHT0, GL_POSITION, (5, 10, 10, 1))
	glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.6, 0.6, 1.0, 1.0))
	glEnable(GL_COLOR_MATERIAL)

	init_particles()

def display():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()
	gluLookAt(0, 2, 8, 0, 0, 0, 0, 1, 0)

	# Dibujar suelo
	glDisable(GL_LIGHTING)
	glColor3f(0.2, 0.5, 0.2)
	glBegin(GL_QUADS)
	glVertex3f(-5, -0.1, -5)
	glVertex3f(5, -0.1, -5)
	glVertex3f(5, -0.1, 5)
	glVertex3f(-5, -0.1, 5)
	glEnd()
	glEnable(GL_LIGHTING)

	# Dibujar partículas
	glColor4f(0.3, 0.5, 1.0, 0.8)
	for p in particulas:
		glPushMatrix()
		glTranslatef(p[0], p[1], p[2])
		glutSolidSphere(RADIO_PARTICULA, 8, 8)
		glPopMatrix()

	glutSwapBuffers()

def update(value):
	for p in particulas:
		p[1] -= p[3]  # Caída

		if p[1] <= -0.1:  # Reiniciar si toca el suelo
			p[0] = random.uniform(-1.5, 1.5)
			p[1] = ALTURA_INICIAL
			p[2] = random.uniform(-1.0, 1.0)
			p[3] = random.uniform(0.02, VELOCIDAD_CAIDA)

	glutPostRedisplay()
	glutTimerFunc(16, update, 0)

def reshape(w, h):
	glViewport(0, 0, w, h)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(45.0, w / float(h), 1.0, 100.0)
	glMatrixMode(GL_MODELVIEW)

def main():
	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
	glutInitWindowSize(800, 600)
	glutCreateWindow(b"Cascada con Particulas - PyOpenGL")
	init()
	glutDisplayFunc(display)
	glutReshapeFunc(reshape)
	glutTimerFunc(0, update, 0)
	glutMainLoop()

if __name__ == "__main__":
	main()