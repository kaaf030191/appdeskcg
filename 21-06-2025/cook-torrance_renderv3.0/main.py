import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math
import glm # Asegúrate de tener instalada la librería PyGLM

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
		glDeleteShader(shader) # Liberar el shader si falla la compilación
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
	// Define PI para usar en el shader
	#define PI 3.14159265359

	in vec3 FragPos;
	in vec3 Normal;

	out vec4 FragColor;

	uniform vec3 lightPos;
	uniform vec3 viewPos;
	uniform vec3 lightColor;
	uniform vec3 objectColor; // Esto actúa como el albedo/color base
	uniform float roughness;  // Rugosidad del material (0.0 = suave, 1.0 = áspero)
	uniform float metallic;   // Metalicidad del material (0.0 = dieléctrico, 1.0 = metal)

	// Función de Distribución Normal (NDF) - Trowbridge-Reitz GGX
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

	// Función de Geometría - Schlick-GGX (para una dirección, vista o luz)
	float GeometrySchlickGGX(float NdotV, float roughness)
	{
		float r = roughness;
		float k = (r * r) / 2.0; // k para iluminación directa

		float nom   = NdotV;
		float denom = NdotV * (1.0 - k) + k;

		return nom / denom;
	}

	// Método de Smith para combinar las funciones de Geometría
	float GeometrySmith(vec3 N, vec3 V, vec3 L, float roughness)
	{
		float NdotV = max(dot(N, V), 0.0);
		float NdotL = max(dot(N, L), 0.0);
		float ggx2 = GeometrySchlickGGX(NdotV, roughness);
		float ggx1 = GeometrySchlickGGX(NdotL, roughness);

		return ggx1 * ggx2;
	}

	// Aproximación de Fresnel-Schlick
	vec3 FresnelSchlick(float cosTheta, vec3 F0)
	{
		return F0 + (1.0 - F0) * pow(clamp(1.0 - cosTheta, 0.0, 1.0), 5.0);
	}

	void main()
	{
		vec3 N = normalize(Normal);
		vec3 V = normalize(viewPos - FragPos); // Vector de vista (fragmento a cámara)
		vec3 L = normalize(lightPos - FragPos); // Vector de luz (fragmento a luz)
		vec3 H = normalize(L + V); // Vector a medio camino

		// F0 (reflectividad base en incidencia normal)
		// Para dieléctricos (no metales), F0 es típicamente 0.04.
		// Para metales, F0 es el color del albedo (objectColor).
		vec3 F0 = vec3(0.04);
		F0 = mix(F0, objectColor, metallic); // Interpola entre F0_dieléctrico y albedo según la metalicidad

		// Componentes del BRDF de Cook-Torrance
		float NDF = DistributionGGX(N, H, roughness);
		float G = GeometrySmith(N, V, L, roughness);
		vec3 F = FresnelSchlick(max(dot(H, V), 0.0), F0);

		// kS: Reflectancia especular (cantidad de luz reflejada especularmente)
		vec3 kS = F;
		// kD: Reflectancia difusa (cantidad de luz reflejada difusamente)
		vec3 kD = vec3(1.0) - kS;
		// Para los metales, no hay componente difusa, por lo que kD se vuelve 0
		kD *= (1.0 - metallic);

		// Contribución de la luz
		float NdotL = max(dot(N, L), 0.0); // N.L, clamped a 0.0

		// BRDF especular de Cook-Torrance
		vec3 numerator    = NDF * G * F;
		float denominator = 4.0 * max(dot(N, V), 0.0) * NdotL + 0.0001; // Se añade un épsilon para evitar la división por cero
		vec3 specular     = numerator / denominator; // F_especular

		// Radiación de la luz (asumiendo que lightColor representa la intensidad de la luz)
		vec3 radiance = lightColor;

		// Ecuación PBR final para iluminación directa
		// Lo = (kD * (Albedo / PI) + F_especular) * Radiance * N.L
		vec3 Lo = (kD * objectColor / PI + specular) * radiance * NdotL;

		// Añadir un pequeño término ambiental (normalmente manejado por iluminación basada en imágenes en PBR real)
		vec3 ambient = 0.03 * objectColor; // Luz ambiental simple escalada por el color del objeto

		vec3 finalColor = ambient + Lo;

		FragColor = vec4(finalColor, 1.0);
	}
	"""

	# Compilar shaders
	vs = compilar_shader(vertex_shader, GL_VERTEX_SHADER)
	fs = compilar_shader(fragment_shader, GL_FRAGMENT_SHADER)

	if vs is None or fs is None:
		return None

	# Crear programa
	programa = glCreateProgram()
	glAttachShader(programa, vs)
	glAttachShader(programa, fs)
	glLinkProgram(programa)

	# Verificar errores de enlace
	if not glGetProgramiv(programa, GL_LINK_STATUS):
		print("Error al enlazar shaders:")
		print(glGetProgramInfoLog(programa).decode())
		glDeleteProgram(programa)
		return None

	# Los shaders se pueden eliminar después de haberlos enlazado al programa
	glDeleteShader(vs)
	glDeleteShader(fs)

	return programa

def generar_esfera(radio, sectores, anillos):
	"""
	Genera los datos de vértices, normales e índices para una esfera.
	Args:
		radio (float): El radio de la esfera.
		sectores (int): El número de divisiones horizontales (longitud).
		anillos (int): El número de divisiones verticales (latitud).
	Returns:
		tuple: (vertices, normales, indices) como arrays de NumPy.
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

			nx = x / radio
			ny = y / radio
			nz = z / radio
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

