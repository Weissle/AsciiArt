import cv2
import numpy as np
import utils
import time 
from img2img import bgrimg2charimg,bgrimg2charimg_color
import multiprocessing
from moviepy.editor import VideoFileClip,VideoClip
import os
from tqdm import trange
import gc
def multiprocess_warp(cvt_func,frame,*cfg_params):
	cfg = utils.Config(*cfg_params)
	return cvt_func(frame,cfg)

# create video without audio
def create_slient_video(input_path,output_path,cvt_func):
	vid = cv2.VideoCapture(input_path)
	h,w = int(vid.get(4)),int(vid.get(3))
	cfg = utils.Config([h,w],args.scale)

	fps = vid.get(cv2.CAP_PROP_FPS)
	frame_count = vid.get(cv2.CAP_PROP_FRAME_COUNT)

	cvt_core_num = max(1,multiprocessing.cpu_count()-1)
	pool = multiprocessing.Pool(processes=cvt_core_num)
	frames_output = []
	print(f'Reading video from {input_path}')
	for _ in trange(int(frame_count)):
		ret,frame = vid.read()
		if ret == False:
			break
		frames_output.append(pool.apply_async(multiprocess_warp,args=(cvt_func,frame,[h,w],args.scale,cfg.char_list)))

	vid.release()
	pool.close()

	# fourcc = cv2.VideoWriter_fourcc(*'mp4v')
	# output_video = cv2.VideoWriter(output_path,fourcc,fps,cfg.output_size[::-1])
	moviepy.video.VideoClip.VideoClip()
	print('Converting')
	for i in trange(len(frames_output)):
		res = frames_output[i]
		fr = res.get()
		tmp = np.array(fr)
		output_video.write(tmp)

	pool.join()
	output_video.release()

# def video_convert(input_path,output_path,cvt_func):
def video_convert(args):

	input_path = args.input
	output_path = args.output
	if args.need_color :
		cvt_func = bgrimg2charimg_color
	else:
		cvt_func = bgrimg2charimg

	if output_path == '':
		output_path = utils.output_name_generator(input_path)

	ori_vid = VideoFileClip(input_path)
	ori_duration = ori_vid.duration
	w,h = ori_vid.size

	pool = multiprocessing.Pool()
	frames_output = []

	char_list = utils.get_char_list()
	frames_output = []
	for frame in ori_vid.iter_frames(logger='bar'):
		h,w,_ = frame.shape
		frames_output.append(pool.apply_async(multiprocess_warp,args=(cvt_func,frame,[h,w],args.scale,char_list)))

	frames_count = len(frames_output)
	cfg = utils.Config([h,w],args.scale,char_list)
	def get_frame(t):
		idx = int(frames_count/ori_duration*t)
		if idx >= len(frames_output):
			idx = -1
		ret = np.array(frames_output[idx].get())
		# special case for moviepy
		if idx != 0:
			frames_output[idx] = None
		gc.collect()
		return ret

	dst_vid = VideoClip(get_frame,duration=ori_duration)

	if not args.no_audio:
		dst_vid.audio = ori_vid.audio

	# dst_vid.write_videofile(output_path,fps=ori_vid.fps,threads=multiprocessing.cpu_count())	
	dst_vid.write_videofile(output_path,fps=ori_vid.fps,threads=2)	

	# pool.close()
	# pool.join()
	ori_vid.close()
	dst_vid.close()

if __name__ == '__main__':

	start_time = time.time()
	args = utils.get_args()
	video_convert(args)
	print('Total time cost {0}s'.format(time.time() - start_time))