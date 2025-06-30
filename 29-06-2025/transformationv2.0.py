import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class Transformacion:
	def __init__(self, puntos):
		self.puntos = np.array(puntos, dtype=np.float32)
		self.puntos_h = np.hstack((self.puntos, np.ones((len(puntos), 1))))
	
	def traslacion(self, dx, dy, dz):
		T = np.array([
			[1, 0, 0, dx],
			[0, 1, 0, dy],
			[0, 0, 1, dz],
			[0, 0, 0, 1]
		], dtype=np.float32)
		self.puntos_h = self.puntos_h @ T.T
	
	def rotacion(self, theta, eje):
		theta_rad = np.radians(theta)
		eje_norm = eje / np.linalg.norm(eje)
		x, y, z = eje_norm
		c, s = np.cos(theta_rad), np.sin(theta_rad)
		C = 1 - c
		R = np.array([
			[x*x*C + c,   x*y*C - z*s, x*z*C + y*s, 0],
			[y*x*C + z*s, y*y*C + c,   y*z*C - x*s, 0],
			[z*x*C - y*s, z*y*C + x*s, z*z*C + c,   0],
			[0, 0, 0, 1]
		], dtype=np.float32)
		self.puntos_h = self.puntos_h @ R.T
	
	def escalamiento(self, sx, sy, sz):
		S = np.array([
			[sx, 0,  0,  0],
			[0,  sy, 0,  0],
			[0,  0,  sz, 0],
			[0,  0,  0,  1]
		], dtype=np.float32)
		self.puntos_h = self.puntos_h @ S.T
	
	def obtener_puntos(self):
		return (self.puntos_h[:, :3] / self.puntos_h[:, 3][:, np.newaxis]).astype(np.float32)

def dibujar_cubo(puntos):
	glBegin(GL_QUADS)
	# Caras del cubo
	caras = [
		[0, 1, 2, 3], [4, 5, 6, 7],  # Base y tapa
		[0, 1, 5, 4], [3, 2, 6, 7],  # Frontales
		[1, 2, 6, 5], [0, 3, 7, 4]   # Laterales
	]
	glColor3f(0.2, 0.8, 0.6)  # Color del cubo
	for cara in caras:
		for vertice in cara:
			glVertex3fv(puntos[vertice])
	glEnd()
	
	# Dibujar vértices con etiquetas
	glPointSize(8.0)
	glColor3f(1, 0, 0)  # Rojo para vértices
	glBegin(GL_POINTS)
	for p in puntos:
		glVertex3fv(p)
	glEnd()

def dibujar_coordenadas(puntos):
	glColor3f(1, 1, 1)  # Blanco para texto
	for i, p in enumerate(puntos):
		# Posicionar texto cerca del vértice
		glRasterPos3f(p[0] + 0.05, p[1] + 0.05, p[2] + 0.05)
		texto = f"V{i}: ({p[0]:.2f}, {p[1]:.2f}, {p[2]:.2f})"
		for char in texto:
			glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(char))

def dibujar_ejes():
	# Ejes con etiquetas
	ejes = [
		((0, 0, 0), (4, 0, 0), (1, 0, 0), "X"),  # Eje X (rojo)
		((0, 0, 0), (0, 4, 0), (0, 1, 0), "Y"),  # Eje Y (verde)
		((0, 0, 0), (0, 0, 4), (0, 0, 1), "Z")   # Eje Z (azul)
	]
	
	glLineWidth(2.0)
	for inicio, fin, color, etiqueta in ejes:
		glColor3fv(color)
		glBegin(GL_LINES)
		glVertex3fv(inicio)
		glVertex3fv(fin)
		glEnd()
		
		# Etiqueta del eje
		glRasterPos3f(fin[0] + 0.1, fin[1] + 0.1, fin[2] + 0.1)
		for char in etiqueta:
			glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(char))

def init_gl():
	glClearColor(0.1, 0.1, 0.1, 1.0)
	glEnable(GL_DEPTH_TEST)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(45, (800/600), 0.1, 50.0)
	glMatrixMode(GL_MODELVIEW)

def mostrar():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()
	gluLookAt(8, 6, 10, 0, 0, 0, 0, 1, 0)  # Vista panorámica
	
	dibujar_ejes()  # Dibujar ejes con etiquetas
	
	puntos_transformados = transformacion.obtener_puntos()
	dibujar_cubo(puntos_transformados)  # Dibujar cubo
	dibujar_coordenadas(puntos_transformados)  # Mostrar coordenadas
	
	glutSwapBuffers()

def main():
	global transformacion
	# Vértices del cubo unitario
	cubo = [
		[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],
		[0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]
	]
	
	# Aplicar transformaciones
	transformacion = Transformacion(cubo)
	transformacion.rotacion(45, [0, 1, 0])  # Rotación 45° eje Y
	transformacion.traslacion(2, -1, 3)      # Traslación (2,-1,3)
	transformacion.escalamiento(0.5, 0.5, 0.5) # Escalamiento uniforme
	
	# Configurar ventana OpenGL
	glutInit()
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
	glutInitWindowSize(1000, 800)
	glutCreateWindow(b"Cubo 3D con Coordenadas y Ejes")
	glutDisplayFunc(mostrar)
	init_gl()
	glutMainLoop()

if __name__ == "__main__":
	main()