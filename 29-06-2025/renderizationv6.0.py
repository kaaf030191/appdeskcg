# Requiere PyOpenGL, PIL y GLUT instalados
# pip install PyOpenGL PyOpenGL_accelerate Pillow

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL import Image
import numpy as np
import math
import time

# Globals
width, height = 900, 600
angle = 0.0
frame_count = 0
last_time = 0
fps = 0
shader_times = [0.0, 0.0, 0.0]
textures = [0, 0, 0]

# Luz y camara
light_pos = [5.0, 5.0, 5.0]
view_pos = [0.0, 3.0, 12.0]

# Modelos
models = ["Lambertiano", "Phong", "Cook-Torrance"]

# Materiales predefinidos para las esferas
# Los materiales se definen con color base, color especular (si aplica) y shininess/roughness
# Estos serán pasados a las funciones de shader
materials = {
    "Lambertian_Red": {
        "base_color": np.array([0.8, 0.2, 0.2]), # Rojo mate
    },
    "Phong_Green_Plastic": {
        "base_color": np.array([0.2, 0.8, 0.2]), # Verde plástico
        "specular_color": np.array([1.0, 1.0, 1.0]),
        "shininess": 32.0,
    },
    "CookTorrance_Gold": {
        "base_color": np.array([1.0, 0.843, 0.0]), # Color oro (RGB para amarillo oro)
        "roughness": 0.3, # Rugosidad media
        "metallic": 1.0, # Oro es un metal
    }
}


def load_texture(filename):
    try:
        img = Image.open(filename)
        img_data = np.array(list(img.convert("RGB").getdata()), np.uint8)
        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.width, img.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        return tex_id
    except FileNotFoundError:
        print(f"Error: La textura '{filename}' no se encontró. Asegúrate de que esté en la misma carpeta.")
        return 0 # Retorna 0 para indicar que no se pudo cargar la textura


def draw_sphere():
    quadric = gluNewQuadric()
    gluQuadricNormals(quadric, GLU_SMOOTH)
    gluQuadricTexture(quadric, GL_TRUE)
    gluSphere(quadric, 1.0, 100, 100)
    gluDeleteQuadric(quadric)


def bind_texture_for_index(i):
    if textures[i] != 0: # Solo si la textura fue cargada exitosamente
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, textures[i])
    else:
        glDisable(GL_TEXTURE_2D)


def unbind_texture():
    glDisable(GL_TEXTURE_2D)


def reshape(w, h):
    global width, height
    width, height = w, h
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, w / h, 1, 100)
    glMatrixMode(GL_MODELVIEW)


def idle():
    global angle
    angle += 0.5 # Rotación de las esferas
    
    # Rotación de la luz para observar mejor los brillos
    global light_pos
    light_rotation_speed = 0.05
    light_radius = 5.0
    light_pos[0] = light_radius * math.sin(time.time() * light_rotation_speed)
    light_pos[2] = light_radius * math.cos(time.time() * light_rotation_speed)

    glutPostRedisplay()

def set_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    # Deshabilitamos GL_COLOR_MATERIAL para tener control manual de los materiales en los shaders
    glDisable(GL_COLOR_MATERIAL) 

    light_position = [light_pos[0], light_pos[1], light_pos[2], 1.0] # Posicional
    light_color = [1.0, 1.0, 1.0, 1.0] # Luz blanca
    ambient_color = [0.1, 0.1, 0.1, 1.0] # Luz ambiental muy tenue

    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_color)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_color)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambient_color)

def draw_plane():
    # Para el plano, usamos un color simple sin iluminación compleja.
    # Podríamos aplicar un modelo Lambertiano básico aquí si quisiéramos.
    glDisable(GL_LIGHTING) 
    glColor3f(0.3, 0.3, 0.3) # Un gris más oscuro para el plano
    glBegin(GL_QUADS)
    for x in range(-10, 10):
        for z in range(-10, 10):
            glVertex3f(x, -1.0, z)
            glVertex3f(x + 1, -1.0, z)
            glVertex3f(x + 1, -1.0, z + 1)
            glVertex3f(x, -1.0, z + 1)
    glEnd()
    glEnable(GL_LIGHTING) # Volver a habilitar la iluminación para las esferas

