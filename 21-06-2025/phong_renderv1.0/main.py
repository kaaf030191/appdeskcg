import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import numpy as np

def iniciar_luz_phong():
	glEnable(GL_LIGHTING)
	glEnable(GL_LIGHT0)
	glEnable(GL_LIGHT1)  # Segunda luz para más brillo
	
	# Luz principal (más intensa)
	luz_posicion = [3.0, 3.0, 3.0, 1.0]
	luz_ambiente = [0.4, 0.4, 0.4, 1.0]
	luz_difusa = [1.0, 1.0, 1.0, 1.0]
	luz_especular = [1.0, 1.0, 1.0, 1.0]
	
	glLightfv(GL_LIGHT0, GL_POSITION, luz_posicion)
	glLightfv(GL_LIGHT0, GL_AMBIENT, luz_ambiente)
	glLightfv(GL_LIGHT0, GL_DIFFUSE, luz_difusa)
	glLightfv(GL_LIGHT0, GL_SPECULAR, luz_especular)
	
	# Segunda luz (para resaltar especular)
	luz_posicion2 = [-3.0, 3.0, -3.0, 1.0]
	glLightfv(GL_LIGHT1, GL_POSITION, luz_posicion2)
	glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.5, 0.5, 0.5, 1.0])
	glLightfv(GL_LIGHT1, GL_SPECULAR, [0.8, 0.8, 0.8, 1.0])
	
	# Configuración de atenuación
	glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.5)
	glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
	glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.01)

def aplicar_material_oro_phong_brillante():
	# Material oro con parámetros más brillantes
	ambiente = [0.34725, 0.2995, 0.1745, 1.0]  # Aumentado
	difuso = [0.95164, 0.80648, 0.42648, 1.0]   # Más amarillo/dorado
	especular = [0.928281, 0.855802, 0.666065, 1.0]  # Más brillante
	emision = [0.1, 0.1, 0.0, 1.0]  # Leve emisión dorada
	brillo = 128.0  # Aumentado significativamente
	
	glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, ambiente)
	glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, difuso)
	glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, especular)
	glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, emision)
	glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, brillo)
	
	# Configuración avanzada para mejor Phong
	glShadeModel(GL_SMOOTH)
	glEnable(GL_NORMALIZE)
	glEnable(GL_COLOR_MATERIAL)
	glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

def calcular_normales(vertices, caras):
	normales = np.zeros((len(vertices), 3))
	normales_caras = []
	
	for cara in caras:
		v0, v1, v2 = vertices[cara[0]], vertices[cara[1]], vertices[cara[2]]
		u = np.array(v1) - np.array(v0)
		v = np.array(v2) - np.array(v0)
		normal = np.cross(u, v)
		normales_caras.append(normal)
		
	# Promedio de normales para cada vértice
	for i, vertice in enumerate(vertices):
		normales_adyacentes = []
		for j, cara in enumerate(caras):
			if i in cara[:3]:
				normales_adyacentes.append(normales_caras[j])
		
		if normales_adyacentes:
			normal_promedio = np.mean(normales_adyacentes, axis=0)
			normal_promedio /= np.linalg.norm(normal_promedio)
			normales[i] = normal_promedio
	
	return normales

def dibujar_cubo_phong_suave():
	vertices = np.array([
		[1, 1, -1], [1, -1, -1], [-1, -1, -1], [-1, 1, -1],
		[1, 1, 1], [1, -1, 1], [-1, -1, 1], [-1, 1, 1]
	], dtype=np.float32)
	
	caras = [
		(0, 1, 2, 3), (4, 5, 1, 0),
		(7, 6, 5, 4), (3, 2, 6, 7),
		(4, 0, 3, 7), (1, 5, 6, 2)
	]
	
	normales = calcular_normales(vertices, [c[:3] for c in caras])
	
	glBegin(GL_QUADS)
	for cara in caras:
		for v in cara:
			glNormal3fv(normales[v])
			glVertex3fv(vertices[v])
	glEnd()

def dibujar_ejes():
	glDisable(GL_LIGHTING)
	glLineWidth(3.0)
	glBegin(GL_LINES)
	
	# Eje X - rojo
	glColor3f(1, 0, 0)
	glVertex3f(-4, 0, 0)
	glVertex3f(4, 0, 0)
	
	# Eje Y - verde
	glColor3f(0, 1, 0)
	glVertex3f(0, -4, 0)
	glVertex3f(0, 4, 0)
	
	# Eje Z - azul
	glColor3f(0, 0, 1)
	glVertex3f(0, 0, -4)
	glVertex3f(0, 0, 4)
	
	glEnd()
	glEnable(GL_LIGHTING)

def main():
	pygame.init()
	display = (1000, 800)
	pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
	pygame.display.set_caption("Cubo Dorado Brillante con Phong Intenso")

	glClearColor(0.05, 0.05, 0.1, 1)  # Fondo azul oscuro para contraste
	glEnable(GL_DEPTH_TEST)
	
	gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
	glTranslatef(0, 0, -8)
	
	iniciar_luz_phong()
	aplicar_material_oro_phong_brillante()
	
	rot_x, rot_y = 25, 45
	vel_x, vel_y = 0.6, 0.8
	
	clock = pygame.time.Clock()
	ejecutando = True
	while ejecutando:
		for evento in pygame.event.get():
			if evento.type == QUIT:
				ejecutando = False
			elif evento.type == KEYDOWN:
				if evento.key == K_ESCAPE:
					ejecutando = False
				elif evento.key == K_UP:
					vel_x *= 1.1
					vel_y *= 1.1
				elif evento.key == K_DOWN:
					vel_x *= 0.9
					vel_y *= 0.9
		
		rot_x += vel_x
		rot_y += vel_y
		
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		
		# Luz dinámica que gira alrededor del cubo
		tiempo = pygame.time.get_ticks() / 1000.0
		luz_pos = [5*math.sin(tiempo), 3, 5*math.cos(tiempo), 1.0]
		glLightfv(GL_LIGHT0, GL_POSITION, luz_pos)
		
		dibujar_ejes()
		
		glPushMatrix()
		glRotatef(rot_x, 1, 0, 0)
		glRotatef(rot_y, 0, 1, 0)
		dibujar_cubo_phong_suave()
		glPopMatrix()
		
		pygame.display.flip()
		clock.tick(60)
	
	pygame.quit()

if __name__ == "__main__":
	main()