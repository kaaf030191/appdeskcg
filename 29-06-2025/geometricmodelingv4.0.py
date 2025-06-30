import numpy as np
import matplotlib.pyplot as plt

# Puntos de control en 3D
P0 = np.array([0, 0, 0])
P1 = np.array([1, 2, 1])
P2 = np.array([3, 3, 0])
P3 = np.array([4, 0, 2])

def bezier_cubic(t, P0, P1, P2, P3):
	return (1 - t)**3 * P0 + 3 * (1 - t)**2 * t * P1 + 3 * (1 - t) * t**2 * P2 + t**3 * P3

t_values = np.linspace(0, 1, 100)
curve_points = np.array([bezier_cubic(t, P0, P1, P2, P3) for t in t_values])

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Graficar curva Bézier
ax.plot(curve_points[:, 0], curve_points[:, 1], curve_points[:, 2], 
		label='Curva Bézier cúbica', color='blue', linewidth=2)

# Graficar puntos de control
control_points = np.array([P0, P1, P2, P3])
ax.scatter(control_points[:, 0], control_points[:, 1], control_points[:, 2], 
		color='red', s=80, label='Puntos de control', depthshade=True)

# Conectar puntos de control con líneas punteadas
ax.plot(control_points[:, 0], control_points[:, 1], control_points[:, 2], 
		color='red', linestyle='dashed', linewidth=1)

# Ajustes de visualización
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Curva Bézier cúbica en 3D mejorada')

ax.legend()
ax.grid(True)

# Mejorar la perspectiva inicial: elevación y azimut
ax.view_init(elev=30, azim=45)

plt.show()