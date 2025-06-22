
from OpenGL.GL import *
import numpy as np
from utils.math3d import compute_normal

class SurfaceMesh:
    def __init__(self):
        self.grid_size = 20
        self.step = 0.5

    def draw(self):
        for x in range(-self.grid_size, self.grid_size):
            for z in range(-self.grid_size, self.grid_size):
                v0 = [x * self.step, np.sin(x * 0.2) * np.cos(z * 0.2), z * self.step]
                v1 = [(x + 1) * self.step, np.sin((x + 1) * 0.2) * np.cos(z * 0.2), z * self.step]
                v2 = [x * self.step, np.sin(x * 0.2) * np.cos((z + 1) * 0.2), (z + 1) * self.step]
                v3 = [(x + 1) * self.step, np.sin((x + 1) * 0.2) * np.cos((z + 1) * 0.2), (z + 1) * self.step]

                glBegin(GL_TRIANGLES)
                glColor3f(0.7, 0.6, 0.8)

                n1 = compute_normal(v0, v1, v2)
                glNormal3fv(n1)
                glVertex3fv(v0)
                glVertex3fv(v1)
                glVertex3fv(v2)

                n2 = compute_normal(v2, v1, v3)
                glNormal3fv(n2)
                glVertex3fv(v2)
                glVertex3fv(v1)
                glVertex3fv(v3)
                glEnd()
