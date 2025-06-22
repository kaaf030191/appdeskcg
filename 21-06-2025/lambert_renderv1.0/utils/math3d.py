
import numpy as np

def compute_normal(v0, v1, v2):
    u = np.subtract(v1, v0)
    v = np.subtract(v2, v0)
    n = np.cross(u, v)
    norm = np.linalg.norm(n)
    if norm == 0:
        return [0, 1, 0]
    return n / norm
