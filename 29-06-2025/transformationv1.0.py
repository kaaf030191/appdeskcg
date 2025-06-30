import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import time

# --- Clase Transformacion (sin cambios) ---
class Transformacion:
	def __init__(self, puntos):
		self.puntos = np.array(puntos, dtype=np.float32)
		self.puntos_homogeneos = np.hstack((self.puntos, np.ones((self.puntos.shape[0], 1))))
		self.matriz_transformacion_acumulada = np.identity(4, dtype=np.float32)
		self.puntos_transformados = self.puntos.copy()

	def aplicar_transformacion(self, matriz_transformacion):
		# La multiplicación de matrices se realiza en el orden correcto para acumular transformaciones.
		# Primero la nueva transformación, luego la acumulada.
		self.matriz_transformacion_acumulada = np.dot(matriz_transformacion, self.matriz_transformacion_acumulada)
		
		# Aplicamos la transformación acumulada a los puntos originales (no a los ya transformados)
		# Esto asegura que cada nueva transformación se aplique sobre el estado original
		# y luego sobre las transformaciones acumuladas, o que se haga de forma directa.
		# La forma actual (self.puntos_homogeneos * matriz_acumulada) es para puntos fila-vector.
		# OpenGL típicamente usa columna-vector, pero con numpy y Transpuesta (T) podemos simularlo.
		self.puntos_transformados_homogeneos = np.dot(self.puntos_homogeneos, self.matriz_transformacion_acumulada.T)
		
		# Normalización para pasar de coordenadas homogéneas a cartesianas
		self.puntos_transformados = self.puntos_transformados_homogeneos[:, :3] / self.puntos_transformados_homogeneos[:, 3, np.newaxis]
		return self.puntos_transformados

	def traslacion(self, dx, dy, dz):
		matriz_traslacion = np.array([
			[1, 0, 0, dx],
			[0, 1, 0, dy],
			[0, 0, 1, dz],
			[0, 0, 0, 1]
		], dtype=np.float32)
		return self.aplicar_transformacion(matriz_traslacion)

	def rotacion(self, angulo_grados, eje):
		angulo_rad = np.radians(angulo_grados)
		matriz_rotacion = np.identity(4, dtype=np.float32)

		if eje == 'x':
			matriz_rotacion[1, 1] = np.cos(angulo_rad)
			matriz_rotacion[1, 2] = -np.sin(angulo_rad)
			matriz_rotacion[2, 1] = np.sin(angulo_rad)
			matriz_rotacion[2, 2] = np.cos(angulo_rad)
		elif eje == 'y':
			matriz_rotacion[0, 0] = np.cos(angulo_rad)
			matriz_rotacion[0, 2] = np.sin(angulo_rad)
			matriz_rotacion[2, 0] = -np.sin(angulo_rad)
			matriz_rotacion[2, 2] = np.cos(angulo_rad)
		elif eje == 'z':
			matriz_rotacion[0, 0] = np.cos(angulo_rad)
			matriz_rotacion[0, 1] = -np.sin(angulo_rad)
			matriz_rotacion[1, 0] = np.sin(angulo_rad)
			matriz_rotacion[1, 1] = np.cos(angulo_rad)
		else:
			raise ValueError("Eje de rotación no válido. Use 'x', 'y' o 'z'.")
		
		return self.aplicar_transformacion(matriz_rotacion)

	def escalamiento(self, sx, sy, sz):
		matriz_escalamiento = np.array([
			[sx, 0, 0, 0],
			[0, sy, 0, 0],
			[0, 0, sz, 0],
			[0, 0, 0, 1]
		], dtype=np.float32)
		return self.aplicar_transformacion(matriz_escalamiento)

	def reset_transformacion(self):
		# Reinicia la matriz de transformación acumulada a la identidad
		self.matriz_transformacion_acumulada = np.identity(4, dtype=np.float32)
		# Los puntos transformados vuelven a ser los originales
		self.puntos_transformados = self.puntos.copy()

# --- Configuración de PyOpenGL ---

# Vértices de un cubo unitario
vertices_cubo_unitario = np.array([
	[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],  # Cara frontal (0,1,2,3)
	[0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]   # Cara trasera (4,5,6,7)
], dtype=np.float32)

# Definición de las aristas para dibujar el cubo
aristas_cubo = [
	(0, 1), (1, 2), (2, 3), (3, 0),  # Lados de la cara frontal
	(4, 5), (5, 6), (6, 7), (7, 4),  # Lados de la cara trasera
	(0, 4), (1, 5), (2, 6), (3, 7)   # Conexión entre caras
]

