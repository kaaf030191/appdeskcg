import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import bisplrep, bisplev
from mpl_toolkits.mplot3d import Axes3D

# Definir la malla de control (puntos de control 3D)
n, m = 5, 5  # Número de puntos de control en u y v
u = np.linspace(0, 1, n)
v = np.linspace(0, 1, m)
u_grid, v_grid = np.meshgrid(u, v, indexing='ij')

# Crear una superficie paramétrica simple (ejemplo: una silla de montar)
x = u_grid
y = v_grid
z = np.sin(u_grid * np.pi) * np.cos(v_grid * np.pi)

# Ajustar una superficie B-spline a los puntos de control
tck = bisplrep(u_grid, v_grid, z, s=0)

# Evaluar la B-spline en una malla más fina para visualización
u_fine = np.linspace(0, 1, 50)
v_fine = np.linspace(0, 1, 50)
z_fine = bisplev(u_fine, v_fine, tck)

# Crear la figura 3D
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Graficar la superficie B-spline
u_fine_grid, v_fine_grid = np.meshgrid(u_fine, v_fine, indexing='ij')
ax.plot_surface(u_fine_grid, v_fine_grid, z_fine, alpha=0.7, cmap='viridis')

# Graficar la malla de control
ax.scatter(u_grid, v_grid, z, color='red', s=50, label='Puntos de control')
ax.plot_wireframe(u_grid, v_grid, z, color='red', linewidth=1, alpha=0.5)

# Configuración del gráfico
ax.set_xlabel('u')
ax.set_ylabel('v')
ax.set_zlabel('z')
ax.set_title('Superficie B-spline con Malla de Control')
ax.legend()

plt.tight_layout()
plt.show()