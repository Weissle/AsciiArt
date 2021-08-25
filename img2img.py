import cv2
import numpy
import utils
from PIL import ImageFont,Image,ImageDraw
import pathlib

def bgrimg2charimg(img,cfg):
	img = cv2.resize(img,tuple(cfg.chars_size[::-1]),0.5,0.5,cv2.INTER_AREA)
	img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

	chars = utils.grayimg2chars(img,cfg)
	ret = Image.new("L",cfg.output_size[::-1],color=(255))

	d = ImageDraw.Draw(ret)

	txt = '\n'.join(chars)
	d.multiline_text((0,0),txt,font=cfg.font,fill=(0),spacing=0) 
	
	return ret

def bgrimg2charimg_color(img,cfg):
	img = cv2.resize(img,tuple(cfg.chars_size[::-1]),0.5,0.5,cv2.INTER_AREA)
	img2 = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

	chars = utils.grayimg2chars(img2,cfg)
	ret = Image.new("RGB",cfg.output_size[::-1],(255,255,255))

	d = ImageDraw.Draw(ret)
	for row in range(cfg.chars_size[0]):
		for col in range(cfg.chars_size[1]):
			tmp = img[row][col]
			# bgr 2 rgb
			color = tuple(tmp[::-1])
			d.text((col*cfg.char_width,row*cfg.char_height),chars[row][col],fill=color,font=cfg.font) 
	return ret

def convert(input_path,output_path,cvt_func):
	img = cv2.imread(input_path)
	h,w,_ = img.shape
	cfg = utils.Config([h,w],[h,w])

	img = cvt_func(img,cfg);
	if output_path == '':
		output_path = utils.output_name_generator(input_path)
	img.save(output_path)

if __name__ == '__main__':
	args = utils.get_args()
	need_color = args.need_color
	if need_color:
		cvt_func = bgrimg2charimg_color
	else:
		cvt_func = bgrimg2charimg
	convert(args.input,args.output,cvt_func)

