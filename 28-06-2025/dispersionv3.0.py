from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import sys

# Tamaño ventana
width, height = 800, 600

# Ángulo de rotación inicial
angle_x = 30
angle_y = 30

# Cargar datos desde archivo
def cargar_datos(nombre_archivo):
	datos = []
	with open(nombre_archivo, 'r') as archivo:
		for linea in archivo:
			try:
				temp, humedad, precip = map(float, linea.strip().split(';'))
				datos.append([temp, humedad, precip])
			except:
				pass
	return np.array(datos)

datos = cargar_datos("data.txt")

# Normalizar los datos para que entren al rango 0–1
def normalizar(val, min_val, max_val):
	return (val - min_val) / (max_val - min_val) if max_val > min_val else 0

def init():
	glClearColor(0.0, 0.0, 0.0, 1.0)
	glEnable(GL_DEPTH_TEST)
	glPointSize(5.0)

def display():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()

	# Cámara
	glTranslatef(-0.5, -0.5, -3)  # Ajuste para ver bien los datos normalizados
	glRotatef(angle_x, 1, 0, 0)
	glRotatef(angle_y, 0, 1, 0)

	# Obtener máximos y mínimos para normalizar
	temp_vals = datos[:, 0]
	hum_vals = datos[:, 1]
	prec_vals = datos[:, 2]

	min_temp, max_temp = np.min(temp_vals), np.max(temp_vals)
	min_hum, max_hum = np.min(hum_vals), np.max(hum_vals)
	min_prec, max_prec = np.min(prec_vals), np.max(prec_vals)

	glBegin(GL_POINTS)
	for temp, humedad, precip in datos:
		# Normalizar coordenadas
		x = normalizar(temp, min_temp, max_temp)
		y = normalizar(humedad, min_hum, max_hum)
		z = normalizar(precip, min_prec, max_prec)

		# Color (puedes usar temp/hum/prec también como r/g/b)
		glColor3f(x, y, z)  # codifica color por las 3 variables

		# Dibujar punto
		glVertex3f(x, y, z)
	glEnd()

	glutSwapBuffers()

def reshape(w, h):
	global width, height
	width, height = w, h
	glViewport(0, 0, w, h)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(45.0, float(w)/float(h), 0.1, 100.0)
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
	glutCreateWindow(b"Dispersion 3D de clima")
	init()
	glutDisplayFunc(display)
	glutReshapeFunc(reshape)
	glutSpecialFunc(special_keys)
	glutMainLoop()

if __name__ == "__main__":
	main()