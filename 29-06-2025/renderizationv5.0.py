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


def load_texture(filename):
    img = Image.open(filename)
    img_data = np.array(list(img.convert("RGB").getdata()), np.uint8)
    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.width, img.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    return tex_id


def draw_sphere():
    quadric = gluNewQuadric()
    gluQuadricNormals(quadric, GLU_SMOOTH)
    gluQuadricTexture(quadric, GL_TRUE)
    gluSphere(quadric, 1.0, 100, 100)
    gluDeleteQuadric(quadric)


def bind_texture_for_index(i):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textures[i])


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
    angle += 0.5
    if angle > 360:
        angle -= 360
    glutPostRedisplay()

def set_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)

    light_position = [light_pos[0], light_pos[1], light_pos[2], 1.0]
    light_color = [1.0, 1.0, 1.0, 1.0]
    ambient_color = [0.2, 0.2, 0.2, 1.0]

    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_color)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_color)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambient_color)

def draw_plane():
    glDisable(GL_LIGHTING)
    glColor3f(0.2, 0.2, 0.2)
    glBegin(GL_QUADS)
    for x in range(-10, 10):
        for z in range(-10, 10):
            glVertex3f(x, -1.0, z)
            glVertex3f(x + 1, -1.0, z)
            glVertex3f(x + 1, -1.0, z + 1)
            glVertex3f(x, -1.0, z + 1)
    glEnd()
    glEnable(GL_LIGHTING)

def draw_shadow(x, z):
    glDisable(GL_LIGHTING)
    glColor4f(0.0, 0.0, 0.0, 0.2)
    glPushMatrix()
    glTranslatef(x, -0.99, z)
    glScalef(1.0, 0.01, 1.0)
    glutSolidSphere(1.0, 50, 50)
    glPopMatrix()
    glEnable(GL_LIGHTING)

def draw_text(x, y, text):
    glDisable(GL_LIGHTING)
    glColor3f(1.0, 1.0, 1.0)
    glWindowPos2f(x, y)
    for c in text.encode():
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, c)
    glEnable(GL_LIGHTING)

def lambert_shader():
    normal = np.array([0.0, 0.0, 1.0])
    light_dir = np.array(light_pos) - np.array([0.0, 0.0, 0.0])
    light_dir /= np.linalg.norm(light_dir)
    diff = max(np.dot(normal, light_dir), 0.0)
    color = diff * np.array([1.0, 0.0, 0.0])
    glColor4f(*color, 0.95)

def phong_shader():
    normal = np.array([0.0, 0.0, 1.0])
    light_dir = np.array(light_pos) - np.array([0.0, 0.0, 0.0])
    view_dir = np.array(view_pos) - np.array([0.0, 0.0, 0.0])
    light_dir /= np.linalg.norm(light_dir)
    view_dir /= np.linalg.norm(view_dir)
    reflect_dir = 2 * np.dot(normal, light_dir) * normal - light_dir
    diff = max(np.dot(normal, light_dir), 0.0)
    spec = pow(max(np.dot(view_dir, reflect_dir), 0.0), 32.0)
    color = diff * np.array([0.0, 1.0, 0.0]) + spec * np.array([1.0, 1.0, 1.0])
    glColor4f(*np.clip(color, 0, 1), 0.95)

def cook_torrance_shader():
    N = np.array([0.0, 0.0, 1.0])
    V = np.array(view_pos) - np.array([0.0, 0.0, 0.0])
    L = np.array(light_pos) - np.array([0.0, 0.0, 0.0])
    V /= np.linalg.norm(V)
    L /= np.linalg.norm(L)
    H = (V + L) / np.linalg.norm(V + L)
    roughness = 0.3
    metallic = 0.9
    F0 = 0.04 * (1 - metallic) + metallic
    F = F0 + (1 - F0) * pow(1 - max(np.dot(H, V), 0.0), 5.0)
    k = (roughness + 1) ** 2 / 8
    G1 = np.dot(N, V) / (np.dot(N, V) * (1 - k) + k)
    G2 = np.dot(N, L) / (np.dot(N, L) * (1 - k) + k)
    G = G1 * G2
    alpha = roughness ** 2
    NdotH = max(np.dot(N, H), 0.0)
    denom = (NdotH ** 2) * (alpha ** 2 - 1) + 1
    D = (alpha ** 2) / (math.pi * denom ** 2)
    NdotL = max(np.dot(N, L), 0.0)
    NdotV = max(np.dot(N, V), 0.0)
    specular = (F * G * D) / (4 * NdotV * NdotL + 0.001)
    kd = (1 - F) * (1 - metallic)
    base_color = np.array([1.0, 0.4, 0.2])
    diffuse = kd * base_color / math.pi
    color = (diffuse + specular) * NdotL
    glColor4f(*np.clip(color, 0, 1), 0.95)

# Función display y main permanecen igual

# ...

def display():
    global angle, frame_count, last_time, fps, shader_times
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(*view_pos, 0, 0, 0, 0, 1, 0)
    set_lighting()
    draw_plane()

    positions = [-3.0, 0.0, 3.0]
    shaders = [lambert_shader, phong_shader, cook_torrance_shader]

    for i in range(3):
        draw_shadow(positions[i], 0.0)

    for i in range(3):
        start = time.perf_counter()
        glPushMatrix()
        glTranslatef(positions[i], 0.0, 0.0)
        glRotatef(angle, 0, 1, 0)
        shaders[i]()
        bind_texture_for_index(i)
        draw_sphere()
        unbind_texture()
        glPopMatrix()
        shader_times[i] = time.perf_counter() - start

    draw_text(10, height - 20, f"FPS: {fps:.2f}")
    for i, model in enumerate(models):
        draw_text(10, height - 40 - i * 20, f"{model}: {shader_times[i]*1000:.2f} ms/frame")

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
    glEnable(GL_MULTISAMPLE)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_NORMALIZE)
    glClearColor(0.1, 0.1, 0.1, 1.0)

    last_time = time.time()

    textures[0] = load_texture("piedra.png")
    textures[1] = load_texture("metal.png")
    textures[2] = load_texture("oro.jpg")

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutIdleFunc(idle)

    glutMainLoop()


if __name__ == '__main__':
    main()
