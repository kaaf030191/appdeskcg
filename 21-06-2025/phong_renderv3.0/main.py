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
	
	# Luz principal (sol)
	glLightfv(GL_LIGHT0, GL_POSITION, [5.0, 10.0, 5.0, 1.0])
	glLightfv(GL_LIGHT0, GL_AMBIENT, [0.1, 0.1, 0.1, 1.0])
	glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 0.9, 1.0])
	glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
	glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 1.0)
	glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
	glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.001)
	
	# Luz de relleno (ambiente)
	glLightfv(GL_LIGHT1, GL_POSITION, [-5.0, 5.0, -5.0, 1.0])
	glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.5, 0.5, 0.6, 1.0])
	glLightfv(GL_LIGHT1, GL_SPECULAR, [0.3, 0.3, 0.4, 1.0])
	
	glEnable(GL_COLOR_MATERIAL)
	glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
	glEnable(GL_NORMALIZE)
	glShadeModel(GL_SMOOTH)

def aplicar_material(color, especular, brillo, emision=[0,0,0,1]):
	glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [c*0.3 for c in color] + [1])
	glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, color + [1])
	glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, especular + [1])
	glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, emision)
	glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, brillo)

def dibujar_superficie(puntos, normales=None):
	if normales is None:
		v1 = np.array(puntos[1]) - np.array(puntos[0])
		v2 = np.array(puntos[2]) - np.array(puntos[0])
		normal = np.cross(v1, v2)
		normal = normal / np.linalg.norm(normal)
		normales = [normal] * len(puntos)
	
	glBegin(GL_POLYGON)
	for punto, normal in zip(puntos, normales):
		glNormal3fv(normal)
		glVertex3fv(punto)
	glEnd()

def dibujar_parabrisas():
	puntos = [
		[-1.2, 0.8, 0.8], [1.2, 0.8, 0.8],
		[1.0, 1.2, -0.5], [-1.0, 1.2, -0.5]
	]
	aplicar_material([0.3, 0.4, 0.6, 0.6], [0.8, 0.8, 0.9], 90)
	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	dibujar_superficie(puntos)
	glDisable(GL_BLEND)

def dibujar_rueda(pos_x, pos_y, pos_z):
	glPushMatrix()
	glTranslatef(pos_x, pos_y, pos_z)
	
	# Neumático
	aplicar_material([0.05, 0.05, 0.05], [0.1, 0.1, 0.1], 10)
	gluDisk(gluNewQuadric(), 0.25, 0.35, 32, 1)
	gluCylinder(gluNewQuadric(), 0.35, 0.35, 0.2, 32, 1)
	glTranslatef(0, 0, 0.2)
	gluDisk(gluNewQuadric(), 0.25, 0.35, 32, 1)
	
	# Llanta
	aplicar_material([0.3, 0.3, 0.3], [0.7, 0.7, 0.7], 80)
	gluDisk(gluNewQuadric(), 0.15, 0.25, 32, 1)
	gluCylinder(gluNewQuadric(), 0.25, 0.25, 0.2, 32, 1)
	glTranslatef(0, 0, 0.2)
	gluDisk(gluNewQuadric(), 0.15, 0.25, 32, 1)
	
	# Tapacubos cromado
	aplicar_material([0.8, 0.8, 0.8], [0.9, 0.9, 0.9], 120)
	gluDisk(gluNewQuadric(), 0, 0.15, 32, 1)
	glPopMatrix()

