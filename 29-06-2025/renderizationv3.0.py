# Requiere PyOpenGL y GLUT instalados
# pip install PyOpenGL PyOpenGL_accelerate

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import math
import time

# Globals
width, height = 900, 600
angle = 0.0
frame_count = 0
last_time = 0
fps = 0
shader_times = [0.0, 0.0, 0.0]

# Luz y camara
light_pos = [5.0, 5.0, 5.0]
view_pos = [0.0, 0.0, 10.0]

# Modelos
models = ["Lambertiano", "Phong", "Cook-Torrance"]


def draw_sphere():
	quadric = gluNewQuadric()
	gluSphere(quadric, 1.0, 50, 50)
	gluDeleteQuadric(quadric)


def set_lighting():
	glEnable(GL_LIGHTING)
	glEnable(GL_LIGHT0)

	light_position = [light_pos[0], light_pos[1], light_pos[2], 1.0]
	light_color = [1.0, 1.0, 1.0, 1.0]
	glLightfv(GL_LIGHT0, GL_POSITION, light_position)
	glLightfv(GL_LIGHT0, GL_DIFFUSE, light_color)
	glLightfv(GL_LIGHT0, GL_SPECULAR, light_color)


def lambert_shader():
	normal = np.array([0.0, 0.0, 1.0])
	light_dir = np.array(light_pos) - np.array([0.0, 0.0, 0.0])
	light_dir /= np.linalg.norm(light_dir)
	diff = max(np.dot(normal, light_dir), 0.0)
	color = diff * np.array([1.0, 0.0, 0.0])  # Rojo puro
	glColor3fv(color)


def phong_shader():
	normal = np.array([0.0, 0.0, 1.0])
	light_dir = np.array(light_pos) - np.array([0.0, 0.0, 0.0])
	view_dir = np.array(view_pos) - np.array([0.0, 0.0, 0.0])
	light_dir /= np.linalg.norm(light_dir)
	view_dir /= np.linalg.norm(view_dir)
	reflect_dir = 2 * np.dot(normal, light_dir) * normal - light_dir

	diff = max(np.dot(normal, light_dir), 0.0)
	spec = pow(max(np.dot(view_dir, reflect_dir), 0.0), 16.0)
	color = diff * np.array([0.0, 1.0, 0.0]) + spec * np.array([1.0, 1.0, 1.0])  # Verde + blanco
	glColor3fv(np.clip(color, 0, 1))


def cook_torrance_shader():
	N = np.array([0.0, 0.0, 1.0])
	V = np.array(view_pos) - np.array([0.0, 0.0, 0.0])
	L = np.array(light_pos) - np.array([0.0, 0.0, 0.0])
	V /= np.linalg.norm(V)
	L /= np.linalg.norm(L)
	H = (V + L) / np.linalg.norm(V + L)

	roughness = 0.4
	metallic = 0.7
	F0 = 0.04
	F0 = F0 * (1 - metallic) + metallic

	F = F0 + (1 - F0) * pow(1 - max(np.dot(H, V), 0.0), 5.0)
	k = (roughness + 1) ** 2 / 8
	G1 = np.dot(N, V) / (np.dot(N, V) * (1 - k) + k)
	G2 = np.dot(N, L) / (np.dot(N, L) * (1 - k) + k)
	G = G1 * G2

	alpha = roughness ** 2
	NdotH = max(np.dot(N, H), 0.0)
	denom = (NdotH ** 2) * (alpha ** 2 - 1) + 1
	D = (alpha ** 2) / (math.pi * denom ** 2)

	NdotL = max(np.dot(N, L), 0.0)
	NdotV = max(np.dot(N, V), 0.0)

	specular = (F * G * D) / (4 * NdotV * NdotL + 0.001)
	kd = (1 - F) * (1 - metallic)
	diffuse = kd * np.array([0.0, 0.0, 1.0]) / math.pi  # Azul puro

	color = (diffuse + specular) * NdotL
	glColor3fv(np.clip(color, 0, 1))


def draw_text(x, y, text):
	glColor3f(1.0, 1.0, 1.0)  # Texto blanco
	glWindowPos2f(x, y)
	for c in text.encode():
		glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, c)


def display():
	global angle, frame_count, last_time, fps, shader_times
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()
	gluLookAt(*view_pos, 0, 0, 0, 0, 1, 0)
	set_lighting()

	positions = [-3.0, 0.0, 3.0]
	shaders = [lambert_shader, phong_shader, cook_torrance_shader]

	for i in range(3):
		start = time.perf_counter()
		glPushMatrix()
		glTranslatef(positions[i], 0.0, 0.0)
		glRotatef(angle, 0, 1, 0)
		shaders[i]()
		draw_sphere()
		glPopMatrix()
		shader_times[i] = time.perf_counter() - start

	glDisable(GL_LIGHTING)
	draw_text(10, height - 20, f"FPS: {fps:.2f}")
	for i, model in enumerate(models):
		draw_text(10, height - 40 - i * 20, f"{model}: {shader_times[i]*1000:.2f} ms/frame")
	glEnable(GL_LIGHTING)

	glutSwapBuffers()

	frame_count += 1
	current_time = time.time()
	if current_time - last_time >= 1.0:
		fps = frame_count / (current_time - last_time)
		frame_count = 0
		last_time = current_time


def reshape(w, h):
	global width, height
	width, height = w, h
	glViewport(0, 0, w, h)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(45, w / h, 1, 100)
	glMatrixMode(GL_MODELVIEW)


def idle():
	global angle
	angle += 0.5
	if angle > 360:
		angle -= 360
	glutPostRedisplay()


def main():
	global last_time
	glutInit()
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
	glutInitWindowSize(width, height)
	glutCreateWindow(b"Comparacion de Modelos de Iluminacion")

	glEnable(GL_DEPTH_TEST)
	glClearColor(0.1, 0.1, 0.1, 1.0)

	last_time = time.time()

	glutDisplayFunc(display)
	glutReshapeFunc(reshape)
	glutIdleFunc(idle)

	glutMainLoop()


if __name__ == '__main__':
	main()