import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# --- Clase Transformacion (sin cambios) ---
class Transformacion:
	def __init__(self, puntos):
		self.puntos = np.array(puntos, dtype=np.float32)
		self.puntos_h = np.hstack(
			(
				self.puntos, np.ones((len(puntos), 1),
				dtype=np.float32)
			)
		)
	
	def traslacion(self, dx, dy, dz):
		T = np.array([
			[1, 0, 0, dx],
			[0, 1, 0, dy],
			[0, 0, 1, dz],
			[0, 0, 0, 1]
		], dtype=np.float32)
		self.puntos_h = np.dot(self.puntos_h, T.T)
	
	def rotacion(self, theta, eje):
		theta_rad = np.radians(theta)
		eje_norm = eje / np.linalg.norm(eje)
		x, y, z = eje_norm
		c, s = np.cos(theta_rad), np.sin(theta_rad)
		C = 1 - c
		R = np.array([
			[x*x*C + c,     x*y*C - z*s, x*z*C + y*s, 0],
			[y*x*C + z*s, y*y*C + c,     y*z*C - x*s, 0],
			[z*x*C - y*s, z*y*C + x*s, z*z*C + c,     0],
			[0, 0, 0, 1]
		], dtype=np.float32)
		self.puntos_h = np.dot(self.puntos_h, R.T)
	
	def escalamiento(self, sx, sy, sz):
		S = np.array([
			[sx, 0,  0,  0],
			[0,  sy, 0,  0],
			[0,  0,  sz, 0],
			[0,  0,  0,  1]
		], dtype=np.float32)
		self.puntos_h = np.dot(self.puntos_h, S.T)
	
	def obtener_puntos(self):
		w = self.puntos_h[:, 3][:, np.newaxis]
		return (self.puntos_h[:, :3] / w).astype(np.float32)

# --- Configuración de PyOpenGL ---

# Vértices de un cubo unitario
vertices_cubo_original = np.array([
	[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],  # Cara frontal (0,1,2,3)
	[0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]   # Cara trasera (4,5,6,7)
], dtype=np.float32)

# Definición de las aristas para dibujar el cubo
aristas_cubo = [
	(0, 1), (1, 2), (2, 3), (3, 0),  # Lados de la cara frontal
	(4, 5), (5, 6), (6, 7), (7, 4),  # Lados de la cara trasera
	(0, 4), (1, 5), (2, 6), (3, 7)   # Conexión entre caras
]

# Instancia para el cubo transformado
transformacion_cubo = Transformacion(vertices_cubo_original)
transformacion_cubo.rotacion(45, [0, 1, 0]) # Rotación alrededor del eje Y
transformacion_cubo.traslacion(2, -1, 3)    # Traslación
transformacion_cubo.escalamiento(0.5, 0.5, 0.5) # Escalamiento

# --- Funciones de Dibujo ---

def dibujar_cubo_con_aristas(vertices, color):
	glColor3fv(color)
	glLineWidth(1.5) # Grosor de las líneas del cubo
	glBegin(GL_LINES)
	for edge in aristas_cubo:
		for vertex_index in edge:
			glVertex3fv(vertices[vertex_index])
	glEnd()

def dibujar_vertices_con_etiquetas(puntos, color, offset=(0.05, 0.05, 0.05)):
	glColor3fv(color)
	glPointSize(8.0) # Tamaño de los puntos de los vértices
	glBegin(GL_POINTS)
	for p in puntos:
		glVertex3fv(p)
	glEnd()
	
	# Dibujar SOLO las etiquetas v1, v2, ... (NO las coordenadas numéricas aquí)
	if color == (1,0,0): # Cubo Original (Rojo)
		glColor3f(1, 1, 1) # Etiquetas blancas
	else: # Cubo Transformado (Cian)
		glColor3f(0.8, 0.8, 0.8) # Etiquetas gris claro

	for i, p in enumerate(puntos):
		etiqueta = f"v{i+1}"
		glRasterPos3f(p[0] + offset[0], p[1] + offset[1], p[2] + offset[2])
		for c_char in etiqueta:
			glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(c_char))

def dibujar_ejes():
	ejes = [
		((0, 0, 0), (4, 0, 0), (1, 0, 0), "X"), # Eje X: Rojo
		((0, 0, 0), (0, 4, 0), (0, 1, 0), "Y"), # Eje Y: Verde
		((0, 0, 0), (0, 0, 4), (0, 0, 1), "Z")  # Eje Z: Azul
	]
	glLineWidth(2.0)
	for inicio, fin, color, etiqueta in ejes:
		glColor3fv(color)
		glBegin(GL_LINES)
		glVertex3fv(inicio)
		glVertex3fv(fin)
		glEnd()
		glRasterPos3f(fin[0] + 0.1, fin[1] + 0.1, fin[2] + 0.1)
		for c_char in etiqueta:
			glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(c_char))

