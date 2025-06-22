import tkinter as tk
from tkinter import ttk
from OpenGL.GL import *
from OpenGL.GLU import *
import math
from pyopengltk import OpenGLFrame

class OpenGLWindow(OpenGLFrame):
	def __init__(self, master=None, **kwargs):
		super().__init__(master, **kwargs)
		
		self.width = 800
		self.height = 600
		self.current_model = "lambert"
		self.angle_x = 0.0
		self.angle_y = 0.0
		self.pos_x = 0.0
		self.pos_y = 0.0
		self.pos_z = 0.0
		self._initialized = False
		
		self.bind("<Key>", self.keyboard)
		self.bind("<Configure>", self.on_resize)
		self.focus_set()
		
	def initgl(self):
		glEnable(GL_DEPTH_TEST)
		glClearColor(0.1, 0.1, 0.1, 1.0)
		
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluPerspective(45, self.width / self.height, 0.1, 100.0)
		
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		
		self.init_lighting()
		self._initialized = True
		
	def init_lighting(self):
		glEnable(GL_LIGHTING)
		glEnable(GL_LIGHT0)
		glLightfv(GL_LIGHT0, GL_POSITION, [2.0, 2.0, 2.0, 1.0])
		glLightfv(GL_LIGHT0, GL_AMBIENT, [0.1, 0.1, 0.1, 1.0])
		glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
		glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
		self.update_material()
	
	def update_material(self):
		if not self._initialized:
			return
			
		if self.current_model == "lambert":
			glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.0, 0.6, 0.8, 1.0])
			glMaterialfv(GL_FRONT, GL_SPECULAR, [0.0, 0.0, 0.0, 1.0])
			glMaterialf(GL_FRONT, GL_SHININESS, 0.0)
		elif self.current_model == "phong":
			glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.6, 0.2, 0.7, 1.0])
			glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
			glMaterialf(GL_FRONT, GL_SHININESS, 50.0)
		elif self.current_model == "blinn":
			glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.2, 0.7, 0.3, 1.0])
			glMaterialfv(GL_FRONT, GL_SPECULAR, [0.8, 0.8, 0.8, 1.0])
			glMaterialf(GL_FRONT, GL_SHININESS, 100.0)
		elif self.current_model == "cook":
			glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.7, 0.5, 0.3, 1.0])
			glMaterialfv(GL_FRONT, GL_SPECULAR, [0.9, 0.9, 0.9, 1.0])
			glMaterialf(GL_FRONT, GL_SHININESS, 10.0)
		
		self.redraw()
	
	def draw_sphere(self, radius=1.0, slices=20, stacks=20):
		for i in range(stacks):
			lat0 = math.pi * (-0.5 + (i) / stacks)
			lat1 = math.pi * (-0.5 + (i+1) / stacks)
			
			glBegin(GL_QUAD_STRIP)
			for j in range(slices + 1):
				lng = 2 * math.pi * j / slices
				x = math.cos(lng)
				y = math.sin(lat0)
				z = math.sin(lng)
				glNormal3f(x * math.cos(lat0), y, z * math.cos(lat0))
				glVertex3f(x * math.cos(lat0) * radius, y * radius, z * math.cos(lat0) * radius)

				y = math.sin(lat1)
				glNormal3f(x * math.cos(lat1), y, z * math.cos(lat1))
				glVertex3f(x * math.cos(lat1) * radius, y * radius, z * math.cos(lat1) * radius)
			glEnd()
	
	def redraw(self):
		if not self._initialized:
			return
			
		try:
			glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
			glLoadIdentity()
			gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)
			
			glTranslatef(self.pos_x, self.pos_y, self.pos_z)
			glRotatef(self.angle_x, 1, 0, 0)
			glRotatef(self.angle_y, 0, 1, 0)
			
			self.draw_sphere()
			
			self.tkSwapBuffers()
		except Exception as e:
			print(f"Error in redraw: {e}")
	
	def keyboard(self, event):
		key = event.char.lower()
		
		if key == "w":
			self.angle_x += 5
		elif key == "s":
			self.angle_x -= 5
		elif key == "a":
			self.angle_y -= 5
		elif key == "d":
			self.angle_y += 5
		elif key == "i":
			self.pos_z -= 0.1
		elif key == "k":
			self.pos_z += 0.1
		elif key == "j":
			self.pos_x -= 0.1
		elif key == "l":
			self.pos_x += 0.1
		elif key == "u":
			self.pos_y += 0.1
		elif key == "o":
			self.pos_y -= 0.1
		elif key == "r":
			self.angle_x = self.angle_y = 0.0
			self.pos_x = self.pos_y = self.pos_z = 0.0
		
		self.redraw()
	
	def on_resize(self, event):
		if not self._initialized:
			return
			
		self.width = event.width
		self.height = event.height
		
		try:
			glViewport(0, 0, self.width, self.height)
			glMatrixMode(GL_PROJECTION)
			glLoadIdentity()
			gluPerspective(45, self.width / self.height, 0.1, 100.0)
			
			glMatrixMode(GL_MODELVIEW)
			self.redraw()
		except Exception as e:
			print(f"Error in resize: {e}")

def main():
	root = tk.Tk()
	root.title("Renderización con PyOpenGL y Tkinter")
	
	main_frame = ttk.Frame(root)
	main_frame.pack(fill=tk.BOTH, expand=True)
	
	controls_frame = ttk.Frame(main_frame, width=200)
	controls_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
	
	gl_frame = OpenGLWindow(main_frame, width=800, height=600)
	gl_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
	
	ttk.Label(controls_frame, text="Modelos de iluminación", font=("Arial", 12)).pack(pady=10)
	
	selected_model = tk.StringVar(value="lambert")
	
	def update_model():
		gl_frame.current_model = selected_model.get()
		gl_frame.update_material()
		gl_frame.focus_set()  # ← 🔑 Recuperar el foco para que el teclado funcione
	
	models = [
		("Lambert", "lambert"),
		("Phong", "phong"),
		("Blinn-Phong", "blinn"),
		("Cook-Torrance", "cook")
	]
	
	for text, value in models:
		ttk.Radiobutton(
			controls_frame, 
			text=text, 
			variable=selected_model, 
			value=value,
			command=update_model
		).pack(anchor="w", padx=20)
	
	ttk.Label(controls_frame, text="Controles:", font=("Arial", 12)).pack(pady=10)
	ttk.Label(controls_frame, text="Rotación: W/S/A/D").pack(anchor="w", padx=20)
	ttk.Label(controls_frame, text="Movimiento: I/K/J/L/U/O").pack(anchor="w", padx=20)
	ttk.Label(controls_frame, text="Reset: R").pack(anchor="w", padx=20)
	
	root.mainloop()

if __name__ == "__main__":
	main()