def dibujar_carroceria():
	# Material metálico rojo
	aplicar_material([0.7, 0.1, 0.1], [0.8, 0.6, 0.6], 90)
	
	# Parte inferior
	puntos_base = [
		[-1.5, 0, 2.5], [1.5, 0, 2.5],
		[1.5, 0, -2.5], [-1.5, 0, -2.5]
	]
	dibujar_superficie(puntos_base)
	
	# Laterales
	puntos_lateral_izq = [
		[-1.5, 0, 2.5], [-1.5, 0.5, 2.0],
		[-1.5, 0.5, -2.0], [-1.5, 0, -2.5]
	]
	dibujar_superficie(puntos_lateral_izq)
	
	puntos_lateral_der = [
		[1.5, 0, 2.5], [1.5, 0.5, 2.0],
		[1.5, 0.5, -2.0], [1.5, 0, -2.5]
	]
	dibujar_superficie(puntos_lateral_der)
	
	# Delantera
	puntos_delante = [
		[-1.5, 0.5, 2.0], [1.5, 0.5, 2.0],
		[1.2, 0.8, 1.5], [-1.2, 0.8, 1.5]
	]
	dibujar_superficie(puntos_delante)
	
	# Capó
	puntos_capo = [
		[-1.2, 0.8, 1.5], [1.2, 0.8, 1.5],
		[0.8, 1.0, -0.5], [-0.8, 1.0, -0.5]
	]
	dibujar_superficie(puntos_capo)
	
	# Techo
	puntos_techo = [
		[-0.8, 1.0, -0.5], [0.8, 1.0, -0.5],
		[0.6, 0.9, -1.5], [-0.6, 0.9, -1.5]
	]
	dibujar_superficie(puntos_techo)
	
	# Trasera
	puntos_trasera = [
		[-1.5, 0.5, -2.0], [1.5, 0.5, -2.0],
		[1.2, 0.3, -2.3], [-1.2, 0.3, -2.3]
	]
	dibujar_superficie(puntos_trasera)

def dibujar_faros():
	glPushMatrix()
	aplicar_material([0.9, 0.9, 0.7], [1.0, 1.0, 1.0], 120, [0.5, 0.5, 0.3, 1.0])
	glTranslatef(1.3, 0.4, 2.2)
	gluSphere(gluNewQuadric(), 0.15, 32, 32)
	glTranslatef(-2.6, 0, 0)
	gluSphere(gluNewQuadric(), 0.15, 32, 32)
	glPopMatrix()

def dibujar_auto_completo():
	dibujar_carroceria()
	dibujar_parabrisas()
	dibujar_faros()
	
	# Ruedas
	dibujar_rueda(1.3, 0, 1.8)
	dibujar_rueda(-1.3, 0, 1.8)
	dibujar_rueda(1.3, 0, -1.8)
	dibujar_rueda(-1.3, 0, -1.8)
	
	# Detalles cromados
	aplicar_material([0.8, 0.8, 0.8], [0.95, 0.95, 0.95], 128.0)
	# Parachoques delantero
	glBegin(GL_QUAD_STRIP)
	for z in np.linspace(2.5, 2.2, 5):
		glVertex3f(-1.6, 0.1, z)
		glVertex3f(1.6, 0.1, z)
	glEnd()

def dibujar_escena():
	# Piso con rejilla
	aplicar_material([0.2, 0.2, 0.2], [0.1, 0.1, 0.1], 10)
	glBegin(GL_LINES)
	for i in range(-10, 11):
		glVertex3f(i, 0, -10)
		glVertex3f(i, 0, 10)
		glVertex3f(-10, 0, i)
		glVertex3f(10, 0, i)
	glEnd()
	
	# Fondo
	aplicar_material([0.4, 0.5, 0.7], [0.2, 0.2, 0.3], 30)
	glBegin(GL_QUADS)
	glVertex3f(-20, 0, -20)
	glVertex3f(20, 0, -20)
	glVertex3f(20, 20, -20)
	glVertex3f(-20, 20, -20)
	glEnd()

def main():
	pygame.init()
	display = (1280, 720)
	pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
	pygame.display.set_caption("Automóvil 3D de Alta Calidad con Phong")
	
	gluPerspective(45, (display[0]/display[1]), 0.1, 100.0)
	glTranslatef(0, -1.5, -8)
	
	glEnable(GL_DEPTH_TEST)
	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	
	iniciar_luz_phong()
	
	rot_x, rot_y = 20, 30
	mouse_down = False
	last_pos = None
	
	clock = pygame.time.Clock()
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
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
		
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		
		glPushMatrix()
		glRotatef(rot_x, 1, 0, 0)
		glRotatef(rot_y, 0, 1, 0)
		
		# Actualizar luz dinámica
		tiempo = pygame.time.get_ticks() / 1000.0
		luz_pos = [5*math.sin(tiempo), 8, 5*math.cos(tiempo), 1.0]
		glLightfv(GL_LIGHT0, GL_POSITION, luz_pos)
		
		dibujar_escena()
		dibujar_auto_completo()
		
		glPopMatrix()
		
		pygame.display.flip()
		clock.tick(60)
	
	pygame.quit()

if __name__ == "__main__":
	main()