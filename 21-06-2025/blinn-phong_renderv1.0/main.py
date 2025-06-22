import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math
import glm  # Asegúrate de tener PyGLM instalado

def compilar_shader(fuente, tipo_shader):
	shader = glCreateShader(tipo_shader)
	glShaderSource(shader, fuente)
	glCompileShader(shader)
	if not glGetShaderiv(shader, GL_COMPILE_STATUS):
		error = glGetShaderInfoLog(shader).decode()
		tipo = 'Vertex' if tipo_shader == GL_VERTEX_SHADER else 'Fragment'
		raise RuntimeError(f"Error compilando {tipo} Shader:\n{error}")
	return shader

def crear_programa_shader():
	vertex_shader = """
	#version 330 core
	layout(location = 0) in vec3 position;
	layout(location = 1) in vec3 normal;

	out vec3 FragPos;
	out vec3 Normal;

	uniform mat4 model;
	uniform mat4 view;
	uniform mat4 projection;

	void main() {
		FragPos = vec3(model * vec4(position, 1.0));
		Normal = mat3(transpose(inverse(model))) * normal;
		gl_Position = projection * view * model * vec4(position, 1.0);
	}
	"""

	fragment_shader = """
	#version 330 core
	in vec3 FragPos;
	in vec3 Normal;

	out vec4 FragColor;

	uniform vec3 lightPos;
	uniform vec3 viewPos;
	uniform vec3 lightColor;
	uniform vec3 objectColor;

	void main() {
		float ambientStrength = 0.1;
		float specularStrength = 0.7;
		float shininess = 64.0;

		vec3 ambient = ambientStrength * lightColor;

		vec3 norm = normalize(Normal);
		vec3 lightDir = normalize(lightPos - FragPos);
		float diff = max(dot(norm, lightDir), 0.0);
		vec3 diffuse = diff * lightColor;

		vec3 viewDir = normalize(viewPos - FragPos);
		vec3 halfwayDir = normalize(lightDir + viewDir);
		float spec = pow(max(dot(norm, halfwayDir), 0.0), shininess);
		vec3 specular = specularStrength * spec * lightColor;

		vec3 result = (ambient + diffuse + specular) * objectColor;
		FragColor = vec4(result, 1.0);
	}
	"""

	vs = compilar_shader(vertex_shader, GL_VERTEX_SHADER)
	fs = compilar_shader(fragment_shader, GL_FRAGMENT_SHADER)

	programa = glCreateProgram()
	glAttachShader(programa, vs)
	glAttachShader(programa, fs)
	glLinkProgram(programa)

	if not glGetProgramiv(programa, GL_LINK_STATUS):
		raise RuntimeError(glGetProgramInfoLog(programa).decode())

	glDeleteShader(vs)
	glDeleteShader(fs)

	return programa

def generar_esfera(radio, sectores, anillos):
	vertices = []
	normales = []
	indices = []

	for i in range(anillos + 1):
		phi = math.pi * i / anillos
		for j in range(sectores + 1):
			theta = 2 * math.pi * j / sectores
			x = radio * math.sin(phi) * math.cos(theta)
			y = radio * math.sin(phi) * math.sin(theta)
			z = radio * math.cos(phi)
			vertices.append([x, y, z])
			normales.append([x / radio, y / radio, z / radio])

	for i in range(anillos):
		for j in range(sectores):
			k1 = i * (sectores + 1) + j
			k2 = k1 + sectores + 1
			indices.extend([k1, k2, k1 + 1, k1 + 1, k2, k2 + 1])

	return np.array(vertices, dtype=np.float32), np.array(normales, dtype=np.float32), np.array(indices, dtype=np.uint32)

def main():
	pygame.init()
	display = (800, 600)
	pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
	pygame.display.set_caption("Esfera con Iluminación Blinn-Phong")

	glEnable(GL_DEPTH_TEST)

	vertices, normales, indices = generar_esfera(1.0, 64, 64)

	vao = glGenVertexArrays(1)
	glBindVertexArray(vao)

	vbo_v = glGenBuffers(1)
	glBindBuffer(GL_ARRAY_BUFFER, vbo_v)
	glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
	glEnableVertexAttribArray(0)

	vbo_n = glGenBuffers(1)
	glBindBuffer(GL_ARRAY_BUFFER, vbo_n)
	glBufferData(GL_ARRAY_BUFFER, normales.nbytes, normales, GL_STATIC_DRAW)
	glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)
	glEnableVertexAttribArray(1)

	ebo = glGenBuffers(1)
	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
	glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

	programa = crear_programa_shader()
	glUseProgram(programa)

	projection = glm.perspective(glm.radians(45.0), display[0] / display[1], 0.1, 100.0)
	view = glm.lookAt(glm.vec3(0, 0, 5), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))
	model = glm.mat4(1.0)

	glUniformMatrix4fv(glGetUniformLocation(programa, "projection"), 1, GL_FALSE, glm.value_ptr(projection))
	glUniformMatrix4fv(glGetUniformLocation(programa, "view"), 1, GL_FALSE, glm.value_ptr(view))

	glUniform3f(glGetUniformLocation(programa, "viewPos"), 0.0, 0.0, 5.0)
	glUniform3f(glGetUniformLocation(programa, "lightColor"), 1.0, 0.2, 0.2)  # Luz roja fuerte
	glUniform3f(glGetUniformLocation(programa, "objectColor"), 1.0, 1.0, 1.0)  # Esfera blanca

	clock = pygame.time.Clock()
	while True:
		for e in pygame.event.get():
			if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
				pygame.quit()
				return

		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

		tiempo = pygame.time.get_ticks() / 1000.0
		model = glm.rotate(glm.mat4(1.0), tiempo, glm.vec3(0, 1, 0))
		glUniformMatrix4fv(glGetUniformLocation(programa, "model"), 1, GL_FALSE, glm.value_ptr(model))

		glUniform3f(glGetUniformLocation(programa, "lightPos"), 2.0 * math.cos(tiempo), 2.0, 2.0 * math.sin(tiempo))

		glBindVertexArray(vao)
		glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)

		pygame.display.flip()
		clock.tick(60)

if __name__ == "__main__":
	main()