from PIL import ImageFont,Image,ImageDraw
import numpy as np
import argparse
import pathlib
import math

class Config():
	# input_size , output_size is [height,width]
	def __init__(self,input_size,output_scale:float,char_list=None):
		self.input_size = input_size
		h,w = input_size
		# self.output_size = [h,w]
		# self.output_size = [int(h*output_scale),int(w*output_scale)]
		self.output_size = [int(h*output_scale),int(w*output_scale)]
		if char_list is None:
			self.char_list = get_char_list('resources/char_sorted.txt')
		else:
			self.char_list = char_list
		fnt = load_font(None)
		self.font = fnt
		char_width,char_height = fnt.getsize('A')
		self.char_width,self.char_height = char_width,char_height
		# self.chars_size = [math.ceil(self.output_size[0]/char_height),math.ceil(self.output_size[1]/char_width)]
		self.chars_size = [int(self.output_size[0]/char_height),int(self.output_size[1]/char_width)]

def get_char_list(path):
	f = open(path,'r')
	l = f.readline()
	f.close()
	return list(l)

def grayimg2chars(img,cfg):
	char_list = cfg.char_list
	ret = []
	idxes = ((img/255) * (len(char_list)-1)).astype(int)
	for row in idxes:
		ret.append(''.join([ char_list[tmp] for tmp in row ]))
	return ret


def load_font(path=None):
	# if path == None or path == 'None':
		return ImageFont.load_default()
	# else :
	# 	return ImageFont.truetype(path) 

def get_args():
	parser = argparse.ArgumentParser(description="Convert image(video) to image(video)")
	parser.add_argument('-i','--input',type=str,help='Input file')
	parser.add_argument('-o','--output',type=str,help='Output file',default='')
	parser.add_argument('-c','--color',dest='need_color',help='Need color or just greyscale?',action='store_true')
	parser.add_argument('-s','--scale',dest='scale',help='The output scale of input size. The higher scale, the bigger output size and the better quality.',default=1.0,type=float)
	parser.add_argument('--no-audio',dest='no_audio',help='Need audio ?',action='store_false',default=False)
	return parser.parse_args()

def output_name_generator(input_path):
	input_name = pathlib.Path(input_path).name
	output_path = 'AsciiArt_' + input_name
	return output_path