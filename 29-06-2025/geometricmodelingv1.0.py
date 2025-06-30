import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# Puntos de control para la curva de Bézier cúbica en 3D
control_points = np.array([
	[0.0, 0.0, 0.0],
	[1.0, 3.0, 1.0],
	[3.0, 1.0, 2.0],
	[4.0, 4.0, 0.0]
])

def bezier_curve(t, points):
	"""
	Calcula un punto en la curva de Bézier cúbica.
	P(t) = (1-t)^3 * P0 + 3*(1-t)^2 * t * P1 + 3*(1-t) * t^2 * P2 + t^3 * P3
	"""
	p0, p1, p2, p3 = points
	return (1 - t)**3 * p0 + \
		3 * (1 - t)**2 * t * p1 + \
		3 * (1 - t) * t**2 * p2 + \
		t**3 * p3

def draw_objects(curve_points, control_points):
	"""Dibuja los puntos de control y la curva de Bézier."""
	glPointSize(10.0)
	glBegin(GL_POINTS)
	# Dibujar puntos de control en rojo
	glColor3f(1.0, 0.0, 0.0)
	for point in control_points:
		glVertex3fv(point)
	glEnd()

	# Dibujar las líneas de conexión de los puntos de control en gris
	glColor3f(0.5, 0.5, 0.5)
	glBegin(GL_LINE_STRIP)
	for point in control_points:
		glVertex3fv(point)
	glEnd()

	# Dibujar la curva de Bézier en azul
	glLineWidth(3.0)
	glColor3f(0.0, 0.0, 1.0)
	glBegin(GL_LINE_STRIP)
	for point in curve_points:
		glVertex3fv(point)
	glEnd()

def main():
	pygame.init()
	display = (800, 600)
	pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
	pygame.display.set_caption("Curva de Bézier cúbica en 3D")

	gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
	glTranslatef(0.0, 0.0, -10) # Mueve la cámara hacia atrás

	# Generar puntos para la curva de Bézier
	num_segments = 100
	curve_points = []
	for i in range(num_segments + 1):
		t = i / float(num_segments)
		point = bezier_curve(t, control_points)
		curve_points.append(point)
	curve_points = np.array(curve_points)

	rotation_x = 0
	rotation_y = 0
	mouse_down = False
	last_pos = None

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			elif event.type == MOUSEBUTTONDOWN:
				if event.button == 1:  # Left mouse button
					mouse_down = True
					last_pos = event.pos
			elif event.type == MOUSEBUTTONUP:
				if event.button == 1:
					mouse_down = False
			elif event.type == MOUSEMOTION:
				if mouse_down:
					dx, dy = event.pos[0] - last_pos[0], event.pos[1] - last_pos[1]
					rotation_y += dx * 0.5
					rotation_x += dy * 0.5
					last_pos = event.pos

		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		glPushMatrix()
		glRotatef(rotation_x, 1, 0, 0)
		glRotatef(rotation_y, 0, 1, 0)

		draw_objects(curve_points, control_points)
		glPopMatrix()
		pygame.display.flip()
		pygame.time.wait(10)

if __name__ == "__main__":
	main()