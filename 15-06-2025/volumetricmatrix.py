from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Tamaño de la grilla de voxeles
grid_size = 3
angle = 0  # Rotación global
local_angle = 0  # Rotación local

def draw_voxel(x, y, z, size=0.9):
	"""Dibuja una esfera (voxel) con rotación local en la posición (x, y, z)"""
	half = size / 2
	glPushMatrix()
	glTranslatef(x, y, z)

	# Rotación local individual (basada en posición para variación)
	glRotatef(local_angle + (x + y + z) * 10, 1, 0, 0)

	glScalef(size, size, size)
	glutWireSphere(1.0, 20, 20)
	glPopMatrix()

def init():
	glClearColor(0.1, 0.1, 0.1, 1.0)
	glEnable(GL_DEPTH_TEST)
	glEnable(GL_COLOR_MATERIAL)
	glEnable(GL_LIGHTING)
	glEnable(GL_LIGHT0)
	glLightfv(GL_LIGHT0, GL_POSITION,  (5, 5, 5, 1))
	glLightfv(GL_LIGHT0, GL_AMBIENT,   (0.1, 0.1, 0.1, 1))
	glLightfv(GL_LIGHT0, GL_DIFFUSE,   (0.8, 0.8, 0.8, 1))

def display():
	global angle, local_angle
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()
	glTranslatef(0, 0, -10)

	# Rotación general de toda la escena
	glRotatef(angle, 1, 1, 0)

	# Dibuja una cuadrícula 3D de voxeles (esferas)
	for x in range(-grid_size, grid_size + 1):
		for y in range(-grid_size, grid_size + 1):
			for z in range(-grid_size, grid_size + 1):
				if (x + y + z) % 2 == 0:  # Patrón de volumen
					glColor3f((x + grid_size) / 6.0, (y + grid_size) / 6.0, (z + grid_size) / 6.0)
					draw_voxel(x, y, z, size=0.4)

	glutSwapBuffers()
	angle += 0.3
	local_angle += 1.0  # velocidad de rotación individual

def reshape(w, h):
	glViewport(0, 0, w, h)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(45.0, float(w) / float(h), 1.0, 100.0)
	glMatrixMode(GL_MODELVIEW)

def main():
	glutInit()
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
	glutInitWindowSize(800, 600)
	glutCreateWindow(b"Modelo Geometrico Volumetrico con Voxeles")
	init()
	glutDisplayFunc(display)
	glutIdleFunc(display)
	glutReshapeFunc(reshape)
	glutMainLoop()

if __name__ == "__main__":
	main()