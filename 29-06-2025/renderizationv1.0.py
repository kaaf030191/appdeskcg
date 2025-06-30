# Requiere PyOpenGL y GLUT instalados
# pip install PyOpenGL PyOpenGL_accelerate

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import math

# Globals
width, height = 800, 600
angle = 0.0
shader_mode = 0  # 0: Lambert, 1: Phong, 2: Cook-Torrance

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
	color = diff * np.array([1.0, 0.5, 0.3])
	glColor3fv(color)


def phong_shader():
	normal = np.array([0.0, 0.0, 1.0])
	light_dir = np.array(light_pos) - np.array([0.0, 0.0, 0.0])
	view_dir = np.array(view_pos) - np.array([0.0, 0.0, 0.0])
	light_dir /= np.linalg.norm(light_dir)
	view_dir /= np.linalg.norm(view_dir)
	reflect_dir = 2 * np.dot(normal, light_dir) * normal - light_dir

	diff = max(np.dot(normal, light_dir), 0.0)
	spec = pow(max(np.dot(view_dir, reflect_dir), 0.0), 32.0)
	color = diff * np.array([1.0, 0.5, 0.3]) + spec * np.array([1.0, 1.0, 1.0])
	glColor3fv(np.clip(color, 0, 1))


def cook_torrance_shader():
	N = np.array([0.0, 0.0, 1.0])
	V = np.array(view_pos) - np.array([0.0, 0.0, 0.0])
	L = np.array(light_pos) - np.array([0.0, 0.0, 0.0])
	V /= np.linalg.norm(V)
	L /= np.linalg.norm(L)
	H = (V + L) / np.linalg.norm(V + L)

	roughness = 0.5
	metallic = 0.2
	F0 = 0.04
	F0 = F0 * (1 - metallic) + metallic

	# Fresnel
	F = F0 + (1 - F0) * pow(1 - max(np.dot(H, V), 0.0), 5.0)

	# Geometría
	k = (roughness + 1) ** 2 / 8
	G1 = np.dot(N, V) / (np.dot(N, V) * (1 - k) + k)
	G2 = np.dot(N, L) / (np.dot(N, L) * (1 - k) + k)
	G = G1 * G2

	# Distribución GGX
	alpha = roughness ** 2
	NdotH = max(np.dot(N, H), 0.0)
	denom = (NdotH ** 2) * (alpha ** 2 - 1) + 1
	D = (alpha ** 2) / (math.pi * denom ** 2)

	NdotL = max(np.dot(N, L), 0.0)
	NdotV = max(np.dot(N, V), 0.0)

	specular = (F * G * D) / (4 * NdotV * NdotL + 0.001)
	kd = (1 - F) * (1 - metallic)
	diffuse = kd * np.array([1.0, 0.5, 0.3]) / math.pi

	color = (diffuse + specular) * NdotL
	glColor3fv(np.clip(color, 0, 1))


def display():
	global angle
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()
	gluLookAt(*view_pos, 0, 0, 0, 0, 1, 0)

	glRotatef(angle, 0, 1, 0)

	set_lighting()

	if shader_mode == 0:
		lambert_shader()
	elif shader_mode == 1:
		phong_shader()
	else:
		cook_torrance_shader()

	draw_sphere()

	glRasterPos3f(-2.0, -1.5, 0)
	for c in models[shader_mode].encode():
		glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, c)

	glutSwapBuffers()


def reshape(w, h):
	global width, height
	width, height = w, h
	glViewport(0, 0, w, h)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(45, w / h, 1, 100)
	glMatrixMode(GL_MODELVIEW)


def keyboard(key, x, y):
	global shader_mode
	if key == b'1':
		shader_mode = 0
	elif key == b'2':
		shader_mode = 1
	elif key == b'3':
		shader_mode = 2
	glutPostRedisplay()


def idle():
	global angle
	angle += 0.5
	if angle > 360:
		angle -= 360
	glutPostRedisplay()


def main():
	glutInit()
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
	glutInitWindowSize(width, height)
	glutCreateWindow(b"Comparacion de Modelos de Iluminacion")

	glEnable(GL_DEPTH_TEST)
	glClearColor(0.1, 0.1, 0.1, 1.0)

	glutDisplayFunc(display)
	glutReshapeFunc(reshape)
	glutKeyboardFunc(keyboard)
	glutIdleFunc(idle)

	glutMainLoop()


if __name__ == '__main__':
	main()