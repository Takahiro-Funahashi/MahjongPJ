from scene import *
from PIL import Image, ImageDraw

import io
import ui

A = Action

class DemoGui(Scene):
	def __init__(self):
		super().__init__()
		self.background_color = "darkgreen"
		import class_Pai as Pai
		self.Pai = Pai.class_Pai()
		self.img_path ='./image/'
		
		self.pai_size = (24, 32)
		
		pai = 'man1.gif'
		
		timg = self._set_image_texture(pai,0)
		pai_node = SpriteNode(timg, position=(120,80))
		pai_node.size = self.pai_size
		self.add_child(pai_node)
		
		return
		
	def _set_image_texture(self, pai, rotate):
		path = self.img_path + pai
		img = Image.open(path)
		img = img.rotate(rotate)
		timg = self._set_texture_img(img)
		return timg

	def _set_texture_img(self, img):
		bfile = io.BytesIO()
		img.save(bfile, format='png')
		bimg = bfile.getvalue()
		uimg = ui.Image.from_data(bimg)
		timg = Texture(uimg)
		return timg
		
	def setup(self):
		return
	def update(self):
		return
	def touch_began(self, touch):
		touch_l = self.point_from_scene(touch.location)
	def touch_moved(self, touch):
		touch_l = self.point_from_scene(touch.location)
	def touch_ended(self, touch):
		touch_l = self.point_from_scene(touch.location)
		
if __name__ == '__main__':
	import os
	print(os.getcwd())
	#run(DemoGui(), PORTRAIT)
