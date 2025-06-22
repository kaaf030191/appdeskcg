import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import numpy as np

def iniciar_luz_phong():
	glEnable(GL_LIGHTING)
	glEnable(GL_LIGHT0)
	glEnable(GL_LIGHT1)
	
	# Luz principal (foco frontal)
	glLightfv(GL_LIGHT0, GL_POSITION, [0, 3, 5, 1])
	glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1])
	glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.9, 0.9, 0.9, 1])
	glLightfv(GL_LIGHT0, GL_SPECULAR, [1, 1, 1, 1])
	glLightf(GL_LIGHT0, GL_SPOT_CUTOFF, 30)
	glLightf(GL_LIGHT0, GL_SPOT_EXPONENT, 20)
	glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, [0, -0.5, -1])
	
	# Luz ambiental (cielo)
	glLightfv(GL_LIGHT1, GL_POSITION, [0, 10, 0, 0])
	glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.4, 0.4, 0.4, 1])
	glLightfv(GL_LIGHT1, GL_SPECULAR, [0.3, 0.3, 0.3, 1])
	
	glEnable(GL_COLOR_MATERIAL)
	glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
	glEnable(GL_NORMALIZE)

def aplicar_material(color, especular, brillo, emision=[0,0,0,1]):
	glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [c*0.2 for c in color] + [1])
	glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, color + [1])
	glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, especular + [1])
	glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, emision)
	glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, brillo)

def dibujar_rectangulo(p1, p2, p3, p4):
	normal = np.cross(np.array(p2)-np.array(p1), np.array(p3)-np.array(p1))
	normal = normal / np.linalg.norm(normal)
	
	glBegin(GL_QUADS)
	glNormal3fv(normal)
	glVertex3fv(p1)
	glVertex3fv(p2)
	glVertex3fv(p3)
	glVertex3fv(p4)
	glEnd()

def dibujar_cilindro(radius, height, slices=16):
	glPushMatrix()
	glRotatef(90, 1, 0, 0)
	
	# Lados
	glBegin(GL_QUAD_STRIP)
	for i in range(slices+1):
		angle = 2 * math.pi * i / slices
		x = radius * math.cos(angle)
		z = radius * math.sin(angle)
		normal = [x, 0, z]
		
		glNormal3fv(normal)
		glVertex3f(x, height/2, z)
		glVertex3f(x, -height/2, z)
	glEnd()
	
	# Tapas
	glBegin(GL_POLYGON)
	glNormal3f(0, 1, 0)
	for i in range(slices, -1, -1):
		angle = 2 * math.pi * i / slices
		glVertex3f(radius * math.cos(angle), height/2, radius * math.sin(angle))
	glEnd()
	
	glBegin(GL_POLYGON)
	glNormal3f(0, -1, 0)
	for i in range(slices+1):
		angle = 2 * math.pi * i / slices
		glVertex3f(radius * math.cos(angle), -height/2, radius * math.sin(angle))
	glEnd()
	
	glPopMatrix()

def dibujar_rueda(pos_x, pos_y, pos_z):
	glPushMatrix()
	glTranslatef(pos_x, pos_y, pos_z)
	
	# Llanta
	aplicar_material([0.1, 0.1, 0.1], [0.5, 0.5, 0.5], 50)
	dibujar_cilindro(0.3, 0.2)
	
	# Borde cromado
	aplicar_material([0.7, 0.7, 0.7], [0.9, 0.9, 0.9], 100)
	dibujar_cilindro(0.35, 0.21)
	dibujar_cilindro(0.25, 0.21)
	
	# Rayos
	aplicar_material([0.3, 0.3, 0.3], [0.5, 0.5, 0.5], 30)
	for i in range(5):
		glRotatef(72, 0, 1, 0)
		glBegin(GL_QUADS)
		glVertex3f(0.15, 0.11, 0.02)
		glVertex3f(0.15, -0.11, 0.02)
		glVertex3f(0.25, -0.11, 0.02)
		glVertex3f(0.25, 0.11, 0.02)
		glEnd()
	
	glPopMatrix()

