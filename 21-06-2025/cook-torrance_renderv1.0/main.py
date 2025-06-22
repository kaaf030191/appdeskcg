import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math
import glm  # IMPORTAR GLM ANTES DE USARLO

def compilar_shader(fuente, tipo_shader):
	shader = glCreateShader(tipo_shader)
	glShaderSource(shader, fuente)
	glCompileShader(shader)

	if not glGetShaderiv(shader, GL_COMPILE_STATUS):
		error = glGetShaderInfoLog(shader).decode()
		print(f"Error al compilar shader ({'vertex' if tipo_shader == GL_VERTEX_SHADER else 'fragment'}):")
		print(error)
		return None
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

	void main()
	{
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

	void main()
	{
		float ambientStrength = 0.1;
		float specularStrength = 0.5;
		float shininess = 32.0;

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

	if vs is None or fs is None:
		return None

	programa = glCreateProgram()
	glAttachShader(programa, vs)
	glAttachShader(programa, fs)
	glLinkProgram(programa)

	if not glGetProgramiv(programa, GL_LINK_STATUS):
		print("Error al enlazar shaders:")
		print(glGetProgramInfoLog(programa).decode())
		return None

	glDeleteShader(vs)
	glDeleteShader(fs)

	return programa

def generar_esfera(radio, sectores, anillos):
	vertices = []
	normales = []
	indices = []

	sector_step = 2 * math.pi / sectores
	ring_step = math.pi / anillos

	for i in range(anillos + 1):
		ring_angle = math.pi / 2 - i * ring_step
		xy = radio * math.cos(ring_angle)
		z = radio * math.sin(ring_angle)

		for j in range(sectores + 1):
			sector_angle = j * sector_step
			x = xy * math.cos(sector_angle)
			y = xy * math.sin(sector_angle)
			vertices.append([x, y, z])
			normales.append([x / radio, y / radio, z / radio])

	for i in range(anillos):
		for j in range(sectores):
			k1 = i * (sectores + 1) + j
			k2 = k1 + sectores + 1
			indices += [k1, k2, k1 + 1, k1 + 1, k2, k2 + 1]

	return np.array(vertices, dtype=np.float32), np.array(normales, dtype=np.float32), np.array(indices, dtype=np.uint32)

def main():
	pygame.init()
	display = (800, 600)
	pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
	pygame.display.set_caption("Esfera con Blinn-Phong")

	glEnable(GL_DEPTH_TEST)

	vertices, normales, indices = generar_esfera(1.0, 32, 32)
	num_indices = len(indices)

	vao = glGenVertexArrays(1)
	glBindVertexArray(vao)

	vbo_vertices = glGenBuffers(1)
	glBindBuffer(GL_ARRAY_BUFFER, vbo_vertices)
	glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
	glEnableVertexAttribArray(0)

	vbo_normales = glGenBuffers(1)
	glBindBuffer(GL_ARRAY_BUFFER, vbo_normales)
	glBufferData(GL_ARRAY_BUFFER, normales.nbytes, normales, GL_STATIC_DRAW)
	glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)
	glEnableVertexAttribArray(1)

	ebo = glGenBuffers(1)
	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
	glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

	programa = crear_programa_shader()
	if programa is None:
		pygame.quit()
		return

	glUseProgram(programa)
	projection = glm.perspective(glm.radians(45), display[0]/display[1], 0.1, 100.0)
	glUniformMatrix4fv(glGetUniformLocation(programa, "projection"), 1, GL_FALSE, glm.value_ptr(projection))

	view = glm.lookAt(glm.vec3(0, 0, 5), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))
	glUniformMatrix4fv(glGetUniformLocation(programa, "view"), 1, GL_FALSE, glm.value_ptr(view))

	model = glm.mat4(1.0)
	glUniformMatrix4fv(glGetUniformLocation(programa, "model"), 1, GL_FALSE, glm.value_ptr(model))

	glUniform3f(glGetUniformLocation(programa, "lightPos"), 2.0, 2.0, 2.0)
	glUniform3f(glGetUniformLocation(programa, "viewPos"), 0.0, 0.0, 5.0)
	glUniform3f(glGetUniformLocation(programa, "lightColor"), 1.0, 1.0, 1.0)
	glUniform3f(glGetUniformLocation(programa, "objectColor"), 0.8, 0.2, 0.2)

	clock = pygame.time.Clock()
	running = True

	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
				running = False

		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

		tiempo = pygame.time.get_ticks() / 1000.0
		model = glm.rotate(glm.mat4(1.0), tiempo, glm.vec3(0.0, 1.0, 0.0))
		glUniformMatrix4fv(glGetUniformLocation(programa, "model"), 1, GL_FALSE, glm.value_ptr(model))

		glBindVertexArray(vao)
		glDrawElements(GL_TRIANGLES, num_indices, GL_UNSIGNED_INT, None)

		pygame.display.flip()
		clock.tick(60)

	glDeleteVertexArrays(1, [vao])
	glDeleteBuffers(1, [vbo_vertices])
	glDeleteBuffers(1, [vbo_normales])
	glDeleteBuffers(1, [ebo])
	glDeleteProgram(programa)
	pygame.quit()

if __name__ == "__main__":
	main()