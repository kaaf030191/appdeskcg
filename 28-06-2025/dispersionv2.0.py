from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import sys

# Tamaño de ventana
width, height = 800, 600

# Ángulos de rotación
angle_x = 30
angle_y = 30

# Cargar datos desde archivo .txt
def cargar_datos(nombre_archivo):
	datos = []
	with open(nombre_archivo, 'r') as archivo:
		for linea in archivo:
			try:
				temp, humedad, precip = map(float, linea.strip().split(';'))
				datos.append([temp, humedad, precip])
			except:
				pass  # Ignorar líneas mal formateadas
	return np.array(datos)

datos = cargar_datos("data.txt")

def init():
	glClearColor(0.1, 0.1, 0.1, 1.0)
	glEnable(GL_DEPTH_TEST)
	glPointSize(6.0)

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
	# X - Temperatura (rojo)
	glColor3f(1.0, 0.0, 0.0)
	glVertex3f(0, 0, 0)
	glVertex3f(50, 0, 0)
	# Y - Humedad (verde)
	glColor3f(0.0, 1.0, 0.0)
	glVertex3f(0, 0, 0)
	glVertex3f(0, 100, 0)
	# Z - Precipitación (azul)
	glColor3f(0.0, 0.5, 1.0)
	glVertex3f(0, 0, 0)
	glVertex3f(0, 0, 300)
	glEnd()

def display():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()

	# Posicionar cámara
	glTranslatef(-30, -60, -400)
	glRotatef(angle_x, 1, 0, 0)
	glRotatef(angle_y, 0, 1, 0)

	# Ejes de referencia
	draw_axes()

	# Dibujar puntos por variable
	glBegin(GL_POINTS)
	for temp, humedad, precip in datos:
		# Punto rojo: temperatura en eje X
		glColor3f(1.0, 0.0, 0.0)
		glVertex3f(temp, 0, 0)

		# Punto verde: humedad en eje Y
		glColor3f(0.0, 1.0, 0.0)
		glVertex3f(0, humedad, 0)

		# Punto azul: precipitación en eje Z
		glColor3f(0.0, 0.0, 1.0)
		glVertex3f(0, 0, precip)
	glEnd()

	# Dibujar leyenda
	draw_text(10, height - 20, "Cada variable tiene su color y eje:")
	draw_text(10, height - 40, "🔴 TEMPERATURA PROMEDIO (°C) → eje X")
	draw_text(10, height - 60, "🟢 HUMEDAD RELATIVA PROMEDIO (%) → eje Y")
	draw_text(10, height - 80, "🔵 PRECIPITACIÓN (mm) → eje Z")

	glutSwapBuffers()

def reshape(w, h):
	global width, height
	width = w
	height = h
	glViewport(0, 0, w, h)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(45.0, float(w)/float(h), 1.0, 1000.0)
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
	glutCreateWindow(b"Nube de puntos por variable (colores separados)")
	init()
	glutDisplayFunc(display)
	glutReshapeFunc(reshape)
	glutSpecialFunc(special_keys)
	glutMainLoop()

if __name__ == "__main__":
	main()