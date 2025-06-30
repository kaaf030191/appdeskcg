import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Puntos de control para la curva Bézier cúbica en 3D
control_points = np.array([
	[-2.0, -1.0, 0.0],  # P0
	[-1.0, 2.0, 1.0],   # P1
	[1.0, 2.0, -1.0],   # P2
	[2.0, -1.0, 0.0]    # P3
], dtype=np.float32)

# Número de puntos a generar en la curva
num_points = 100

def init():
	glClearColor(0.0, 0.0, 0.0, 1.0)
	glEnable(GL_DEPTH_TEST)
	glPointSize(5.0)
	glLineWidth(2.0)

def draw_control_points():
	glColor3f(1.0, 0.0, 0.0)  # Rojo para los puntos de control
	glBegin(GL_POINTS)
	for point in control_points:
		glVertex3fv(point)
	glEnd()
	
	# Dibujar líneas entre los puntos de control
	glColor3f(0.5, 0.5, 0.5)  # Gris para las líneas de control
	glBegin(GL_LINE_STRIP)
	for point in control_points:
		glVertex3fv(point)
	glEnd()

def bezier_curve(t, points):
	"""Calcula un punto en la curva Bézier para un parámetro t dado"""
	# Fórmula de la curva Bézier cúbica:
	# B(t) = (1-t)³P0 + 3(1-t)²tP1 + 3(1-t)t²P2 + t³P3
	t2 = t * t
	t3 = t2 * t
	mt = 1 - t
	mt2 = mt * mt
	mt3 = mt2 * mt
	
	point = (mt3 * points[0] + 
			3 * mt2 * t * points[1] + 
			3 * mt * t2 * points[2] + 
			t3 * points[3])
	
	return point

def draw_bezier_curve():
	glColor3f(0.0, 1.0, 1.0)  # Cian para la curva
	glBegin(GL_LINE_STRIP)
	
	for i in range(num_points + 1):
		t = i / num_points
		point = bezier_curve(t, control_points)
		glVertex3fv(point)
	
	glEnd()

def display():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()
	
	# Configurar la vista
	gluLookAt(3, 3, 3,  # posición de la cámara
			0, 0, 0,  # punto al que mira
			0, 1, 0)  # vector de arriba
	
	# Dibujar los ejes coordenados
	glBegin(GL_LINES)
	# Eje X (rojo)
	glColor3f(1.0, 0.0, 0.0)
	glVertex3f(0.0, 0.0, 0.0)
	glVertex3f(3.0, 0.0, 0.0)
	# Eje Y (verde)
	glColor3f(0.0, 1.0, 0.0)
	glVertex3f(0.0, 0.0, 0.0)
	glVertex3f(0.0, 3.0, 0.0)
	# Eje Z (azul)
	glColor3f(0.0, 0.0, 1.0)
	glVertex3f(0.0, 0.0, 0.0)
	glVertex3f(0.0, 0.0, 3.0)
	glEnd()
	
	# Dibujar los elementos de la curva
	draw_control_points()
	draw_bezier_curve()
	
	glutSwapBuffers()

def reshape(w, h):
	glViewport(0, 0, w, h)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(45, w/h, 0.1, 50.0)
	glMatrixMode(GL_MODELVIEW)

def main():
	glutInit()
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
	glutInitWindowSize(800, 600)
	glutCreateWindow(b"Curva Bezier Cubica 3D")
	
	init()
	
	glutDisplayFunc(display)
	glutReshapeFunc(reshape)
	
	glutMainLoop()

if __name__ == "__main__":
	main()