"""
ejemplo de modelos de color digital con python y pyopengl.
"""

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import colorsys

# Color base en RGB (valores entre 0 y 1)
base_rgb = [0.7, 0.2, 0.4]  # Puedes cambiar este color

# Funciones para convertir a otros modelos
def rgb_to_cmy(rgb):
	return [1 - c for c in rgb]

def rgb_to_hsv(rgb):
	return colorsys.rgb_to_hsv(*rgb)

def hsv_to_rgb(hsv):
	return colorsys.hsv_to_rgb(*hsv)

# Dibuja un rectángulo de color
def draw_square(x, y, w, h, color):
	glColor3f(*color)
	glBegin(GL_QUADS)
	glVertex2f(x, y)
	glVertex2f(x + w, y)
	glVertex2f(x + w, y - h)
	glVertex2f(x, y - h)
	glEnd()

# Dibuja texto
def draw_label(text, x, y):
	glColor3f(0, 0, 0)
	glRasterPos2f(x, y)
	for ch in text:
		glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))

def display():
	glClear(GL_COLOR_BUFFER_BIT)

	# RGB
	draw_square(-0.9, 0.6, 0.5, 0.5, base_rgb)
	draw_label(f"RGB: {tuple(round(c,2) for c in base_rgb)}", -0.85, 0.05)

	# CMY
	cmy = rgb_to_cmy(base_rgb)
	draw_square(0.4, 0.6, 0.5, 0.5, cmy)
	draw_label(f"CMY: {tuple(round(c,2) for c in cmy)}", 0.45, 0.05)

	# HSV
	hsv = rgb_to_hsv(base_rgb)
	hsv_rgb = hsv_to_rgb(hsv)
	draw_square(-0.25, -0.3, 0.5, 0.5, hsv_rgb)
	draw_label(f"HSV: {tuple(round(c,2) for c in hsv)}", -0.2, -0.85)

	glFlush()

def main():
	glutInit()
	glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
	glutInitWindowSize(800, 600)
	glutCreateWindow(b"Modelos de Color: RGB, CMY, HSV")
	glClearColor(1, 1, 1, 1)
	glMatrixMode(GL_PROJECTION)
	gluOrtho2D(-1.0, 1.0, -1.0, 1.0)
	glutDisplayFunc(display)
	glutMainLoop()

if __name__ == "__main__":
	main()