# --- Función Principal ---
def main():
	"""
	Función principal para inicializar Pygame y OpenGL, configurar la escena
	y ejecutar el bucle de renderizado.
	"""
	pygame.init()
	display = (800, 600)
	pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
	pygame.display.set_caption("Esfera con Cook-Torrance")

	# Configurar OpenGL
	glEnable(GL_DEPTH_TEST)
	glClearColor(0.1, 0.1, 0.1, 1.0)

	# Generar esfera
	vertices, normales, indices = generar_esfera(1.0, 32, 32)
	num_indices = len(indices)

	# Crear VBOs y VAO
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

	glBindVertexArray(0)

	# Crear programa de shaders
	programa = crear_programa_shader()
	if programa is None:
		glDeleteVertexArrays(1, [vao])
		glDeleteBuffers(1, [vbo_vertices])
		glDeleteBuffers(1, [vbo_normales])
		glDeleteBuffers(1, [ebo])
		pygame.quit()
		return

	# Configurar proyección
	glUseProgram(programa)
	projection = glm.perspective(glm.radians(45.0), display[0] / display[1], 0.1, 100.0)
	glUniformMatrix4fv(glGetUniformLocation(programa, "projection"), 1, GL_FALSE, glm.value_ptr(projection))

	# Configurar cámara
	view = glm.lookAt(
		glm.vec3(0, 0, 5),
		glm.vec3(0, 0, 0),
		glm.vec3(0, 1, 0)
	)
	glUniformMatrix4fv(glGetUniformLocation(programa, "view"), 1, GL_FALSE, glm.value_ptr(view))

	# Configurar modelo
	model = glm.mat4(1.0)
	glUniformMatrix4fv(glGetUniformLocation(programa, "model"), 1, GL_FALSE, glm.value_ptr(model))

	# Configurar luces y material
	glUniform3f(glGetUniformLocation(programa, "lightPos"), 2.0, 2.0, 2.0)
	glUniform3f(glGetUniformLocation(programa, "viewPos"), 0.0, 0.0, 5.0)
	glUniform3f(glGetUniformLocation(programa, "lightColor"), 1.0, 1.0, 1.0) # Luz blanca

	# Parámetros del material (prueba diferentes combinaciones)
	glUniform3f(glGetUniformLocation(programa, "objectColor"), 0.7, 0.2, 0.2)  # Rojo
	glUniform1f(glGetUniformLocation(programa, "roughness"), 0.2)             # Material más pulido
	glUniform1f(glGetUniformLocation(programa, "metallic"), 0.0)              # Dieléctrico (no metal)

	# Bucle principal
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

		# Rotar la esfera
		tiempo = pygame.time.get_ticks() / 1000.0
		model = glm.rotate(glm.mat4(1.0), tiempo, glm.vec3(0.0, 1.0, 0.0))
		glUniformMatrix4fv(glGetUniformLocation(programa, "model"), 1, GL_FALSE, glm.value_ptr(model))

		# Dibujar
		glBindVertexArray(vao)
		glDrawElements(GL_TRIANGLES, num_indices, GL_UNSIGNED_INT, None)

		pygame.display.flip()
		clock.tick(60)

	# Limpieza
	glDeleteVertexArrays(1, [vao])
	glDeleteBuffers(1, [vbo_vertices])
	glDeleteBuffers(1, [vbo_normales])
	glDeleteBuffers(1, [ebo])
	glDeleteProgram(programa)
	pygame.quit()

if __name__ == "__main__":
	main()