# Creamos una instancia para el cubo original (que no se transforma en esta demostración)
transformador_cubo_original_display = Transformacion(vertices_cubo_unitario)

# Creamos una instancia para el cubo que sí será transformado
transformador_cubo_transformado_display = Transformacion(vertices_cubo_unitario)
# Aplicamos todas las transformaciones a este cubo una sola vez al inicio
transformador_cubo_transformado_display.rotacion(45, 'y')
transformador_cubo_transformado_display.traslacion(2, -1, 3)
transformador_cubo_transformado_display.escalamiento(0.5, 0.5, 0.5)

def init_gl():
	glClearColor(0.0, 0.0, 0.0, 1.0) # Color de fondo: negro
	glEnable(GL_DEPTH_TEST) # Habilitar prueba de profundidad para correcta visualización 3D
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	# Ajuste de la perspectiva para abarcar ambos cubos y los ejes
	# Aumentamos el far clip plane a 100.0 para asegurar que todo sea visible
	gluPerspective(45, (800 / 600), 0.1, 100.0) 
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	# Posición de la cámara ajustada para ver bien todos los elementos.
	# Miramos hacia un punto intermedio entre el origen y el centro del cubo transformado.
	gluLookAt(8, 8, 8, 1.5, 0.5, 1.5, 0, 1, 0) 

def draw_cube(vertices, color=(1, 1, 1)):
	glBegin(GL_LINES)
	glColor3fv(color)
	for edge in aristas_cubo:
		for vertex_index in edge:
			glVertex3fv(vertices[vertex_index])
	glEnd()

def draw_axes():
	glBegin(GL_LINES)
	
	# Eje X (Rojo)
	glColor3f(1.0, 0.0, 0.0)
	glVertex3f(0.0, 0.0, 0.0)
	glVertex3f(5.0, 0.0, 0.0) # Longitud del eje aumentada
	
	# Eje Y (Verde)
	glColor3f(0.0, 1.0, 0.0)
	glVertex3f(0.0, 0.0, 0.0)
	glVertex3f(0.0, 5.0, 0.0)
	
	# Eje Z (Azul)
	glColor3f(0.0, 0.0, 1.0)
	glVertex3f(0.0, 0.0, 0.0)
	glVertex3f(0.0, 0.0, 5.0)
	glEnd()

	# Etiquetas para los ejes
	draw_text((5.1, 0, 0), "X", (1.0, 0.0, 0.0), font=GLUT_BITMAP_HELVETICA_18) # Fuente más grande
	draw_text((0, 5.1, 0), "Y", (0.0, 1.0, 0.0), font=GLUT_BITMAP_HELVETICA_18)
	draw_text((0, 0, 5.1), "Z", (0.0, 0.0, 1.0), font=GLUT_BITMAP_HELVETICA_18)

def draw_text(position, text_string, color=(1,1,1), font=GLUT_BITMAP_HELVETICA_10):
	# Guardar el estado actual de la matriz de proyección y modelo
	glMatrixMode(GL_PROJECTION)
	glPushMatrix()
	glLoadIdentity()
	# Usar proyección ortográfica para dibujar texto en 2D en la pantalla
	gluOrtho2D(0, glutGet(GLUT_WINDOW_WIDTH), 0, glutGet(GLUT_WINDOW_HEIGHT))
	
	glMatrixMode(GL_MODELVIEW)
	glPushMatrix()
	glLoadIdentity()
	
	# Deshabilitar la prueba de profundidad para que el texto siempre sea visible
	glDisable(GL_DEPTH_TEST)

	glColor3fv(color)
	
	# Obtener las coordenadas de la ventana para el texto
	modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
	projection = glGetDoublev(GL_PROJECTION_MATRIX)
	viewport = glGetIntegerv(GL_VIEWPORT)
	
	# Proyectar las coordenadas 3D a la pantalla 2D
	screen_x, screen_y, screen_z = gluProject(position[0], position[1], position[2],
											modelview, projection, viewport)
	
	glRasterPos2f(screen_x + 5, screen_y + 5) # Pequeño offset para que no se superponga con el punto
	for char_code in text_string.encode('ascii'): # Convertir a bytes para glutBitmapCharacter
		glutBitmapCharacter(font, char_code)

	# Re-habilitar la prueba de profundidad y restaurar matrices
	glEnable(GL_DEPTH_TEST)
	glMatrixMode(GL_PROJECTION)
	glPopMatrix()
	glMatrixMode(GL_MODELVIEW)
	glPopMatrix()

