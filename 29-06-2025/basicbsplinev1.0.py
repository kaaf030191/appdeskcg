import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import BSpline
from mpl_toolkits.mplot3d import Axes3D

# -------------------------
# PARÁMETROS BÁSICOS
# -------------------------
# Número de puntos de control
m, n = 4, 4  # control points in u and v direction

# Crear malla de puntos de control (4x4)
control_points = np.array([[[i, j, np.sin(i) * np.cos(j)] for j in range(n)] for i in range(m)])
control_points = np.array(control_points)

# -------------------------
# NODOS Y GRADO DE SPLINE
# -------------------------
k = 3  # grado (cúbico)
# Nodos uniformes abiertos para u y v
kv_u = np.concatenate(([0]*(k+1), np.linspace(0,1,m-k), [1]*(k+1)))
kv_v = np.concatenate(([0]*(k+1), np.linspace(0,1,n-k), [1]*(k+1)))

# Parámetros u y v
num = 30  # densidad
u_vals = np.linspace(0, 1, num)
v_vals = np.linspace(0, 1, num)

# -------------------------
# GENERACIÓN DE LA SUPERFICIE
# -------------------------
surface = np.zeros((num, num, 3))

for i, u in enumerate(u_vals):
	for j, v in enumerate(v_vals):
		point = np.zeros(3)
		for a in range(m):
			for b in range(n):
				# Base functions
				bu = BSpline.basis_element(kv_u[a:a+k+2])(u)
				bv = BSpline.basis_element(kv_v[b:b+k+2])(v)
				point += control_points[a][b] * bu * bv
		surface[i][j] = point

# -------------------------
# VISUALIZACIÓN EN 3D
# -------------------------
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Dibujar superficie
X = surface[:, :, 0]
Y = surface[:, :, 1]
Z = surface[:, :, 2]
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, alpha=0.7, cmap='viridis', edgecolor='k')

# Dibujar malla de control
for i in range(m):
	ax.plot(control_points[i,:,0], control_points[i,:,1], control_points[i,:,2], 'ro-')
for j in range(n):
	ax.plot(control_points[:,j,0], control_points[:,j,1], control_points[:,j,2], 'ro-')

# Configuración del gráfico
ax.set_title("Superficie B-spline con malla de control")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
plt.tight_layout()
plt.show()