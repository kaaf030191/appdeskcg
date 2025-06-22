import pygame
from pygame.locals import *
from OpenGL.GL import *
import numpy as np
import glm
import math

# === SHADERS ===
def compilar_shader(codigo, tipo):
	shader = glCreateShader(tipo)
	glShaderSource(shader, codigo)
	glCompileShader(shader)
	if not glGetShaderiv(shader, GL_COMPILE_STATUS):
		raise RuntimeError(glGetShaderInfoLog(shader).decode())
	return shader

def crear_shader_program():
	vs = """
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
		gl_Position = projection * view * vec4(FragPos, 1.0);
	}
	"""

	fs = """
	#version 330 core
	in vec3 FragPos;
	in vec3 Normal;

	out vec4 FragColor;

	uniform vec3 lightPos;
	uniform vec3 viewPos;
	uniform vec3 lightColor;
	uniform vec3 albedo;
	uniform float metallic;
	uniform float roughness;
	uniform float ao;

	const float PI = 3.14159265359;

	float DistributionGGX(vec3 N, vec3 H, float roughness) {
		float a = roughness * roughness;
		float a2 = a * a;
		float NdotH = max(dot(N, H), 0.0);
		float NdotH2 = NdotH * NdotH;

		float num = a2;
		float denom = (NdotH2 * (a2 - 1.0) + 1.0);
		denom = PI * denom * denom;

		return num / max(denom, 0.001);
	}

	float GeometrySchlickGGX(float NdotV, float roughness) {
		float r = roughness + 1.0;
		float k = (r * r) / 8.0;

		float num = NdotV;
		float denom = NdotV * (1.0 - k) + k;

		return num / denom;
	}

	float GeometrySmith(vec3 N, vec3 V, vec3 L, float roughness) {
		float ggx1 = GeometrySchlickGGX(max(dot(N, V), 0.0), roughness);
		float ggx2 = GeometrySchlickGGX(max(dot(N, L), 0.0), roughness);
		return ggx1 * ggx2;
	}

	vec3 fresnelSchlick(float cosTheta, vec3 F0) {
		return F0 + (1.0 - F0) * pow(1.0 - cosTheta, 5.0);
	}

	void main() {
		vec3 N = normalize(Normal);
		vec3 V = normalize(viewPos - FragPos);
		vec3 L = normalize(lightPos - FragPos);
		vec3 H = normalize(V + L);

		float distance = length(lightPos - FragPos);
		float attenuation = 1.0 / (distance * distance);
		vec3 radiance = lightColor * attenuation;

		vec3 F0 = vec3(0.04);
		F0 = mix(F0, albedo, metallic);

		float NDF = DistributionGGX(N, H, roughness);
		float G = GeometrySmith(N, V, L, roughness);
		vec3 F = fresnelSchlick(max(dot(H, V), 0.0), F0);

		vec3 numerator = NDF * G * F;
		float denominator = 4.0 * max(dot(N, V), 0.0) * max(dot(N, L), 0.0);
		vec3 specular = numerator / max(denominator, 0.001);

		vec3 kS = F;
		vec3 kD = vec3(1.0) - kS;
		kD *= 1.0 - metallic;

		float NdotL = max(dot(N, L), 0.0);

		vec3 Lo = (kD * albedo / PI + specular) * radiance * NdotL;
		vec3 ambient = vec3(0.03) * albedo * ao;

		vec3 color = ambient + Lo;
		color = color / (color + vec3(1.0));
		color = pow(color, vec3(1.0 / 2.2));

		FragColor = vec4(color, 1.0);
	}
	"""

	vertex = compilar_shader(vs, GL_VERTEX_SHADER)
	fragment = compilar_shader(fs, GL_FRAGMENT_SHADER)
	programa = glCreateProgram()
	glAttachShader(programa, vertex)
	glAttachShader(programa, fragment)
	glLinkProgram(programa)

	if not glGetProgramiv(programa, GL_LINK_STATUS):
		raise RuntimeError(glGetProgramInfoLog(programa).decode())

	glDeleteShader(vertex)
	glDeleteShader(fragment)

	return programa

