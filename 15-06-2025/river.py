"""
crea una función procedural 3D para representar el fuego, con python y pyopenGL

debe ser con partículas, corrige esa parte

varía este último código y genera un río

cambia los colores, y genera más realismo
"""

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random
import math
import sys

# Número de partículas de agua
NUM_PARTICULAS = 5000

class ParticulaAgua:
	def __init__(self):
		self.reset()

	def reset(self):
		self.x = random.uniform(-4.0, 4.0)
		self.z = random.uniform(-0.6, 0.6)
		self.y = math.sin(self.x * 2) * 0.03
		self.vx = random.uniform(0.01, 0.02)
		self.vz = random.uniform(-0.002, 0.002)
		self.tiempo = random.uniform(0, 2 * math.pi)
		self.size = random.uniform(0.04, 0.07)
		self.bril = random.uniform(0.7, 1.0)

	def update(self):
		self.x += self.vx
		self.z += self.vz
		self.tiempo += 0.1
		self.y = math.sin(self.tiempo + self.x * 0.5) * 0.05
		if self.x > 4.2:
			self.reset()
			self.x = -4.0

agua = [ParticulaAgua() for _ in range(NUM_PARTICULAS)]

def init():
	glClearColor(0.1, 0.1, 0.15, 1.0)  # Noche o sombra
	glEnable(GL_DEPTH_TEST)
	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	glEnable(GL_POINT_SMOOTH)
	glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)

	glEnable(GL_LIGHTING)
	glEnable(GL_LIGHT0)
	glLightfv(GL_LIGHT0, GL_POSITION, (1, 3, 2, 1))
	glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.6, 0.6, 0.9, 1.0))
	glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.4, 1.0))

def draw_particula(p):
	glPushMatrix()
	glTranslatef(p.x, p.y, p.z)

	# Azul profundo con reflejo tenue
	glColor4f(0.1 * p.bril, 0.4 * p.bril, 0.9, 0.55)
	glutSolidSphere(p.size, 10, 10)
	glPopMatrix()

def display():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()

	gluLookAt(0, 1.2, 6, 0, 0, 0, 0, 1, 0)

	for p in agua:
		p.update()
		draw_particula(p)

	glutSwapBuffers()

def reshape(w, h):
	glViewport(0, 0, w, h)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(45.0, float(w) / float(h), 1.0, 50.0)
	glMatrixMode(GL_MODELVIEW)

def timer(v):
	glutPostRedisplay()
	glutTimerFunc(16, timer, 0)  # ~60 FPS

def main():
	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
	glutInitWindowSize(800, 600)
	glutCreateWindow(b"Rio Procedural Realista con PyOpenGL")
	init()
	glutDisplayFunc(display)
	glutReshapeFunc(reshape)
	glutTimerFunc(0, timer, 0)
	glutMainLoop()

if __name__ == "__main__":
	main()