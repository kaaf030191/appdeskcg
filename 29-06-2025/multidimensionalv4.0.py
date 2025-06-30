import sys
import numpy as np
import pandas as pd
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

window_width = 1000
window_height = 600
data, normalized_data = None, None
dimension_names = []
selected_points = set()

selecting = False
selected_axis = None
start_y = None
end_y = None

# === Cargar datos ===
def load_data():
	global data, normalized_data, dimension_names
	data = pd.DataFrame({
		'A': np.random.rand(100),
		'B': np.random.rand(100),
		'C': np.random.rand(100),
		'D': np.random.rand(100),
		'E': np.random.rand(100)
	})
	dimension_names = list(data.columns)
	normalized_data = (data - data.min()) / (data.max() - data.min())

# === Dibujar texto ===
def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_12):
	glRasterPos2f(x, y)
	for ch in text:
		glutBitmapCharacter(font, ord(ch))

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
		draw_text(x - 0.015, 1.02, dimension_names[i])

# === Dibujar líneas de datos ===
def draw_data():
	n = len(dimension_names)
	for i, row in normalized_data.iterrows():
		if i in selected_points:
			glColor3f(0.1, 1.0, 0.1)  # Verde brillante
			glLineWidth(2.0)
		else:
			glColor3f(0.5, 0.5, 1)
			glLineWidth(1.0)

		glBegin(GL_LINE_STRIP)
		for j, val in enumerate(row):
			x = j / (n - 1)
			glVertex2f(x, val)
		glEnd()

		# Dibujar puntos resaltados
		if i in selected_points:
			glPointSize(4)
			glBegin(GL_POINTS)
			for j, val in enumerate(row):
				x = j / (n - 1)
				glVertex2f(x, val)
			glEnd()

# === Dibujar barra de selección ===
def draw_selection_box():
	if not selecting or selected_axis is None or start_y is None or end_y is None:
		return
	x = selected_axis / (len(dimension_names) - 1)
	glColor4f(1, 0, 0, 0.3)
	glBegin(GL_QUADS)
	glVertex2f(x - 0.015, min(start_y, end_y))
	glVertex2f(x + 0.015, min(start_y, end_y))
	glVertex2f(x + 0.015, max(start_y, end_y))
	glVertex2f(x - 0.015, max(start_y, end_y))
	glEnd()

	# Etiqueta de rango seleccionado
	glColor3f(1, 1, 0)
	y_mid = (start_y + end_y) / 2
	draw_text(x + 0.02, y_mid, f"{min(start_y, end_y):.2f} - {max(start_y, end_y):.2f}")

# === Mostrar resumen de selección ===
def draw_selection_info():
	if len(selected_points) > 0:
		glColor3f(1, 1, 0)
		draw_text(0.01, 0.97, f"Seleccionados: {len(selected_points)}")

# === Selección de puntos ===
def select_points(axis_index, y_min, y_max):
	global selected_points
	selected_points.clear()
	if y_min > y_max:
		y_min, y_max = y_max, y_min
	for i, row in normalized_data.iterrows():
		if y_min <= row.iloc[axis_index] <= y_max:
			selected_points.add(i)

# === Mouse click ===
def mouse(button, state, x, y):
	global selecting, start_y, end_y, selected_axis
	norm_x = x / window_width
	norm_y = 1 - y / window_height
	if button == GLUT_LEFT_BUTTON:
		if state == GLUT_DOWN:
			selecting = True
			start_y = norm_y
			end_y = norm_y
			selected_axis = get_nearest_axis(norm_x)
		elif state == GLUT_UP:
			selecting = False
			end_y = norm_y
			if selected_axis is not None:
				select_points(selected_axis, start_y, end_y)
			glutPostRedisplay()

# === Mouse arrastre ===
def motion(x, y):
	global end_y
	if selecting:
		end_y = 1 - y / window_height
		glutPostRedisplay()

# === Encontrar eje más cercano ===
def get_nearest_axis(x_click):
	n = len(dimension_names)
	distances = [abs(x_click - (i / (n - 1))) for i in range(n)]
	return np.argmin(distances)

# === Render principal ===
def display():
	glClear(GL_COLOR_BUFFER_BIT)
	draw_axes()
	draw_data()
	draw_selection_box()
	draw_selection_info()
	glutSwapBuffers()

def reshape(width, height):
	global window_width, window_height
	window_width, window_height = width, height
	glViewport(0, 0, width, height)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluOrtho2D(0, 1, 0, 1)
	glMatrixMode(GL_MODELVIEW)

def main():
	load_data()
	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
	glutInitWindowSize(window_width, window_height)
	glutCreateWindow(b"Parallel Coordinates - Seleccion Visual Mejorada")
	glClearColor(0.1, 0.1, 0.1, 1)
	glutDisplayFunc(display)
	glutReshapeFunc(reshape)
	glutMouseFunc(mouse)
	glutMotionFunc(motion)
	glutMainLoop()

if __name__ == "__main__":
	main()