def draw_shadow(x, z):
    # La sombra es un disco plano, oscuro y semitransparente.
    glDisable(GL_LIGHTING)
    glColor4f(0.0, 0.0, 0.0, 0.4) # Más opaca para una sombra más visible
    glPushMatrix()
    glTranslatef(x, -0.99, z)
    glRotatef(90, 1, 0, 0) # Orientar el disco para que quede plano
    gluDisk(gluNewQuadric(), 0, 1.0, 50, 1) # Dibujar un disco en lugar de una esfera aplanada
    glPopMatrix()
    glEnable(GL_LIGHTING)

def draw_text(x, y, text):
    glDisable(GL_LIGHTING)
    
    # Dibujar un fondo semitransparente para el texto
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    # Fondo más grande que el texto para un mejor padding
    text_length = len(text) * 9 # Estimación del ancho del texto (cada caracter es ~9px)
    text_height = 20 # Altura de la fuente GLUT_BITMAP_HELVETICA_18
    
    glColor4f(0.0, 0.0, 0.0, 0.5) # Fondo negro semitransparente
    glBegin(GL_QUADS)
    glVertex2f(x - 5, y - 2)
    glVertex2f(x + text_length + 5, y - 2)
    glVertex2f(x + text_length + 5, y + text_height + 2)
    glVertex2f(x - 5, y + text_height + 2)
    glEnd()
    
    glDisable(GL_BLEND)

    # Dibujar el texto
    glColor3f(1.0, 1.0, 1.0) # Texto blanco
    glWindowPos2f(x, y)
    for c in text.encode():
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, c)
    glEnable(GL_LIGHTING)


# --- Funciones de Shaders (Modelos de Iluminación) ---
# Ahora reciben un diccionario de material para mayor flexibilidad

def lambert_shader(material):
    # En OpenGL, podemos usar glMaterialfv para configurar las propiedades del material
    # y dejar que el pipeline fijo de OpenGL maneje la iluminación Lambertiana
    # ya que glColor solo afecta GL_AMBIENT_AND_DIFFUSE cuando GL_COLOR_MATERIAL está habilitado.
    # Como lo deshabilitamos, configuramos directamente el material.
    
    diffuse_color = material["base_color"]
    ambient_color = diffuse_color * 0.1 # Pequeña contribución ambiental basada en el difuso

    glMaterialfv(GL_FRONT, GL_AMBIENT, (*ambient_color, 1.0))
    glMaterialfv(GL_FRONT, GL_DIFFUSE, (*diffuse_color, 1.0))
    glMaterialfv(GL_FRONT, GL_SPECULAR, (0.0, 0.0, 0.0, 1.0)) # Sin especular
    glMaterialf(GL_FRONT, GL_SHININESS, 0.0) # Sin brillo


def phong_shader(material):
    # Similar al Lambertiano, usamos glMaterialfv para configurar los componentes
    # difuso y especular, y shininess.

    diffuse_color = material["base_color"]
    specular_color = material["specular_color"]
    shininess = material["shininess"]
    ambient_color = diffuse_color * 0.1

    glMaterialfv(GL_FRONT, GL_AMBIENT, (*ambient_color, 1.0))
    glMaterialfv(GL_FRONT, GL_DIFFUSE, (*diffuse_color, 1.0))
    glMaterialfv(GL_FRONT, GL_SPECULAR, (*specular_color, 1.0))
    glMaterialf(GL_FRONT, GL_SHININESS, shininess)


