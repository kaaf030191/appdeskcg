"""
Crear un modelo basado en datos utilizando python con pyopengl. La lectura de datos debe ser de un archivo en formato texto.

Solo tengo una columan de datos de temperatura.

Genera un gráfico tipo picos de montaña, con esos datos.

No le des rotación y dale colores distintivos entre los altos y bajos (la rotación le puedes dar en el centro pero a demanda, mediante presionado de teclas).

Agrégale la función de zoom con alguna tecla.

Al siguiente código generado, agrégale la leyenda para interpretar el gráfico.

Intégralo en el otro código y no pongas os datos, ya se lee del archivo, solo incorpora los rangos.

Ok, pero, agrégale el texto de la categoría al costado de cada color de la leyenda.

Aún no aparece el texto, como tiene negro, quizás falte darle el color blanco al texto.

Nada aún, no aparece el texto en la pantalla, para cada color, debe decir si es bajo, alto, media, y así para cada caso, al cosado de los mismo colores.
"""

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import numpy as np

# Leer temperaturas desde archivo
def leer_temperaturas(archivo):
	datos = []
	with open(archivo, 'r') as f:
		for linea in f:
			try:
				temp = float(linea.strip())
				datos.append(temp)
			except:
				continue
	return datos

# Convertir a matriz cuadrada lo más cercana posible
def generar_malla(datos):
	size = int(math.sqrt(len(datos)))
	total_necesario = size * size
	if len(datos) < total_necesario:
		datos += [0.0] * (total_necesario - len(datos))  # Rellenar con ceros
	malla = []
	for i in range(size):
		fila = []
		for j in range(size):
			idx = i * size + j
			fila.append(datos[idx])
		malla.append(fila)
	return malla

# Clasificación por percentiles
def calcular_rangos(datos):
	q1 = np.percentile(datos, 25)
	q2 = np.percentile(datos, 50)
	q3 = np.percentile(datos, 75)
	q95 = np.percentile(datos, 95)
	return q1, q2, q3, q95

def color_por_categoria(t, q1, q2, q3, q95):
	if t < q1:
		return (0.1, 0.1, 0.8)   # Muy baja
	elif t < q2:
		return (0.3, 0.5, 1.0)   # Baja
	elif t < q3:
		return (0.3, 0.9, 0.3)   # Media
	elif t < q95:
		return (1.0, 0.6, 0.0)   # Alta
	else:
		return (1.0, 0.0, 0.0)   # Muy alta

def dibujar_montaña(malla, q1, q2, q3, q95):
	filas = len(malla)
	cols = len(malla[0])
	for i in range(filas - 1):
		glBegin(GL_TRIANGLE_STRIP)
		for j in range(cols):
			for k in [i, i + 1]:
				t = malla[k][j]
				glColor3f(*color_por_categoria(t, q1, q2, q3, q95))
				glVertex3f(j * 0.3, t / 5.0, -k * 0.3)
		glEnd()

# Leyenda con texto
def dibujar_leyenda_opengl(colores_etiquetas):
	y_base = 100
	barra_x = 30
	ancho = 20
	alto = 25

	glMatrixMode(GL_PROJECTION)
	glPushMatrix()
	glLoadIdentity()
	glOrtho(0, 800, 0, 600, -1, 1)

	glMatrixMode(GL_MODELVIEW)
	glPushMatrix()
	glLoadIdentity()
	glDisable(GL_DEPTH_TEST)

	for i, (color, _) in enumerate(colores_etiquetas):
		y = y_base + i * (alto + 5)
		glColor3f(*color)
		glBegin(GL_QUADS)
		glVertex2f(barra_x, y)
		glVertex2f(barra_x + ancho, y)
		glVertex2f(barra_x + ancho, y + alto)
		glVertex2f(barra_x, y + alto)
		glEnd()

	glEnable(GL_DEPTH_TEST)
	glPopMatrix()
	glMatrixMode(GL_PROJECTION)
	glPopMatrix()
	glMatrixMode(GL_MODELVIEW)

def dibujar_texto_leyenda(colores_etiquetas, font, screen):
	y_base = 100
	barra_x = 30
	ancho = 20
	alto = 25
	espaciado = 10

	for i, (_, etiqueta) in enumerate(colores_etiquetas):
		y = y_base + i * (alto + 5)
		text_surface = font.render(etiqueta, True, (255, 255, 255))  # Texto blanco
		screen.blit(text_surface, (barra_x + ancho + espaciado, y))

def main():
	pygame.init()
	display = (800, 600)
	screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
	pygame.display.set_caption("Picos de Montaña - Temperaturas Categorizadas")
	font = pygame.font.SysFont("Arial", 16)

	gluPerspective(45, (display[0] / display[1]), 0.1, 100.0)
	glTranslatef(-3, -2, -15)
	glEnable(GL_DEPTH_TEST)

	temperaturas = leer_temperaturas("temperatura.txt")
	malla = generar_malla(temperaturas)
	q1, q2, q3, q95 = calcular_rangos(temperaturas)

	rot_x = 20
	rot_y = 0

	colores_etiquetas = [
		((0.1, 0.1, 0.8), "Muy baja"),
		((0.3, 0.5, 1.0), "Baja"),
		((0.3, 0.9, 0.3), "Media"),
		((1.0, 0.6, 0.0), "Alta"),
		((1.0, 0.0, 0.0), "Muy alta"),
	]

	ejecutando = True
	while ejecutando:
		for evento in pygame.event.get():
			if evento.type == pygame.QUIT:
				ejecutando = False
			elif evento.type == pygame.KEYDOWN:
				if evento.key == pygame.K_LEFT:
					rot_y -= 5
				elif evento.key == pygame.K_RIGHT:
					rot_y += 5
				elif evento.key == pygame.K_UP:
					rot_x -= 5
				elif evento.key == pygame.K_DOWN:
					rot_x += 5

		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

		glPushMatrix()
		glRotatef(rot_x, 1, 0, 0)
		glRotatef(rot_y, 0, 1, 0)
		dibujar_montaña(malla, q1, q2, q3, q95)
		glPopMatrix()

		# Leyenda con OpenGL (bloques de color)
		dibujar_leyenda_opengl(colores_etiquetas)

		# Leyenda con texto usando pygame (debe ir después de OpenGL)
		dibujar_texto_leyenda(colores_etiquetas, font, screen)

		pygame.display.flip()
		pygame.time.wait(10)

	pygame.quit()

if __name__ == "__main__":
	main()