# === GEOMETRÍA ===
def generar_esfera(radio, sectores, anillos):
	vertices, normales, indices = [], [], []

	for i in range(anillos + 1):
		lat = math.pi * i / anillos
		for j in range(sectores + 1):
			lon = 2 * math.pi * j / sectores
			x = math.sin(lat) * math.cos(lon)
			y = math.cos(lat)
			z = math.sin(lat) * math.sin(lon)
			vertices.append([x * radio, y * radio, z * radio])
			normales.append([x, y, z])

	for i in range(anillos):
		for j in range(sectores):
			first = i * (sectores + 1) + j
			second = first + sectores + 1
			indices.extend([first, second, first + 1, second, second + 1, first + 1])

	return np.array(vertices, dtype=np.float32), np.array(normales, dtype=np.float32), np.array(indices, dtype=np.uint32)

# === PRINCIPAL ===
def main():
	pygame.init()
	display = (1000, 800)
	pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
	pygame.display.set_caption("Iluminación Cook-Torrance")

	glEnable(GL_DEPTH_TEST)

	vertices, normales, indices = generar_esfera(1.0, 64, 64)

	vao = glGenVertexArrays(1)
	glBindVertexArray(vao)

	vbo = glGenBuffers(1)
	glBindBuffer(GL_ARRAY_BUFFER, vbo)
	glBufferData(GL_ARRAY_BUFFER, vertices.nbytes + normales.nbytes, None, GL_STATIC_DRAW)
	glBufferSubData(GL_ARRAY_BUFFER, 0, vertices.nbytes, vertices)
	glBufferSubData(GL_ARRAY_BUFFER, vertices.nbytes, normales.nbytes, normales)

	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
	glEnableVertexAttribArray(0)
	glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(vertices.nbytes))
	glEnableVertexAttribArray(1)

	ebo = glGenBuffers(1)
	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
	glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

	programa = crear_shader_program()
	glUseProgram(programa)

	projection = glm.perspective(glm.radians(45), display[0] / display[1], 0.1, 100.0)
	view = glm.lookAt(glm.vec3(0, 0, 4), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))

	model = glm.mat4(1.0)

	glUniformMatrix4fv(glGetUniformLocation(programa, "projection"), 1, GL_FALSE, glm.value_ptr(projection))
	glUniformMatrix4fv(glGetUniformLocation(programa, "view"), 1, GL_FALSE, glm.value_ptr(view))

	glUniform3f(glGetUniformLocation(programa, "albedo"), 0.9, 0.0, 0.1)
	glUniform1f(glGetUniformLocation(programa, "metallic"), 0.8)
	glUniform1f(glGetUniformLocation(programa, "roughness"), 0.2)
	glUniform1f(glGetUniformLocation(programa, "ao"), 1.0)

	clock = pygame.time.Clock()
	running = True

	while running:
		for e in pygame.event.get():
			if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
				running = False

		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

		# Animar luz girando
		t = pygame.time.get_ticks() / 1000.0
		light_pos = glm.vec3(3 * math.sin(t), 2.0, 3 * math.cos(t))
		glUniform3fv(glGetUniformLocation(programa, "lightPos"), 1, glm.value_ptr(light_pos))
		glUniform3fv(glGetUniformLocation(programa, "viewPos"), 1, glm.value_ptr(glm.vec3(0, 0, 4)))
		glUniform3f(glGetUniformLocation(programa, "lightColor"), 5.0, 5.0, 5.0)

		rot_model = glm.rotate(model, t * 0.5, glm.vec3(0, 1, 0))
		glUniformMatrix4fv(glGetUniformLocation(programa, "model"), 1, GL_FALSE, glm.value_ptr(rot_model))

		glBindVertexArray(vao)
		glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)

		pygame.display.flip()
		clock.tick(60)

	pygame.quit()

if __name__ == "__main__":
	main()