def cook_torrance_shader(material):
    # El modelo Cook-Torrance es un modelo de PBR y NO es soportado directamente por
    # el pipeline de iluminación fijo de OpenGL. Para implementarlo correctamente,
    # se necesitaría un **shader program GLSL** personalizado.
    #
    # Dado que estamos usando el pipeline fijo de OpenGL (GL.GL_LIGHTING, GL.GL_LIGHT0, etc.),
    # una implementación "directa" de Cook-Torrance es imposible sin GLSL.
    #
    # Para propósitos de este ejercicio y demostrar la apariencia del oro,
    # lo que haremos es:
    # 1. Simular la **apariencia de un metal dorado** usando los parámetros de GL_SPECULAR
    #    y GL_DIFFUSE de la mejor manera posible con el pipeline fijo.
    #    Esto NO será una implementación matemáticamente correcta de Cook-Torrance.
    # 2. **Como alternativa y para fines didácticos, la implementación de abajo
    #    es una recreación del cálculo Cook-Torrance que tenías, pero sus resultados
    #    solo se aplican directamente si tuvieras un sistema de sombreado
    #    pixel-a-pixel implementado con GLSL, no con el pipeline fijo.**
    #
    # Para que el ejemplo visual funcione con oro, configuraremos un material
    # "tipo oro" usando las propiedades estándar de OpenGL.

    # Configuración de material para parecer oro con el pipeline fijo de OpenGL
    # Oro es un metal, su color especular es su color base, y su componente difusa es casi nula.
    gold_ambient = np.array([0.24725, 0.1995, 0.0745, 1.0]) # Valores estándar de oro ambiental
    gold_diffuse = np.array([0.75164, 0.60648, 0.22648, 1.0]) # Valores estándar de oro difuso
    gold_specular = np.array([0.628281, 0.555802, 0.366065, 1.0]) # Valores estándar de oro especular
    gold_shininess = 51.2 # Un valor de shininess típico para oro

    glMaterialfv(GL_FRONT, GL_AMBIENT, gold_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, gold_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, gold_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, gold_shininess)
    
    # *************************************************************************
    # IMPORTANTE: El siguiente bloque de código `cook_torrance_shader`
    # ES LA IMPLEMENTACIÓN DE COOK-TORRANCE QUE TENÍAS.
    # ESTE CÓDIGO SOLO TENDRÍA UN EFECTO VISIBLE SI TUVIERAS UN SHADER GLSL
    # PERSONALIZADO. EN EL CONTEXTO DE PyOpenGL CON EL PIPELINE FIJO,
    # **NO TIENE NINGÚN EFECTO EN EL RENDERING ACTUAL DEL OBJETO**
    # YA QUE ESTAMOS USANDO GL_LIGHTING Y GL_MATERIAL.
    # Lo dejo para referencia de tu lógica original, pero visualmente,
    # la apariencia del oro será controlada por `glMaterialfv` de arriba.
    # *************************************************************************

    """
    # Tu implementación original de Cook-Torrance (solo para referencia y con un fix)
    N = np.array([0.0, 0.0, 1.0]) # Esto es una aproximación, necesitarías la normal real del vértice
    V = np.array(view_pos) - np.array([0.0, 0.0, 0.0]) # Debería ser la posición del vértice
    L = np.array(light_pos) - np.array([0.0, 0.0, 0.0]) # Debería ser la posición del vértice
    
    # Normalizar vectores
    V = V / np.linalg.norm(V)
    L = L / np.linalg.norm(L)
    N = N / np.linalg.norm(N) # Asegurarse que N esté normalizado
    
    H = (V + L)
    if np.linalg.norm(H) > 0: # Evitar división por cero
        H = H / np.linalg.norm(H)
    else:
        H = np.array([0.0, 0.0, 0.0]) # O algún valor seguro
    
    # Material properties from the 'material' dictionary
    base_color = material["base_color"]
    roughness = material["roughness"]
    metallic = material["metallic"]

    # Fresnel term (Schlick's approximation)
    F0 = 0.04 * (1 - metallic) + base_color * metallic # F0 para metales y dieléctricos
    F = F0 + (1 - F0) * pow(1 - max(np.dot(H, V), 0.0), 5.0)

    # Geometry term (Schlick-GGX)
    k = (roughness + 1)**2 / 8.0 # Roughness para la función G
    NdotV = max(np.dot(N, V), 0.0)
    NdotL = max(np.dot(N, L), 0.0)
    G1_V = NdotV / (NdotV * (1.0 - k) + k)
    G1_L = NdotL / (NdotL * (1.0 - k) + k)
    G = G1_V * G1_L

    # Normal Distribution Function (Trowbridge-Reitz GGX)
    alpha = roughness**2
    NdotH = max(np.dot(N, H), 0.0)
    denom_D = (NdotH**2 * (alpha**2 - 1.0) + 1.0)
    D = (alpha**2) / (math.pi * denom_D**2)
    
    # Denominador de la ecuación especular
    denom_specular = 4.0 * NdotV * NdotL + 0.001 # Add a small epsilon to avoid division by zero
    
    specular_brdf = (D * G * F) / denom_specular
    
    # Diffuse term
    kd = (1.0 - F) * (1.0 - metallic)
    diffuse_brdf = kd * base_color / math.pi

    # Final color
    radiance = np.array([1.0, 1.0, 1.0]) # Asumiendo luz blanca unitaria
    color = (diffuse_brdf + specular_brdf) * radiance * NdotL
    
    glColor4f(*np.clip(color, 0, 1), 0.95)
    """

