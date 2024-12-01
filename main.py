from typing import TypeVar

import noise
import tkinter as tk


T = TypeVar('T')


class App(tk.Tk):
	def __init__(self):
		super(App, self).__init__()
		self.title("Map Generator")
		self.minsize(600, 480)

		# components
		self.control_pannel = tk.LabelFrame(self, text="Parameters")
		self.noise_canvas = NoiseCanvas(self)
		self.noise_canvas_xscrollbar = tk.Scrollbar(self, orient="horizontal")
		self.noise_canvas_yscrollbar = tk.Scrollbar(self, orient="vertical")

		# variables
		self.noise_canvas.image = tk.PhotoImage(master=self)
		self.noise_canvas.image_scale = 0.1

		# events
		self.noise_canvas['xscrollcommand'] = self.noise_canvas_xscrollbar.set
		self.noise_canvas['yscrollcommand'] = self.noise_canvas_yscrollbar.set
		self.noise_canvas_xscrollbar["command"] = self.noise_canvas.xview
		self.noise_canvas_yscrollbar["command"] = self.noise_canvas.yview

		self.place_components()

	def place_components(self):
		MARGIN = 20
		CONTROL_WIDTH = 200
		SCROLL_WIDTH = 10

		self.noise_canvas.place(
			x=MARGIN, y=MARGIN,
			relwidth=1.0, relheight=1.0,
			width=-CONTROL_WIDTH, height=-(MARGIN + SCROLL_WIDTH)
		)
		self.noise_canvas_xscrollbar.place(
			x=MARGIN, y=-MARGIN,
			rely=1.0, relwidth=1.0,
			width=-CONTROL_WIDTH, height=SCROLL_WIDTH
		)
		self.control_pannel.place(
			x=-(CONTROL_WIDTH + MARGIN + SCROLL_WIDTH), y=MARGIN,
			relx=1.0
		)


class NoiseCanvas(tk.Canvas):
	def __init__(self, master):
		super(NoiseCanvas, self).__init__(master)
		self.noise_image = tk.PhotoImage(master=self)
		self.noise_scale = 0.1
		self.texture_size = 128, 128
		self.persistence = 0.5
		self.lacunarity = 2.0
		self.octaves = 6
		self.seed = 0

		self.noise_id = self.create_image(0, 0, image=self.noise_image)
		self.draw_noise()

	def draw_noise(self):
		self.noise_image.configure(width=self.texture_size[0], height=self.texture_size[1])

		for x in range(self.texture_size[0]):
			for y in range(self.texture_size[1]):
				noise_value = noise.pnoise2(
					x * self.noise_scale, y * self.noise_scale,
					octaves=self.octaves,
					persistence=self.persistence,
					lacunarity=self.lacunarity,
					repeatx=self.texture_size[0], repeaty=self.texture_size[1],
					base=self.seed
				)
				color = "#" + hex(int((noise_value + 1) / 2 * 256))[2:].rjust(2, '0') * 3
				self.noise_image.put(color, to=(x, y))


def clamp(value, mini, maxi):
	return max(mini, min(maxi, value))


def main():
	App().mainloop()


if __name__ == '__main__':
	main()
