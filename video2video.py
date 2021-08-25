import cv2
import numpy as np
import utils
from PIL import ImageFont,Image,ImageDraw
import time 
from subprocess import Popen,PIPE
from img2img import bgrimg2charimg,bgrimg2charimg_color
import multiprocessing

def multiprocess_warp(cvt_func,frame,*cfg_params):
	cfg = utils.Config(*cfg_params)
	return cvt_func(frame,cfg)

def video_convert(input_path,output_path,cvt_func):

	starttime =  time.time()
	vid = cv2.VideoCapture(input_path)
	h,w = int(vid.get(4)),int(vid.get(3))
	cfg = utils.Config([h,w],[h,w])

	fps = vid.get(cv2.CAP_PROP_FPS)
	frame_count = vid.get(cv2.CAP_PROP_FRAME_COUNT)

	print(f'frame_cout = :{frame_count}')
	if output_path == '':
		output_path = utils.output_name_generator(input_path)
	cvt_core_num = max(1,multiprocessing.cpu_count()-1)
	pool = multiprocessing.Pool(processes=cvt_core_num)
	frames_output = []
	while True:
		ret,frame = vid.read()
		if ret == False:
			break
		frames_output.append(pool.apply_async(multiprocess_warp,args=(cvt_func,frame,[h,w],[h,w],cfg.char_list)))
	
	pool.close()

	fourcc = cv2.VideoWriter_fourcc(*'H264')
	output_video = cv2.VideoWriter(output_path,fourcc,fps,(w,h))
	cnt = 0
	for res in frames_output:
		fr = res.get()
		tmp = np.array(fr)
		output_video.write(tmp)
		cnt += 1
		print(f'{cnt}/{frame_count}')

	pool.join()
	vid.release()
	output_video.release()
	print(time.time()-starttime)

if __name__ == '__main__':
	args = utils.get_args()
	need_color = args.need_color
	if need_color:
		cvt_func = bgrimg2charimg_color
	else:
		cvt_func = bgrimg2charimg
	video_convert(args.input,args.output,cvt_func)