# --- Función Display y Main ---

def display():
    global angle, frame_count, last_time, fps, shader_times
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(*view_pos, 0, 0, 0, 0, 1, 0)
    
    # Configura la iluminación global (posición y color de la luz)
    set_lighting() 
    
    draw_plane()

    positions = [-3.0, 0.0, 3.0] # Posiciones de las esferas
    
    # Shaders y sus materiales correspondientes
    shader_configs = [
        (lambert_shader, materials["Lambertian_Red"]),
        (phong_shader, materials["Phong_Green_Plastic"]),
        (cook_torrance_shader, materials["CookTorrance_Gold"])
    ]

    # Dibujar sombras primero
    for i in range(len(positions)):
        draw_shadow(positions[i], 0.0)

    # Dibujar las esferas
    for i in range(len(positions)):
        start = time.perf_counter() # Iniciar contador de tiempo para el shader

        glPushMatrix()
        glTranslatef(positions[i], 0.0, 0.0)
        glRotatef(angle, 0, 1, 0) # Rotación sobre su propio eje
        
        # Aplicar el shader con el material correspondiente
        shader_func, material_props = shader_configs[i]
        shader_func(material_props)
        
        bind_texture_for_index(i)
        draw_sphere()
        unbind_texture()
        glPopMatrix()
        
        shader_times[i] = time.perf_counter() - start # Registrar tiempo de ejecución del shader

    # Dibujar información de rendimiento y modelos
    draw_text(10, height - 20, f"FPS: {fps:.2f}")
    for i, model in enumerate(models):
        draw_text(10, height - 40 - i * 25, f"{model}: {shader_times[i]*1000:.3f} ms/frame")
    
    # Instrucciones de la luz
    draw_text(10, height - 120, "Luz rotando para observar brillos")


    glutSwapBuffers()

    frame_count += 1
    current_time = time.time()
    if current_time - last_time >= 1.0:
        fps = frame_count / (current_time - last_time)
        frame_count = 0
        last_time = current_time


def main():
    global last_time, textures
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH | GLUT_MULTISAMPLE)
    glutInitWindowSize(width, height)
    glutCreateWindow(b"Comparacion de Modelos de Iluminacion")

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_MULTISAMPLE) # Habilitar antialiasing
    glShadeModel(GL_SMOOTH)
    glEnable(GL_NORMALIZE) # Normaliza las normales automáticamente después de transformaciones
    glClearColor(0.1, 0.1, 0.1, 1.0) # Fondo más oscuro

    last_time = time.time()

    # Cargar texturas (asegúrate de que los archivos existan)
    textures[0] = load_texture("piedra.png")
    textures[1] = load_texture("metal.png")
    textures[2] = load_texture("oro.jpg") # Asegúrate de tener una imagen de oro

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutIdleFunc(idle)

    glutMainLoop()


if __name__ == '__main__':
    main()