def draw_legend():
	# Posición y tamaño de la ventana para la leyenda
	win_width = glutGet(GLUT_WINDOW_WIDTH)
	win_height = glutGet(GLUT_WINDOW_HEIGHT)
	
	# Entrar en modo 2D para dibujar la leyenda
	glMatrixMode(GL_PROJECTION)
	glPushMatrix()
	glLoadIdentity()
	gluOrtho2D(0, win_width, 0, win_height)
	
	glMatrixMode(GL_MODELVIEW)
	glPushMatrix()
	glLoadIdentity()
	
	glDisable(GL_DEPTH_TEST)

	# Coordenadas de inicio de la leyenda (ajustadas a la esquina superior izquierda)
	x_start = 10
	y_start = win_height - 30 # Más espacio desde arriba
	line_height = 20 # Más espacio entre líneas

	glColor3f(1.0, 1.0, 1.0) # Color por defecto para el texto de la leyenda

	# Título de la leyenda
	glRasterPos2f(x_start, y_start)
	for char_code in b"LEYENDA:":
		glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, char_code) # Título más grande
	
	y_start -= line_height

	# Cubo Original
	glRasterPos2f(x_start, y_start)
	glColor3f(1.0, 1.0, 1.0) # Color blanco para la etiqueta del cubo original
	for char_code in b"Cubo Original (Blanco)":
		glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, char_code)
	
	y_start -= line_height

	# Cubo Transformado
	glRasterPos2f(x_start, y_start)
	glColor3f(0.0, 1.0, 0.0) # Color verde para la etiqueta del cubo transformado
	for char_code in b"Cubo Transformado (Verde)":
		glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, char_code)

	y_start -= line_height

	# Ejes
	glRasterPos2f(x_start, y_start)
	glColor3f(1.0, 0.0, 0.0) # Color rojo para el eje X
	for char_code in b"Eje X (Rojo)":
		glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, char_code)
	
	y_start -= line_height
	
	glRasterPos2f(x_start, y_start)
	glColor3f(0.0, 1.0, 0.0) # Color verde para el eje Y
	for char_code in b"Eje Y (Verde)":
		glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, char_code)

	y_start -= line_height

	glRasterPos2f(x_start, y_start)
	glColor3f(0.0, 0.0, 1.0) # Color azul para el eje Z
	for char_code in b"Eje Z (Azul)":
		glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, char_code)
	
	# Restaurar estado de OpenGL
	glEnable(GL_DEPTH_TEST)
	glMatrixMode(GL_PROJECTION)
	glPopMatrix()
	glMatrixMode(GL_MODELVIEW)
	glPopMatrix()


def display():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()
	# Reestablecer la vista para cada frame
	gluLookAt(8, 8, 8, 1.5, 0.5, 1.5, 0, 1, 0) # Posición de la cámara

	draw_axes() # Dibujar los ejes

	# Dibujar el cubo original (blanco) y sus coordenadas
	draw_cube(vertices_cubo_unitario, color=(1, 1, 1))
	for i, vertex in enumerate(vertices_cubo_unitario):
		draw_text(vertex, f"({vertex[0]:.1f},{vertex[1]:.1f},{vertex[2]:.1f})", (1,1,1), font=GLUT_BITMAP_HELVETICA_12)
	
	# Dibujar el cubo transformado (verde) y sus coordenadas
	# Ahora siempre se dibuja, para que estén ambos cubos visibles.
	draw_cube(transformador_cubo_transformado_display.puntos_transformados, color=(0, 1, 0))
	for i, vertex in enumerate(transformador_cubo_transformado_display.puntos_transformados):
		# Usamos .2f para mostrar dos decimales en las coordenadas transformadas
		draw_text(vertex, f"({vertex[0]:.2f},{vertex[1]:.2f},{vertex[2]:.2f})", (0,1,0), font=GLUT_BITMAP_HELVETICA_12)
	
	draw_legend() # Dibujar la leyenda

	glutSwapBuffers()

def keyboard(key, x, y):
	# La barra espaciadora ya no alterna visibilidad, siempre se muestran ambos cubos.
	# Podríamos usarla para rotar la cámara o hacer otra interacción si se desea.
	if key == b'\x1b': # Escape key para salir
		glutLeaveMainLoop()
	glutPostRedisplay()

def main():
	glutInit()
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
	glutInitWindowSize(1200, 800) # Tamaño de ventana más grande para más espacio
	glutCreateWindow(b"Transformaciones 3D de Cubo con Ejes, Coordenadas y Leyenda") 

	init_gl()
	glutDisplayFunc(display)
	glutKeyboardFunc(keyboard)
	glutMainLoop()

if __name__ == "__main__":
	main()