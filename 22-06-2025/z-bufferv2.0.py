"""
Genera un código en python con PyOpenGL (Un ejemplo visual) donde se muestre 2 cubos que se solapan y donde el Z-buffer decide cuál se ve. "Aplica técnica de resterización Z-Buffer".
"""

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

def init():
	# Configuración inicial de OpenGL
	glEnable(GL_DEPTH_TEST)  # Habilita el Z-Buffer
	glDepthFunc(GL_LESS)     # Configura la función de profundidad
	
	# Configura la iluminación básica
	glEnable(GL_LIGHTING)
	glEnable(GL_LIGHT0)
	glLightfv(GL_LIGHT0, GL_POSITION, [1, 1, 1, 0])
	glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 1, 1, 1])
	glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1])
	
	glMatrixMode(GL_PROJECTION)
	gluPerspective(45, (800/600), 0.1, 50.0)
	glMatrixMode(GL_MODELVIEW)

def draw_cube(color, position):
	glPushMatrix()
	glTranslatef(*position)
	
	# Material properties
	glMaterialfv(GL_FRONT, GL_DIFFUSE, color)
	
	# Cara frontal
	glBegin(GL_QUADS)
	glNormal3f(0, 0, 1)
	glVertex3f(-1, -1, 1)
	glVertex3f(1, -1, 1)
	glVertex3f(1, 1, 1)
	glVertex3f(-1, 1, 1)
	glEnd()
	
	# Cara trasera
	glBegin(GL_QUADS)
	glNormal3f(0, 0, -1)
	glVertex3f(-1, -1, -1)
	glVertex3f(-1, 1, -1)
	glVertex3f(1, 1, -1)
	glVertex3f(1, -1, -1)
	glEnd()
	
	# Cara superior
	glBegin(GL_QUADS)
	glNormal3f(0, 1, 0)
	glVertex3f(-1, 1, -1)
	glVertex3f(-1, 1, 1)
	glVertex3f(1, 1, 1)
	glVertex3f(1, 1, -1)
	glEnd()
	
	# Cara inferior
	glBegin(GL_QUADS)
	glNormal3f(0, -1, 0)
	glVertex3f(-1, -1, -1)
	glVertex3f(1, -1, -1)
	glVertex3f(1, -1, 1)
	glVertex3f(-1, -1, 1)
	glEnd()
	
	# Cara derecha
	glBegin(GL_QUADS)
	glNormal3f(1, 0, 0)
	glVertex3f(1, -1, -1)
	glVertex3f(1, 1, -1)
	glVertex3f(1, 1, 1)
	glVertex3f(1, -1, 1)
	glEnd()
	
	# Cara izquierda
	glBegin(GL_QUADS)
	glNormal3f(-1, 0, 0)
	glVertex3f(-1, -1, -1)
	glVertex3f(-1, -1, 1)
	glVertex3f(-1, 1, 1)
	glVertex3f(-1, 1, -1)
	glEnd()
	
	glPopMatrix()

def main():
	pygame.init()
	display = (800, 600)
	pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
	pygame.display.set_caption("Z-Buffer: Cubos Solapados")
	
	init()
	
	# Posiciones de los cubos (se solaparán en el espacio 3D)
	cube1_pos = (0, 0, -5)
	cube2_pos = (0.5, 0.5, -4)  # Este cubo está más cerca de la cámara
	
	# Colores de los cubos (RGBA)
	cube1_color = (0.8, 0.2, 0.2, 1.0)  # Rojo
	cube2_color = (0.2, 0.2, 0.8, 1.0)  # Azul
	
	angle = 0
	
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				return
		
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		
		# Configura la vista
		glLoadIdentity()
		gluLookAt(3, 3, 3, 0, 0, -4, 0, 1, 0)
		
		# Rotación para mejor visualización
		glRotatef(angle, 0, 1, 0)
		angle += 0.5
		
		# Dibuja los cubos
		draw_cube(cube1_color, cube1_pos)
		draw_cube(cube2_color, cube2_pos)
		
		pygame.display.flip()
		pygame.time.wait(10)

if __name__ == "__main__":
	main()