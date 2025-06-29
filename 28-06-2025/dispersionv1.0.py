from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import sys

# Dimensiones de la ventana
width, height = 800, 600

# Rotación de la cámara
angle_x = 30
angle_y = 30

# Cargar datos desde archivo TXT
def cargar_datos(nombre_archivo):
	datos = []
	with open(nombre_archivo, 'r') as archivo:
		for linea in archivo:
			try:
				temp, humedad, precip = map(float, linea.strip().split(';'))
				datos.append([temp, humedad, precip])
			except:
				pass  # Ignora líneas mal formateadas
	return np.array(datos)

# Cargar datos
datos = cargar_datos("data.txt")

def init():
	glClearColor(0.1, 0.1, 0.1, 1.0)
	glEnable(GL_DEPTH_TEST)
	glPointSize(5.0)

def draw_text(x, y, texto):
	glMatrixMode(GL_PROJECTION)
	glPushMatrix()
	glLoadIdentity()
	gluOrtho2D(0, width, 0, height)
	
	glMatrixMode(GL_MODELVIEW)
	glPushMatrix()
	glLoadIdentity()

	glColor3f(1.0, 1.0, 1.0)
	glRasterPos2f(x, y)
	for ch in texto:
		glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))
	
	glPopMatrix()
	glMatrixMode(GL_PROJECTION)
	glPopMatrix()
	glMatrixMode(GL_MODELVIEW)

def draw_axes():
	glLineWidth(2.0)
	glBegin(GL_LINES)
	# X (Temperatura) - rojo
	glColor3f(1.0, 0.0, 0.0)
	glVertex3f(0, 0, 0)
	glVertex3f(50, 0, 0)
	# Y (Humedad) - verde
	glColor3f(0.0, 1.0, 0.0)
	glVertex3f(0, 0, 0)
	glVertex3f(0, 100, 0)
	# Z (Precipitación) - azul
	glColor3f(0.0, 0.5, 1.0)
	glVertex3f(0, 0, 0)
	glVertex3f(0, 0, 300)
	glEnd()

def display():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()

	# Posicionar la cámara
	glTranslatef(-20, -50, -300)
	glRotatef(angle_x, 1, 0, 0)
	glRotatef(angle_y, 0, 1, 0)

	# Dibujar ejes
	draw_axes()

	# Dibujar puntos
	glBegin(GL_POINTS)
	for temp, humedad, precip in datos:
		# Normalización de valores
		r = min(temp / 50.0, 1.0)
		g = min(humedad / 100.0, 1.0)
		b = min(precip / 300.0, 1.0)
		glColor3f(r, g, b)
		glVertex3f(temp, humedad, precip)
	glEnd()

	# Dibujar leyenda
	draw_text(10, height - 20, "Ejes:")
	draw_text(10, height - 40, "X = TEMPERATURA (°C) [Rojo]")
	draw_text(10, height - 60, "Y = HUMEDAD RELATIVA (%) [Verde]")
	draw_text(10, height - 80, "Z = PRECIPITACIÓN (mm) [Azul]")
	glutSwapBuffers()

def reshape(w, h):
	global width, height
	width = w
	height = h
	glViewport(0, 0, w, h)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(45.0, float(w) / float(h), 1.0, 1000.0)
	glMatrixMode(GL_MODELVIEW)

def special_keys(key, x, y):
	global angle_x, angle_y
	if key == GLUT_KEY_UP:
		angle_x += 5
	elif key == GLUT_KEY_DOWN:
		angle_x -= 5
	elif key == GLUT_KEY_LEFT:
		angle_y -= 5
	elif key == GLUT_KEY_RIGHT:
		angle_y += 5
	glutPostRedisplay()

def main():
	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
	glutInitWindowSize(width, height)
	glutCreateWindow(b"Nube de puntos climaticos (color por variable)")
	init()
	glutDisplayFunc(display)
	glutReshapeFunc(reshape)
	glutSpecialFunc(special_keys)
	glutMainLoop()

if __name__ == "__main__":
	main()