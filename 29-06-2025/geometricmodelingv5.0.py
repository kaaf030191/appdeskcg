import numpy as np
import matplotlib.pyplot as plt

# Vértices del cubo centrado en el origen, lado 2
vertices = np.array([
	[-1, -1, -1],  # 0
	[ 1, -1, -1],  # 1
	[ 1,  1, -1],  # 2
	[-1,  1, -1],  # 3
	[-1, -1,  1],  # 4
	[ 1, -1,  1],  # 5
	[ 1,  1,  1],  # 6
	[-1,  1,  1],  # 7
])

# Aristas del cubo
aristas = [
	(0,1), (1,2), (2,3), (3,0),  # base inferior
	(4,5), (5,6), (6,7), (7,4),  # base superior
	(0,4), (1,5), (2,6), (3,7)   # aristas verticales
]

# Definir puntos de control: P0 y P3 son vértices opuestos del cubo
P0 = vertices[0]  # vértice (-1, -1, -1)
P3 = vertices[6]  # vértice (1, 1, 1)

# P1 y P2 son puntos de control internos que definen la forma de la curva
P1 = np.array([-1, 1, 0])   # cerca del vértice 3
P2 = np.array([1, -1, 0])   # cerca del vértice 5

def bezier_cubic(t, P0, P1, P2, P3):
	return (1 - t)**3 * P0 + 3 * (1 - t)**2 * t * P1 + 3 * (1 - t) * t**2 * P2 + t**3 * P3

t_values = np.linspace(0, 1, 200)
curve_points = np.array([bezier_cubic(t, P0, P1, P2, P3) for t in t_values])

fig = plt.figure(figsize=(10,8))
ax = fig.add_subplot(111, projection='3d')

# Dibujar aristas del cubo
for edge in aristas:
	p1 = vertices[edge[0]]
	p2 = vertices[edge[1]]
	ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], color='gray', linewidth=1.5)

# Graficar puntos de control
control_points = np.array([P0, P1, P2, P3])
ax.scatter(control_points[:,0], control_points[:,1], control_points[:,2], color='red', s=80, label='Puntos de control', depthshade=True)

# Conectar puntos de control con líneas punteadas
ax.plot(control_points[:,0], control_points[:,1], control_points[:,2], color='red', linestyle='dashed', linewidth=1)

# Graficar curva Bézier
ax.plot(curve_points[:,0], curve_points[:,1], curve_points[:,2], color='blue', linewidth=2, label='Curva Bézier cúbica')

# Ajustes de la gráfica
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Curva Bézier cúbica saliendo de vértices del cubo')

ax.legend()
ax.grid(True)

# Limitar ejes para que coincidan con el cubo
ax.set_xlim([-1.1, 1.1])
ax.set_ylim([-1.1, 1.1])
ax.set_zlim([-1.1, 1.1])

# Vista inicial para buena perspectiva
ax.view_init(elev=30, azim=45)

plt.show()