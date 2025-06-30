import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Definir puntos de control P0, P1, P2, P3 en 3D
P0 = np.array([0, 0, 0])
P1 = np.array([1, 2, 1])
P2 = np.array([3, 3, 0])
P3 = np.array([4, 0, 2])

# Función para calcular un punto en la curva Bézier cúbica para un valor t
def bezier_cubic(t, P0, P1, P2, P3):
	return (1 - t)**3 * P0 + 3 * (1 - t)**2 * t * P1 + 3 * (1 - t) * t**2 * P2 + t**3 * P3

# Generar valores de t
t_values = np.linspace(0, 1, 100)

# Calcular puntos de la curva
curve_points = np.array([bezier_cubic(t, P0, P1, P2, P3) for t in t_values])

# Visualización
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Graficar curva Bézier
ax.plot(curve_points[:, 0], curve_points[:, 1], curve_points[:, 2], label='Curva Bézier cúbica', color='blue')

# Graficar puntos de control
control_points = np.array([P0, P1, P2, P3])
ax.scatter(control_points[:, 0], control_points[:, 1], control_points[:, 2], color='red', label='Puntos de control')

# Conectar puntos de control con líneas
ax.plot(control_points[:, 0], control_points[:, 1], control_points[:, 2], color='red', linestyle='dashed')

ax.legend()
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Curva Bézier cúbica en 3D')

plt.show()