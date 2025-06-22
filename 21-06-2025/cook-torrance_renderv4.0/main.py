import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math
import glm

# --- Funciones de Utilidad OpenGL ---
def compilar_shader(fuente, tipo_shader):
	"""
	Compila un shader de OpenGL.
	Args:
		fuente (str): El código fuente del shader.
		tipo_shader (int): El tipo de shader (GL_VERTEX_SHADER o GL_FRAGMENT_SHADER).
	Returns:
		int: El ID del shader compilado, o None si hay un error.
	"""
	shader = glCreateShader(tipo_shader)
	glShaderSource(shader, fuente)
	glCompileShader(shader)

	# Verificar errores de compilación
	if not glGetShaderiv(shader, GL_COMPILE_STATUS):
		error = glGetShaderInfoLog(shader).decode()
		print(f"Error al compilar shader ({'vertex' if tipo_shader == GL_VERTEX_SHADER else 'fragment'}):")
		print(error)
		glDeleteShader(shader)
		return None
	return shader

def crear_programa_shader():
	"""
	Crea y enlaza un programa de shaders con un vertex y fragment shader.
	Returns:
		int: El ID del programa de shader, o None si hay un error.
	"""
	# Vertex Shader
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

	# Fragment Shader (Cook-Torrance PBR)
	fragment_shader = """
	#version 330 core
	#define PI 3.14159265359

	in vec3 FragPos;
	in vec3 Normal;

	out vec4 FragColor;

	uniform vec3 lightPos;
	uniform vec3 viewPos;
	uniform vec3 lightColor;
	uniform vec3 objectColor;
	uniform float roughness;
	uniform float metallic;

	float DistributionGGX(vec3 N, vec3 H, float roughness)
	{
		float a = roughness*roughness;
		float a2 = a*a;
		float NdotH = max(dot(N, H), 0.0);
		float NdotH2 = NdotH*NdotH;

		float nom   = a2;
		float denom = (NdotH2 * (a2 - 1.0) + 1.0);
		denom = PI * denom * denom;

		return nom / denom;
	}

	float GeometrySchlickGGX(float NdotV, float roughness)
	{
		float r = roughness;
		float k = (r * r) / 2.0;

		float nom   = NdotV;
		float denom = NdotV * (1.0 - k) + k;

		return nom / denom;
	}

	float GeometrySmith(vec3 N, vec3 V, vec3 L, float roughness)
	{
		float NdotV = max(dot(N, V), 0.0);
		float NdotL = max(dot(N, L), 0.0);
		float ggx2 = GeometrySchlickGGX(NdotV, roughness);
		float ggx1 = GeometrySchlickGGX(NdotL, roughness);

		return ggx1 * ggx2;
	}

	vec3 FresnelSchlick(float cosTheta, vec3 F0)
	{
		return F0 + (1.0 - F0) * pow(clamp(1.0 - cosTheta, 0.0, 1.0), 5.0);
	}

	void main()
	{
		vec3 N = normalize(Normal);
		vec3 V = normalize(viewPos - FragPos);
		vec3 L = normalize(lightPos - FragPos);
		vec3 H = normalize(L + V);

		vec3 F0 = vec3(0.04);
		F0 = mix(F0, objectColor, metallic);

		float NDF = DistributionGGX(N, H, roughness);
		float G = GeometrySmith(N, V, L, roughness);
		vec3 F = FresnelSchlick(max(dot(H, V), 0.0), F0);

		vec3 kS = F;
		vec3 kD = vec3(1.0) - kS;
		kD *= (1.0 - metallic);

		float NdotL = max(dot(N, L), 0.0);

		vec3 numerator    = NDF * G * F;
		float denominator = 4.0 * max(dot(N, V), 0.0) * NdotL + 0.0001;
		vec3 specular     = numerator / denominator;

		vec3 radiance = lightColor;
		vec3 Lo = (kD * objectColor / PI + specular) * radiance * NdotL;

		vec3 ambient = 0.03 * objectColor;

		vec3 finalColor = ambient + Lo;

		FragColor = vec4(finalColor, 1.0);
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
		glDeleteProgram(programa)
		return None

	glDeleteShader(vs)
	glDeleteShader(fs)

	return programa

def generar_esfera(radio, sectores, anillos):
	"""
	Genera los datos de vértices, normales e índices para una esfera.
	"""
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
			nx, ny, nz = x / radio, y / radio, z / radio
			normales.append([nx, ny, nz])

	for i in range(anillos):
		for j in range(sectores):
			k1 = i * (sectores + 1) + j
			k2 = k1 + sectores + 1

			indices.append(k1)
			indices.append(k2)
			indices.append(k1 + 1)

			indices.append(k1 + 1)
			indices.append(k2)
			indices.append(k2 + 1)

	return np.array(vertices, dtype=np.float32), np.array(normales, dtype=np.float32), np.array(indices, dtype=np.uint32)

def generar_cubo(lado):
	"""
	Genera los datos de vértices, normales e índices para un cubo.
	El cubo se centra en el origen.
	"""
	half_lado = lado / 2.0

	# Los vértices de un cubo. Nota: se repiten para asegurar normales correctas por cara.
	vertices = np.array([
		# Cara frontal
		-half_lado, -half_lado,  half_lado, # 0
		half_lado, -half_lado,  half_lado, # 1
		half_lado,  half_lado,  half_lado, # 2
		-half_lado,  half_lado,  half_lado, # 3

		# Cara trasera
		-half_lado, -half_lado, -half_lado, # 4
		half_lado, -half_lado, -half_lado, # 5
		half_lado,  half_lado, -half_lado, # 6
		-half_lado,  half_lado, -half_lado, # 7

		# Cara izquierda
		-half_lado, -half_lado, -half_lado, # 8 (reuso de 4)
		-half_lado, -half_lado,  half_lado, # 9 (reuso de 0)
		-half_lado,  half_lado,  half_lado, # 10 (reuso de 3)
		-half_lado,  half_lado, -half_lado, # 11 (reuso de 7)

		# Cara derecha
		half_lado, -half_lado,  half_lado, # 12 (reuso de 1)
		half_lado, -half_lado, -half_lado, # 13 (reuso de 5)
		half_lado,  half_lado, -half_lado, # 14 (reuso de 6)
		half_lado,  half_lado,  half_lado, # 15 (reuso de 2)

		# Cara superior
		-half_lado,  half_lado,  half_lado, # 16 (reuso de 3)
		half_lado,  half_lado,  half_lado, # 17 (reuso de 2)
		half_lado,  half_lado, -half_lado, # 18 (reuso de 6)
		-half_lado,  half_lado, -half_lado, # 19 (reuso de 7)

		# Cara inferior
		-half_lado, -half_lado, -half_lado, # 20 (reuso de 4)
		half_lado, -half_lado, -half_lado, # 21 (reuso de 5)
		half_lado, -half_lado,  half_lado, # 22 (reuso de 1)
		-half_lado, -half_lado,  half_lado, # 23 (reuso de 0)
	], dtype=np.float32)

	# Normales por cara
	normales = np.array([
		# Cara frontal
		0.0, 0.0, 1.0,  0.0, 0.0, 1.0,  0.0, 0.0, 1.0,  0.0, 0.0, 1.0,
		# Cara trasera
		0.0, 0.0, -1.0, 0.0, 0.0, -1.0, 0.0, 0.0, -1.0, 0.0, 0.0, -1.0,
		# Cara izquierda
		-1.0, 0.0, 0.0, -1.0, 0.0, 0.0, -1.0, 0.0, 0.0, -1.0, 0.0, 0.0,
		# Cara derecha
		1.0, 0.0, 0.0,  1.0, 0.0, 0.0,  1.0, 0.0, 0.0,  1.0, 0.0, 0.0,
		# Cara superior
		0.0, 1.0, 0.0,  0.0, 1.0, 0.0,  0.0, 1.0, 0.0,  0.0, 1.0, 0.0,
		# Cara inferior
		0.0, -1.0, 0.0, 0.0, -1.0, 0.0, 0.0, -1.0, 0.0, 0.0, -1.0, 0.0,
	], dtype=np.float32).reshape(-1, 3) # Reshape para que cada normal sea un vec3

	# Índices para dibujar cada cara como dos triángulos
	indices = np.array([
		0, 1, 2,  2, 3, 0,       # Cara frontal
		4, 5, 6,  6, 7, 4,       # Cara trasera
		8, 9, 10, 10, 11, 8,     # Cara izquierda
		12, 13, 14, 14, 15, 12,  # Cara derecha
		16, 17, 18, 18, 19, 16,  # Cara superior
		20, 21, 22, 22, 23, 20   # Cara inferior
	], dtype=np.uint32)

	return vertices, normales, indices


# --- Función Principal ---
def main():
	pygame.init()
	display = (800, 600)
	pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
	pygame.display.set_caption("Esfera y Cubo con Cook-Torrance")

	glEnable(GL_DEPTH_TEST)
	glClearColor(0.1, 0.1, 0.1, 1.0)

	programa = crear_programa_shader()
	if programa is None:
		pygame.quit()
		return

	# --- Configuración de la Esfera ---
	vertices_esfera, normales_esfera, indices_esfera = generar_esfera(1.0, 32, 32)
	num_indices_esfera = len(indices_esfera)

	vao_esfera = glGenVertexArrays(1)
	glBindVertexArray(vao_esfera)

	vbo_vertices_esfera = glGenBuffers(1)
	glBindBuffer(GL_ARRAY_BUFFER, vbo_vertices_esfera)
	glBufferData(GL_ARRAY_BUFFER, vertices_esfera.nbytes, vertices_esfera, GL_STATIC_DRAW)
	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
	glEnableVertexAttribArray(0)

	vbo_normales_esfera = glGenBuffers(1)
	glBindBuffer(GL_ARRAY_BUFFER, vbo_normales_esfera)
	glBufferData(GL_ARRAY_BUFFER, normales_esfera.nbytes, normales_esfera, GL_STATIC_DRAW)
	glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)
	glEnableVertexAttribArray(1)

	ebo_esfera = glGenBuffers(1)
	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo_esfera)
	glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices_esfera.nbytes, indices_esfera, GL_STATIC_DRAW)

	glBindVertexArray(0) # Desvincular VAO de la esfera

	# --- Configuración del Cubo ---
	vertices_cubo, normales_cubo, indices_cubo = generar_cubo(1.0) # Cubo de lado 1.0
	num_indices_cubo = len(indices_cubo)

	vao_cubo = glGenVertexArrays(1)
	glBindVertexArray(vao_cubo)

	vbo_vertices_cubo = glGenBuffers(1)
	glBindBuffer(GL_ARRAY_BUFFER, vbo_vertices_cubo)
	glBufferData(GL_ARRAY_BUFFER, vertices_cubo.nbytes, vertices_cubo, GL_STATIC_DRAW)
	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
	glEnableVertexAttribArray(0)

	vbo_normales_cubo = glGenBuffers(1)
	glBindBuffer(GL_ARRAY_BUFFER, vbo_normales_cubo)
	glBufferData(GL_ARRAY_BUFFER, normales_cubo.nbytes, normales_cubo, GL_STATIC_DRAW)
	glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)
	glEnableVertexAttribArray(1)

	ebo_cubo = glGenBuffers(1)
	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo_cubo)
	glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices_cubo.nbytes, indices_cubo, GL_STATIC_DRAW)

	glBindVertexArray(0) # Desvincular VAO del cubo

	# --- Configuración Uniforme General ---
	glUseProgram(programa)
	projection = glm.perspective(glm.radians(45.0), display[0] / display[1], 0.1, 100.0)
	glUniformMatrix4fv(glGetUniformLocation(programa, "projection"), 1, GL_FALSE, glm.value_ptr(projection))

	view = glm.lookAt(
		glm.vec3(0, 2, 5),  # Posición cámara, un poco más arriba para ver ambos
		glm.vec3(0, 0, 0),
		glm.vec3(0, 1, 0)
	)
	glUniformMatrix4fv(glGetUniformLocation(programa, "view"), 1, GL_FALSE, glm.value_ptr(view))

	glUniform3f(glGetUniformLocation(programa, "lightPos"), 2.0, 2.0, 2.0)
	glUniform3f(glGetUniformLocation(programa, "viewPos"), 0.0, 2.0, 5.0) # Ajustar viewPos a la cámara
	glUniform3f(glGetUniformLocation(programa, "lightColor"), 1.0, 1.0, 1.0)

	# --- Bucle Principal ---
	clock = pygame.time.Clock()
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
				running = False

		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		glUseProgram(programa)

		tiempo = pygame.time.get_ticks() / 1000.0

		# --- Dibujar Esfera ---
		# Posición de la esfera: a la izquierda
		model_esfera = glm.translate(glm.mat4(1.0), glm.vec3(-1.5, 0.0, 0.0))
		model_esfera = glm.rotate(model_esfera, tiempo, glm.vec3(0.0, 1.0, 0.0)) # Rotar
		glUniformMatrix4fv(glGetUniformLocation(programa, "model"), 1, GL_FALSE, glm.value_ptr(model_esfera))

		# Propiedades del material para la esfera (ej. un metal dorado)
		glUniform3f(glGetUniformLocation(programa, "objectColor"), 1.0, 0.84, 0.0) # Dorado
		glUniform1f(glGetUniformLocation(programa, "roughness"), 0.2)
		glUniform1f(glGetUniformLocation(programa, "metallic"), 1.0) # Es un metal

		glBindVertexArray(vao_esfera)
		glDrawElements(GL_TRIANGLES, num_indices_esfera, GL_UNSIGNED_INT, None)


		# --- Dibujar Cubo ---
		# Posición del cubo: a la derecha
		model_cubo = glm.translate(glm.mat4(1.0), glm.vec3(1.5, 0.0, 0.0))
		model_cubo = glm.rotate(model_cubo, tiempo * 0.7, glm.vec3(1.0, 0.5, 0.0)) # Rotar diferente
		glUniformMatrix4fv(glGetUniformLocation(programa, "model"), 1, GL_FALSE, glm.value_ptr(model_cubo))

		# Propiedades del material para el cubo (ej. un plástico azul)
		glUniform3f(glGetUniformLocation(programa, "objectColor"), 0.1, 0.2, 0.8) # Azul
		glUniform1f(glGetUniformLocation(programa, "roughness"), 0.7)
		glUniform1f(glGetUniformLocation(programa, "metallic"), 0.0) # Es un dieléctrico (plástico)

		glBindVertexArray(vao_cubo)
		glDrawElements(GL_TRIANGLES, num_indices_cubo, GL_UNSIGNED_INT, None)


		pygame.display.flip()
		clock.tick(60)

	# --- Limpieza ---
	glDeleteVertexArrays(1, [vao_esfera])
	glDeleteBuffers(1, [vbo_vertices_esfera])
	glDeleteBuffers(1, [vbo_normales_esfera])
	glDeleteBuffers(1, [ebo_esfera])

	glDeleteVertexArrays(1, [vao_cubo])
	glDeleteBuffers(1, [vbo_vertices_cubo])
	glDeleteBuffers(1, [vbo_normales_cubo])
	glDeleteBuffers(1, [ebo_cubo])

	glDeleteProgram(programa)
	pygame.quit()

if __name__ == "__main__":
	main()