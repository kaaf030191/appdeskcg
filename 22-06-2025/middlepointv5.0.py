import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

def draw_axes():
	"""Dibuja los ejes X e Y"""
	glBegin(GL_LINES)
	# Eje X (rojo)
	glColor3f(1.0, 0.0, 0.0)
	glVertex2f(-20, 0)
	glVertex2f(20, 0)
	# Eje Y (verde)
	glColor3f(0.0, 1.0, 0.0)
	glVertex2f(0, -20)
	glVertex2f(0, 20)
	glEnd()

def draw_pixel(x, y):
	"""Dibuja un píxel en la posición (x, y)"""
	glBegin(GL_POINTS)
	glVertex2f(x, y)
	glEnd()

def draw_circle_midpoint(radius):
	"""Implementación del algoritmo de punto medio para dibujar una circunferencia centrada en (0,0)"""
	x = 0
	y = radius
	d = 1 - radius  # Parámetro de decisión inicial
	
	print("Posiciones en el primer octante (desde x=0 hasta x=y):")
	print(f"({x}, {y})")  # Primer punto
	
	while x < y:
		x += 1
		if d < 0:
			d += 2 * x + 1
		else:
			y -= 1
			d += 2 * (x - y) + 1
		
		# Dibujar los 8 puntos simétricos
		draw_pixel(x, y)
		draw_pixel(y, x)
		draw_pixel(-x, y)
		draw_pixel(-y, x)
		draw_pixel(x, -y)
		draw_pixel(y, -x)
		draw_pixel(-x, -y)
		draw_pixel(-y, -x)
		
		# Imprimir solo los puntos del primer octante (x <= y)
		if x <= y:
			print(f"({x}, {y})")

def main():
	pygame.init()
	display = (800, 600)
	pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
	gluOrtho2D(-20, 20, -20, 20)
	
	# Parámetros del círculo
	radius = 10
	
	print(f"Dibujando círculo con centro en (0, 0) y radio {radius}")
	print("Puntos en el primer octante (desde x=0 hasta x=y):")
	
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				return
		
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		
		# Dibujar ejes
		draw_axes()
		
		# Configurar color para el círculo (blanco)
		glColor3f(1.0, 1.0, 1.0)
		
		# Dibujar círculo centrado en (0,0)
		draw_circle_midpoint(radius)
		
		pygame.display.flip()
		pygame.time.wait(10)

if __name__ == "__main__":
	main()