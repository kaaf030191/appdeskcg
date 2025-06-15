"""
ejemplo de fundamentos del color y percepción visual mediante Python con OpenGL.
"""

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Lista de cuadros con color y posición
squares = [
	{"pos": (-0.7, 0.5), "color": (1.0, 0.0, 0.0), "label": "Rojo"},
	{"pos": (-0.3, 0.5), "color": (0.0, 1.0, 0.0), "label": "Verde"},
	{"pos": ( 0.1, 0.5), "color": (0.0, 0.0, 1.0), "label": "Azul"},
	{"pos": (-0.5, 0.0), "color": (1.0, 1.0, 0.0), "label": "Amarillo"},
	{"pos": (-0.1, 0.0), "color": (0.0, 1.0, 1.0), "label": "Cian"},
	{"pos": ( 0.3, 0.0), "color": (1.0, 0.0, 1.0), "label": "Magenta"},
	{"pos": (-0.7, -0.5), "color": (0.5, 0.5, 0.5), "label": "Gris"},
	{"pos": (-0.3, -0.5), "color": (1.0, 1.0, 1.0), "label": "Blanco"},
	{"pos": ( 0.1, -0.5), "color": (0.0, 0.0, 0.0), "label": "Negro"},
]

def draw_square(x, y, color):
	glColor3f(*color)
	glBegin(GL_QUADS)
	glVertex2f(x, y)
	glVertex2f(x + 0.2, y)
	glVertex2f(x + 0.2, y - 0.2)
	glVertex2f(x, y - 0.2)
	glEnd()

def draw_label(text, x, y):
	glColor3f(0.1, 0.1, 0.1)
	glRasterPos2f(x, y)
	for ch in text:
		glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(ch))

def display():
	glClear(GL_COLOR_BUFFER_BIT)
	
	# Fondo dividido para contrastes (gris claro y oscuro)
	glBegin(GL_QUADS)
	glColor3f(0.9, 0.9, 0.9)
	glVertex2f(-1, 1)
	glVertex2f(0, 1)
	glVertex2f(0, -1)
	glVertex2f(-1, -1)

	glColor3f(0.2, 0.2, 0.2)
	glVertex2f(0, 1)
	glVertex2f(1, 1)
	glVertex2f(1, -1)
	glVertex2f(0, -1)
	glEnd()

	# Dibujar cuadrados de color con etiquetas
	for sq in squares:
		draw_square(sq["pos"][0], sq["pos"][1], sq["color"])
		draw_label(sq["label"], sq["pos"][0], sq["pos"][1] - 0.25)

	glFlush()

def main():
	glutInit()
	glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
	glutInitWindowSize(800, 600)
	glutCreateWindow(b"Fundamentos del Color y Percepcion Visual")
	glClearColor(1, 1, 1, 1)
	glMatrixMode(GL_PROJECTION)
	gluOrtho2D(-1, 1, -1, 1)
	glutDisplayFunc(display)
	glutMainLoop()

if __name__ == "__main__":
	main()