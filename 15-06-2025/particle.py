"""
crea una función procedural 3D para representar el fuego, con python y pyopenGL

debe ser con partículas, corrige esa parte
"""

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random
import time
import sys

# Cantidad de partículas
NUM_PARTICULAS = 1000

# Clase de partícula
class Particula:
	def __init__(self):
		self.reset()

	def reset(self):
		self.x = random.uniform(-0.2, 0.2)
		self.y = 0.0
		self.z = random.uniform(-0.2, 0.2)
		self.vy = random.uniform(0.01, 0.03)
		self.size = random.uniform(0.05, 0.1)
		self.life = 1.0  # vida entre 0 y 1
		self.decay = random.uniform(0.005, 0.01)

	def update(self):
		self.y += self.vy
		self.life -= self.decay
		if self.life <= 0.0:
			self.reset()

# Lista de partículas
particulas = [Particula() for _ in range(NUM_PARTICULAS)]

def init():
	glClearColor(0.05, 0.05, 0.1, 1.0)
	glEnable(GL_DEPTH_TEST)
	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	glEnable(GL_POINT_SMOOTH)
	glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)

def draw_particula(p):
	glPushMatrix()
	glTranslatef(p.x, p.y, p.z)

	# Color fuego: de rojo intenso a amarillo tenue
	r = 1.0
	g = p.life  # más vida = más verde
	b = 0.0
	a = p.life  # transparencia
	glColor4f(r, g, b, a)

	glutSolidSphere(p.size, 8, 8)
	glPopMatrix()

def display():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()

	# Cámara
	gluLookAt(0, 1, 5, 0, 1, 0, 0, 1, 0)

	# Dibujar partículas
	for p in particulas:
		p.update()
		draw_particula(p)

	glutSwapBuffers()

def reshape(w, h):
	glViewport(0, 0, w, h)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(45, w / float(h), 1, 50)
	glMatrixMode(GL_MODELVIEW)

def timer(v):
	glutPostRedisplay()
	glutTimerFunc(16, timer, 0)  # 60 FPS

def main():
	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
	glutInitWindowSize(800, 600)
	glutCreateWindow(b"Fuego Procedural 3D con Particulas")
	init()
	glutDisplayFunc(display)
	glutReshapeFunc(reshape)
	glutTimerFunc(0, timer, 0)
	glutMainLoop()

if __name__ == "__main__":
	main()