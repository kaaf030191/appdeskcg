"""
crear un triángulo en 2D cuyos vértices deben de estar en una matriz. mediante python con OpenGL.
"""
# Importamos los módulos necesarios de PyOpenGL
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Definimos los vértices del triángulo en una matriz.
# Cada sublista representa un vértice con coordenadas (x, y)
vertices = [
	[-0.5, -0.5],  # Vértice inferior izquierdo
	[ 0.5, -0.5],  # Vértice inferior derecho
	[ 0.0,  0.5]   # Vértice superior central
]

# Esta función se encarga de dibujar el triángulo
def draw_triangle():
	glClear(GL_COLOR_BUFFER_BIT)  # Limpia el búfer de color con el color de fondo

	glBegin(GL_TRIANGLES)  # Inicia la especificación de un triángulo
	for vertex in vertices:
		glVertex2f(vertex[0], vertex[1])  # Enviamos cada vértice a OpenGL
	glEnd()  # Finaliza la especificación de los vértices

	glFlush()  # Fuerza el renderizado inmediato en pantalla

# Función principal donde se configura OpenGL y se lanza la ventana
def main():
	glutInit()  # Inicializa GLUT
	glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)  # Usa un búfer único y modo de color RGB
	glutInitWindowSize(500, 500)  # Tamaño de la ventana (ancho x alto en píxeles)
	glutCreateWindow(b"Triangulo 2D en OpenGL")  # Crea una ventana con un título (sin acentos para compatibilidad)

	glClearColor(1.0, 1.0, 1.0, 1.0)  # Establece el color de fondo como blanco (RGBA)
	glColor3f(0.0, 0.0, 1.0)  # Establece el color del triángulo como azul (RGB)

	glMatrixMode(GL_PROJECTION)  # Cambia a la matriz de proyección
	gluOrtho2D(-1, 1, -1, 1)  # Define el sistema de coordenadas 2D (de -1 a 1 en X e Y)

	glutDisplayFunc(draw_triangle)  # Asigna la función de dibujo para la ventana
	glutMainLoop()  # Inicia el bucle principal de eventos (renderizado y entrada del usuario)

# Punto de entrada del programa
if __name__ == "__main__":
	main()