def dibujar_auto():
	# Carrocería principal (color rojo metálico)
	aplicar_material([0.8, 0.1, 0.1], [0.7, 0.6, 0.6], 80)
	
	# Base del auto
	dibujar_rectangulo([-1.5, 0, 2], [1.5, 0, 2], [1.5, 0, -3], [-1.5, 0, -3])
	dibujar_rectangulo([-1.5, 0.5, 2], [1.5, 0.5, 2], [1.5, 0, 2], [-1.5, 0, 2])
	dibujar_rectangulo([-1.5, 0.5, -3], [1.5, 0.5, -3], [1.5, 0, -3], [-1.5, 0, -3])
	
	# Laterales
	dibujar_rectangulo([-1.5, 0.5, 2], [-1.5, 0.5, -3], [-1.5, 0, -3], [-1.5, 0, 2])
	dibujar_rectangulo([1.5, 0.5, 2], [1.5, 0, 2], [1.5, 0, -3], [1.5, 0.5, -3])
	
	# Capó y parabrisas
	dibujar_rectangulo([-1.5, 0.5, 2], [1.5, 0.5, 2], [1.2, 1.2, 0.5], [-1.2, 1.2, 0.5])
	dibujar_rectangulo([-1.2, 1.2, 0.5], [1.2, 1.2, 0.5], [1.0, 1.0, -1.5], [-1.0, 1.0, -1.5])
	
	# Vidrio (material transparente)
	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	aplicar_material([0.4, 0.6, 0.8, 0.3], [0.8, 0.8, 0.8], 90)
	dibujar_rectangulo([-1.0, 1.0, -1.5], [1.0, 1.0, -1.5], [0.8, 0.8, -2.5], [-0.8, 0.8, -2.5])
	glDisable(GL_BLEND)
	
	# Parachoques cromado
	aplicar_material([0.8, 0.8, 0.8], [0.9, 0.9, 0.9], 120)
	dibujar_rectangulo([-1.6, 0.2, 2.1], [1.6, 0.2, 2.1], [1.6, -0.1, 2.1], [-1.6, -0.1, 2.1])
	dibujar_rectangulo([-1.6, 0.2, -3.1], [1.6, 0.2, -3.1], [1.6, -0.1, -3.1], [-1.6, -0.1, -3.1])
	
	# Faros (material vidrio con emisión)
	aplicar_material([0.9, 0.9, 0.8], [1, 1, 1], 100, [0.8, 0.8, 0.5, 1])
	glPushMatrix()
	glTranslatef(1.4, 0.3, 1.8)
	gluSphere(gluNewQuadric(), 0.15, 16, 16)
	glTranslatef(-2.8, 0, 0)
	gluSphere(gluNewQuadric(), 0.15, 16, 16)
	glPopMatrix()
	
	# Ruedas
	dibujar_rueda(1.0, 0.0, 1.5)
	dibujar_rueda(-1.0, 0.0, 1.5)
	dibujar_rueda(1.0, 0.0, -2.5)
	dibujar_rueda(-1.0, 0.0, -2.5)

def dibujar_piso():
	aplicar_material([0.3, 0.3, 0.3], [0.1, 0.1, 0.1], 10)
	glBegin(GL_QUADS)
	glNormal3f(0, 1, 0)
	for x in range(-10, 10, 1):
		for z in range(-10, 10, 1):
			glVertex3f(x, -0.01, z)
			glVertex3f(x+1, -0.01, z)
			glVertex3f(x+1, -0.01, z+1)
			glVertex3f(x, -0.01, z+1)
	glEnd()

def main():
	pygame.init()
	display = (1200, 900)
	pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
	pygame.display.set_caption("Automóvil 3D con Iluminación Phong")
	
	gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
	glTranslatef(0, -1, -10)
	
	iniciar_luz_phong()
	
	rot_x, rot_y = 0, 0
	rot_auto = 0
	mouse_down = False
	last_pos = None
	
	clock = pygame.time.Clock()
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:  # Botón izquierdo
					mouse_down = True
					last_pos = event.pos
			elif event.type == pygame.MOUSEBUTTONUP:
				if event.button == 1:
					mouse_down = False
			elif event.type == pygame.MOUSEMOTION and mouse_down:
				dx, dy = event.pos[0] - last_pos[0], event.pos[1] - last_pos[1]
				rot_y += dx * 0.5
				rot_x -= dy * 0.5
				last_pos = event.pos
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					running = False
		
		rot_auto += 0.5
		
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		
		glPushMatrix()
		glRotatef(rot_x, 1, 0, 0)
		glRotatef(rot_y, 0, 1, 0)
		
		# Actualizar posición de la luz (foco sigue al auto)
		light_pos = [3*math.sin(rot_auto*0.02), 3, 3*math.cos(rot_auto*0.02), 1]
		glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
		
		dibujar_piso()
		
		glPushMatrix()
		glRotatef(rot_auto, 0, 1, 0)
		glTranslatef(0, 0, 5*math.sin(rot_auto*0.01))
		dibujar_auto()
		glPopMatrix()
		
		glPopMatrix()
		
		pygame.display.flip()
		clock.tick(60)
	
	pygame.quit()

if __name__ == "__main__":
	main()