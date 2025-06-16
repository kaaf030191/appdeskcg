"""
crea una función procedural 3D para representar el fuego, con python y pyopenGL

debe ser con partículas, corrige esa parte

varía este último código y genera un río

cambia los colores, y genera más realismo

cambiarlo por mallas

ponlo en modo de malla

generar una cascada
"""

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import math

# Dimensiones
ancho_cascada = 20
alto_cascada = 30
espaciado = 0.2
tiempo = 0.0

def init():
	glClearColor(0.1, 0.1, 0.2, 1.0)
	glEnable(GL_DEPTH_TEST)
	glShadeModel(GL_SMOOTH)

	glEnable(GL_LIGHTING)
	glEnable(GL_LIGHT0)
	glLightfv(GL_LIGHT0, GL_POSITION, (5, 10, 10, 1))
	glLightfv(GL_LIGHT0, GL_AMBIENT, (0.1, 0.1, 0.2, 1.0))
	glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.6, 0.6, 1.0, 1.0))

	glEnable(GL_COLOR_MATERIAL)
	glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

	# Modo malla
	glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

def altura_cascada(x, y, t):
	"""Simula flujo de agua en caída con ondas animadas"""
	return 0.2 * math.sin(0.4 * x + t + y * 0.2)

def draw_cascada(t):
	glColor3f(0.3, 0.5, 1.0)
	for y in range(0, alto_cascada):
		glBegin(GL_TRIANGLE_STRIP)
		for x in range(-ancho_cascada//2, ancho_cascada//2 + 1):
			h1 = altura_cascada(x * espaciado, y * espaciado, t)
			h2 = altura_cascada(x * espaciado, (y + 1) * espaciado, t)
			
			glVertex3f(x * espaciado, -y * espaciado, h1)
			glVertex3f(x * espaciado, -(y + 1) * espaciado, h2)
		glEnd()

def draw_terreno():
	glColor3f(0.1, 0.5, 0.2)
	glBegin(GL_QUADS)
	glVertex3f(-3, 0.1, -1)
	glVertex3f(3, 0.1, -1)
	glVertex3f(3, 0.1, 1)
	glVertex3f(-3, 0.1, 1)
	glEnd()

def display():
	global tiempo
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()

	# Cámara
	gluLookAt(0, 3, 12, 0, -2, 0, 0, 1, 0)

	# Terreno superior
	draw_terreno()

	# Dibujar cascada animada
	draw_cascada(tiempo)

	glutSwapBuffers()
	tiempo += 0.05

def reshape(w, h):
	glViewport(0, 0, w, h)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(45.0, float(w)/float(h), 1.0, 100.0)
	glMatrixMode(GL_MODELVIEW)

def timer(v):
	glutPostRedisplay()
	glutTimerFunc(16, timer, 0)

def main():
	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
	glutInitWindowSize(800, 600)
	glutCreateWindow(b"Cascada Procedural - Modo Malla - PyOpenGL")
	init()
	glutDisplayFunc(display)
	glutReshapeFunc(reshape)
	glutTimerFunc(0, timer, 0)
	glutMainLoop()

if __name__ == "__main__":
	main()