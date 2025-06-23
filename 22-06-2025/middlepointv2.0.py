from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Centro y radio de la circunferencia
x0, y0 = 0, 10
r = 10

# Ventana
width, height = 400, 400

def draw_axes():
	glColor3f(1, 1, 1)  # blanco
	glBegin(GL_LINES)
	# Eje X
	glVertex2f(-width//2, 0)
	glVertex2f(width//2, 0)
	# Eje Y
	glVertex2f(0, -height//2)
	glVertex2f(0, height//2)
	glEnd()

def draw_pixel(x, y):
	glBegin(GL_POINTS)
	glVertex2f(x, y)
	glEnd()

def midpoint_circle():
	x = 0
	y = r
	p = 1 - r

	while x <= y:
		# Dibujar los puntos del primer octante y sus simétricos en el círculo centrado en (x0, y0)
		# Solo consideramos el primer cuadrante (y >= 0, x >= 0)
		px = x + x0
		py = y + y0

		# Dibujamos los puntos en el primer octante (x,y) y sus reflejos sobre las líneas de simetría
		draw_pixel(px, py)         # (x, y)
		draw_pixel(py - y0 + x0, px - x0 + y0)  # (y, x) ajustado al centro

		# Actualizar el parámetro de decisión
		if p < 0:
			p += 2 * x + 3
		else:
			p += 2 * (x - y) + 5
			y -= 1
		x += 1

def display():
	glClear(GL_COLOR_BUFFER_BIT)
	draw_axes()
	glColor3f(1, 0, 0)  # rojo para la circunferencia
	midpoint_circle()
	glFlush()

def reshape(w, h):
	glViewport(0, 0, w, h)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	# Ajustamos la ventana para que el centro (0,10) quede visible
	gluOrtho2D(-width//2, width//2, -height//2, height//2)
	glMatrixMode(GL_MODELVIEW)

def main():
	glutInit()
	glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
	glutInitWindowSize(width, height)
	glutInitWindowPosition(100, 100)
	glutCreateWindow(b"Circunferencia con Algoritmo de Punto Medio")
	glClearColor(0, 0, 0, 0)  # fondo negro
	glColor3f(1, 1, 1)
	glPointSize(3)
	glutDisplayFunc(display)
	glutReshapeFunc(reshape)
	glutMainLoop()

if __name__ == "__main__":
	main()