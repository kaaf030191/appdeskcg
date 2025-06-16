"""
crear un cubo con 8 puntos en python con pyOpenGL en el plano X, Y y Z

dale bordes a las vértices para ver mejor la perspectiva

dale colores a cada cara

ahora agrega los ejes X, Y y Z
"""

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Vértices del cubo
vertices = [
	[-1, -1, -1],  # 0
	[ 1, -1, -1],  # 1
	[ 1,  1, -1],  # 2
	[-1,  1, -1],  # 3
	[-1, -1,  1],  # 4
	[ 1, -1,  1],  # 5
	[ 1,  1,  1],  # 6
	[-1,  1,  1]   # 7
]

# Caras del cubo (índices de vértices)
caras = [
	[0, 1, 2, 3],  # trasera
	[4, 5, 6, 7],  # delantera
	[0, 1, 5, 4],  # inferior
	[3, 2, 6, 7],  # superior
	[1, 2, 6, 5],  # derecha
	[0, 3, 7, 4]   # izquierda
]

# Aristas (para los bordes del cubo)
aristas = [
	[0, 1], [1, 2], [2, 3], [3, 0],
	[4, 5], [5, 6], [6, 7], [7, 4],
	[0, 4], [1, 5], [2, 6], [3, 7]
]

# Colores para cada cara (R, G, B)
colores = [
	(1.0, 0.0, 0.0),  # Rojo
	(0.0, 1.0, 0.0),  # Verde
	(0.0, 0.0, 1.0),  # Azul
	(1.0, 1.0, 0.0),  # Amarillo
	(1.0, 0.0, 1.0),  # Magenta
	(0.0, 1.0, 1.0)   # Cyan
]

def draw_cube():
	# Dibujar caras con colores
	glBegin(GL_QUADS)
	for i, cara in enumerate(caras):
		glColor3fv(colores[i])  # Asigna color por cara
		for vertice in cara:
			glVertex3fv(vertices[vertice])
	glEnd()

	# Dibujar aristas (bordes)
	glColor3f(0.0, 0.0, 0.0)  # Negro
	glLineWidth(2.0)
	glBegin(GL_LINES)
	for arista in aristas:
		for vertice in arista:
			glVertex3fv(vertices[vertice])
	glEnd()

def draw_axes():
	glLineWidth(3.0)
	glBegin(GL_LINES)

	# Eje X (rojo)
	glColor3f(1.0, 0.0, 0.0)
	glVertex3f(0.0, 0.0, 0.0)
	glVertex3f(2.0, 0.0, 0.0)

	# Eje Y (verde)
	glColor3f(0.0, 1.0, 0.0)
	glVertex3f(0.0, 0.0, 0.0)
	glVertex3f(0.0, 2.0, 0.0)

	# Eje Z (azul)
	glColor3f(0.0, 0.0, 1.0)
	glVertex3f(0.0, 0.0, 0.0)
	glVertex3f(0.0, 0.0, 2.0)

	glEnd()

def display():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()
	glTranslatef(0.0, 0.0, -7)
	glRotatef(30, 1, 1, 0)

	draw_axes()  # 🔴🟢🔵 Dibuja los ejes XYZ
	draw_cube()  # 🧊 Dibuja el cubo

	glutSwapBuffers()

def init():
	glEnable(GL_DEPTH_TEST)
	glClearColor(0.95, 0.95, 0.95, 1.0)  # Fondo blanco suave

def reshape(w, h):
	glViewport(0, 0, w, h)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(45, w / h, 0.1, 50.0)
	glMatrixMode(GL_MODELVIEW)

def main():
	glutInit()
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)
	glutInitWindowSize(600, 600)
	glutCreateWindow(b"Cubo 3D con Colores - PyOpenGL")
	init()
	glutDisplayFunc(display)
	glutReshapeFunc(reshape)
	glutMainLoop()

if __name__ == "__main__":
	main()