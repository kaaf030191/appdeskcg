import tkinter as tk
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

# === VARIABLES GLOBALES ===
current_model = "lambert"
angle_x, angle_y = 0.0, 0.0
pos_x, pos_y, pos_z = 0.0, 0.0, 0.0

# === INICIAR RENDERING OPENGL ===
def start_rendering():
	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
	glutInitWindowSize(800, 600)
	glutCreateWindow(b"Shading Models with PyOpenGL and Tkinter")

	glEnable(GL_DEPTH_TEST)
	glClearColor(0.1, 0.1, 0.1, 1.0)

	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(45, 800 / 600, 0.1, 100.0)

	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()

	init_lighting()

	glutDisplayFunc(display)
	glutIdleFunc(display)
	glutKeyboardFunc(keyboard)
	glutMainLoop()

# === ILUMINACIÓN ===
def init_lighting():
	glEnable(GL_LIGHTING)
	glEnable(GL_LIGHT0)
	glLightfv(GL_LIGHT0, GL_POSITION, [2.0, 2.0, 2.0, 1.0])
	glLightfv(GL_LIGHT0, GL_AMBIENT, [0.1, 0.1, 0.1, 1.0])
	glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
	glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])

# === MATERIALES ===
def set_material(model):
	if model == "lambert":
		glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.0, 0.6, 0.8, 1.0])
		glMaterialfv(GL_FRONT, GL_SPECULAR, [0.0, 0.0, 0.0, 1.0])
		glMaterialf(GL_FRONT, GL_SHININESS, 0.0)
	elif model == "phong":
		glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.6, 0.2, 0.7, 1.0])
		glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
		glMaterialf(GL_FRONT, GL_SHININESS, 50.0)
	elif model == "blinn":
		glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.2, 0.7, 0.3, 1.0])
		glMaterialfv(GL_FRONT, GL_SPECULAR, [0.8, 0.8, 0.8, 1.0])
		glMaterialf(GL_FRONT, GL_SHININESS, 100.0)
	elif model == "cook":
		glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.7, 0.5, 0.3, 1.0])
		glMaterialfv(GL_FRONT, GL_SPECULAR, [0.9, 0.9, 0.9, 1.0])
		glMaterialf(GL_FRONT, GL_SHININESS, 10.0)

# === DIBUJAR ESCENA ===
def display():
	global angle_x, angle_y, current_model, pos_x, pos_y, pos_z
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()
	gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)

	glTranslatef(pos_x, pos_y, pos_z)
	glRotatef(angle_x, 1, 0, 0)
	glRotatef(angle_y, 0, 1, 0)

	set_material(current_model)
	glutSolidTeapot(1.0)

	glutSwapBuffers()

# === TECLADO ===
def keyboard(key, x, y):
	global angle_x, angle_y, current_model, pos_x, pos_y, pos_z
	if key == b"w":
		angle_x += 5
	elif key == b"s":
		angle_x -= 5
	elif key == b"a":
		angle_y -= 5
	elif key == b"d":
		angle_y += 5
	elif key == b"1":
		current_model = "lambert"
	elif key == b"2":
		current_model = "phong"
	elif key == b"3":
		current_model = "blinn"
	elif key == b"4":
		current_model = "cook"
	elif key == b"i":
		pos_z -= 0.1
	elif key == b"k":
		pos_z += 0.1
	elif key == b"j":
		pos_x -= 0.1
	elif key == b"l":
		pos_x += 0.1
	elif key == b"u":
		pos_y += 0.1
	elif key == b"o":
		pos_y -= 0.1
	elif key == b"r":
		# Reset position and rotation
		angle_x = angle_y = 0.0
		pos_x = pos_y = pos_z = 0.0
	glutPostRedisplay()

# === INTERFAZ CON TKINTER ===
def main_gui():
	root = tk.Tk()
	root.title("Renderización con PyOpenGL")

	tk.Label(root, text="Modelos de Iluminación", font=("Arial", 14)).pack(pady=10)
	tk.Label(root, text="1: Lambert | 2: Phong | 3: Blinn-Phong | 4: Cook-Torrance", font=("Arial", 10)).pack()
	tk.Label(root, text="W/S: Rotar eje X | A/D: Rotar eje Y", font=("Arial", 10)).pack()
	tk.Label(root, text="I/K: Adelante/Atrás | J/L: Izq/Der | U/O: Arriba/Abajo", font=("Arial", 10)).pack()
	tk.Label(root, text="R: Reiniciar posición y rotación", font=("Arial", 10)).pack(pady=5)

	btn = tk.Button(root, text="Iniciar Visualización 3D", command=start_rendering, bg="lightblue", font=("Arial", 12))
	btn.pack(pady=20)

	root.mainloop()

if __name__ == "__main__":
	main_gui()