def dibujar_texto_2d(texto_lines, x, y, line_height, text_color=(1,1,1), font=GLUT_BITMAP_9_BY_15):
	# Entrar en modo 2D para dibujar el texto
	glMatrixMode(GL_PROJECTION)
	glPushMatrix()
	glLoadIdentity()
	gluOrtho2D(0, glutGet(GLUT_WINDOW_WIDTH), 0, glutGet(GLUT_WINDOW_HEIGHT))
	
	glMatrixMode(GL_MODELVIEW)
	glPushMatrix()
	glLoadIdentity()
	
	glDisable(GL_DEPTH_TEST) # Deshabilitar prueba de profundidad para que el texto siempre sea visible

	glColor3fv(text_color)
	current_y = y
	for line in texto_lines:
		glRasterPos2f(x, current_y)
		for char_code in line.encode('ascii'):
			glutBitmapCharacter(font, char_code)
		current_y -= line_height

	# Restaurar estado de OpenGL
	glEnable(GL_DEPTH_TEST)
	glMatrixMode(GL_PROJECTION)
	glPopMatrix()
	glMatrixMode(GL_MODELVIEW)
	glPopMatrix()

def mostrar():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()
	# Ajuste de la cámara para ver ambos cubos claramente y tener espacio para la leyenda
	gluLookAt(4, 5, 10,  # Posición de la cámara
			0.5, 0.5, 0.5, # Punto al que mira (cerca del centro del cubo original)
			0, 1, 0) # Vector "arriba"

	dibujar_ejes()
	
	# Dibujar el cubo original en rojo (con aristas)
	dibujar_cubo_con_aristas(vertices_cubo_original, (1, 0, 0)) # Rojo
	dibujar_vertices_con_etiquetas(vertices_cubo_original, (1, 0, 0)) # Etiquetas de vértices
	
	# Dibujar el cubo transformado en cian (con aristas)
	dibujar_cubo_con_aristas(transformacion_cubo.obtener_puntos(), (0, 1, 0.6)) # Cian
	dibujar_vertices_con_etiquetas(transformacion_cubo.obtener_puntos(), (0, 1, 0.6)) # Etiquetas de vértices
	
	# --- Leyenda Principal (Explicación de elementos visuales) ---
	margen_x_leyenda = 10
	margen_y_leyenda = glutGet(GLUT_WINDOW_HEIGHT) - 30
	salto_linea_leyenda = 20

	leyenda_principal_lines = [
		"LEYENDA VISUAL:",
		"Cubo Original (Rojo)",
		"Cubo Transformado (Cian)",
		"Eje X (Rojo)",
		"Eje Y (Verde)",
		"Eje Z (Azul)"
	]
	dibujar_texto_2d(leyenda_principal_lines, margen_x_leyenda, margen_y_leyenda, 
					salto_linea_leyenda, font=GLUT_BITMAP_HELVETICA_12)

	# --- Leyenda de Coordenadas de Vértices (SEPARADA) ---
	margen_x_coords = 250 # Posicionar más a la derecha
	margen_y_coords_original = glutGet(GLUT_WINDOW_HEIGHT) - 30 # Misma altura inicial
	salto_linea_coords = 18

	# Coordenadas del Cubo Original
	coords_original_lines = ["COORDENADAS CUBO ORIGINAL (ROJO):"]
	for i, p in enumerate(vertices_cubo_original):
		coords_original_lines.append(f"v{i+1}: ({p[0]:.2f}, {p[1]:.2f}, {p[2]:.2f})")
	
	dibujar_texto_2d(coords_original_lines, margen_x_coords, margen_y_coords_original, 
					salto_linea_coords, text_color=(1,1,1), font=GLUT_BITMAP_HELVETICA_10)

	# Coordenadas del Cubo Transformado
	puntos_t = transformacion_cubo.obtener_puntos()
	coords_transformado_lines = ["COORDENADAS CUBO TRANSFORMADO (CIAN):"]
	for i, p in enumerate(puntos_t):
		coords_transformado_lines.append(f"v{i+1}: ({p[0]:.2f}, {p[1]:.2f}, {p[2]:.2f})")
	
	# Calcular posición Y para la leyenda del cubo transformado
	y_transformado_coords_start = margen_y_coords_original - (len(vertices_cubo_original) + 2) * salto_linea_coords
	dibujar_texto_2d(coords_transformado_lines, margen_x_coords, y_transformado_coords_start, 
					salto_linea_coords, text_color=(0.0, 1.0, 0.6), font=GLUT_BITMAP_HELVETICA_10)

	glutSwapBuffers()

def init_gl():
	glClearColor(0.1, 0.1, 0.1, 1.0) # Fondo ligeramente gris oscuro
	glEnable(GL_DEPTH_TEST)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(45, (1000/800), 0.1, 100.0) 
	glMatrixMode(GL_MODELVIEW)

def main():
	glutInit()
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
	glutInitWindowSize(1000, 800) # Tamaño de ventana
	glutCreateWindow(b"Cubos 3D con Leyendas Separadas y Claras") 
	glutDisplayFunc(mostrar)
	init_gl()
	glutMainLoop()

if __name__ == "__main__":
	main()