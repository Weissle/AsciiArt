import cv2
import numpy as np
import utils
import time 
from img2img import bgrimg2charimg,bgrimg2charimg_color
import multiprocessing
from moviepy.editor import VideoFileClip,VideoClip
import gc

def multiprocess_warp(cvt_func,frame,args):
	return cvt_func(frame,args)

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

	pool = multiprocessing.Pool(maxtasksperchild=64)
	frames_output = []

	for frame in ori_vid.iter_frames(logger='bar'):
		h,w,_ = frame.shape
		frame = frame[:,:,::-1]
		frames_output.append(pool.apply_async(multiprocess_warp,args=(cvt_func,frame,args)))

	frames_count = len(frames_output)
	def get_frame(t):
		idx = int(frames_count/ori_duration*t)
		if idx >= len(frames_output):
			idx = -1
		ret = np.array(frames_output[idx].get())
		# special case for moviepy
		if idx != 0:
			frames_output[idx] = None
		if idx % 256 == 0:
			gc.collect()
		return ret

	dst_vid = VideoClip(get_frame,duration=ori_duration)

	if not args.no_audio:
		dst_vid.audio = ori_vid.audio

	dst_vid.write_videofile(output_path,fps=ori_vid.fps,threads=multiprocessing.cpu_count())	

	pool.close()
	pool.join()

	ori_vid.close()
	dst_vid.close()

if __name__ == '__main__':

	start_time = time.time()
	args = utils.get_args()
	video_convert(args)
	print('Total time cost {0}s'.format(time.time() - start_time))