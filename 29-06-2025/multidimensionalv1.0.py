# visual_parallel_coords.py
import sys
import numpy as np
import pandas as pd
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# === Configuración inicial ===
window_width = 1000
window_height = 600
selected_range = [None, None]
data, normalized_data = None, None
dimension_names = []
selected_points = set()

# === Cargar datos ===
def load_data():
	global data, normalized_data, dimension_names
	# Usar datos artificiales de ejemplo (puedes reemplazar por un CSV)
	data = pd.DataFrame({
		'A': np.random.rand(100),
		'B': np.random.rand(100),
		'C': np.random.rand(100),
		'D': np.random.rand(100),
		'E': np.random.rand(100)
	})
	dimension_names = list(data.columns)
	# Normalizar entre 0 y 1
	normalized_data = (data - data.min()) / (data.max() - data.min())

# === Dibujar ejes ===
def draw_axes():
	n = len(dimension_names)
	for i in range(n):
		x = i / (n - 1)
		glColor3f(1, 1, 1)
		glBegin(GL_LINES)
		glVertex2f(x, 0)
		glVertex2f(x, 1)
		glEnd()
		draw_text(x, 1.02, dimension_names[i])

# === Dibujar texto ===
def draw_text(x, y, text):
	glRasterPos2f(x, y)
	for ch in text:
		glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(ch))

# === Dibujar líneas de datos ===
def draw_data():
	global selected_points
	n = len(dimension_names)
	for i, row in normalized_data.iterrows():
		if i in selected_points:
			glColor3f(1, 0, 0)  # Seleccionado
			glLineWidth(2)
		else:
			glColor3f(0.5, 0.5, 1)
			glLineWidth(1)
		glBegin(GL_LINE_STRIP)
		for j, value in enumerate(row):
			x = j / (n - 1)
			glVertex2f(x, value)
		glEnd()

# === Seleccionar datos con el mouse ===
def select_points(y_min, y_max):
	global selected_points
	selected_points.clear()
	if y_min > y_max:
		y_min, y_max = y_max, y_min
	for i, row in normalized_data.iterrows():
		if all(y_min <= val <= y_max for val in row):
			selected_points.add(i)

# === Dibujar selección actual ===
def draw_selection_box():
	if selected_range[0] is None or selected_range[1] is None:
		return
	glColor4f(1, 0, 0, 0.3)
	glBegin(GL_QUADS)
	glVertex2f(0, selected_range[0])
	glVertex2f(1, selected_range[0])
	glVertex2f(1, selected_range[1])
	glVertex2f(0, selected_range[1])
	glEnd()

# === Render principal ===
def display():
	glClear(GL_COLOR_BUFFER_BIT)
	draw_axes()
	draw_data()
	draw_selection_box()
	glutSwapBuffers()

# === Ajuste de tamaño de ventana ===
def reshape(width, height):
	glViewport(0, 0, width, height)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluOrtho2D(0, 1, 0, 1)
	glMatrixMode(GL_MODELVIEW)

# === Mouse interacciones ===
def mouse(button, state, x, y):
	if button == GLUT_LEFT_BUTTON:
		norm_y = 1 - y / window_height
		if state == GLUT_DOWN:
			selected_range[0] = norm_y
		elif state == GLUT_UP:
			selected_range[1] = norm_y
			select_points(*selected_range)
			glutPostRedisplay()

# === Programa principal ===
def main():
	load_data()
	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
	glutInitWindowSize(window_width, window_height)
	glutCreateWindow(b"Parallel Coordinates (PyOpenGL)")
	glClearColor(0.1, 0.1, 0.1, 1)
	glutDisplayFunc(display)
	glutReshapeFunc(reshape)
	glutMouseFunc(mouse)
	glutMainLoop()

if __name__ == "__main__":
	main()