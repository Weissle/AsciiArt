import cv2
import numpy as np
import utils
import time 
from img2img import bgrimg2charimg,bgrimg2charimg_color
import multiprocessing
from moviepy.editor import VideoFileClip
import os
from tqdm import trange

def multiprocess_warp(cvt_func,frame,*cfg_params):
	cfg = utils.Config(*cfg_params)
	return cvt_func(frame,cfg)

# create video without audio
def create_slient_video(input_path,output_path,cvt_func):
	vid = cv2.VideoCapture(input_path)
	h,w = int(vid.get(4)),int(vid.get(3))
	cfg = utils.Config([h,w],[h,w])

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
		frames_output.append(pool.apply_async(multiprocess_warp,args=(cvt_func,frame,[h,w],[h,w],cfg.char_list)))

	vid.release()
	pool.close()

	fourcc = cv2.VideoWriter_fourcc(*'mp4v')
	output_video = cv2.VideoWriter(output_path,fourcc,fps,(w,h))
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

	if args.no_audio:
		create_slient_video(input_path,output_path,cvt_func)
	else:
		sli_vid_path = 'AsciiArt_TEMP_'+str(int(time.time()))+'.mp4'
		create_slient_video(input_path,sli_vid_path,cvt_func)

		ori_vid = VideoFileClip(input_path)
		sli_vid = VideoFileClip(sli_vid_path)
		audio = ori_vid.audio
		dst_vid = sli_vid.set_audio(audio)
		dst_vid.write_videofile(output_path)

		sli_vid.close()
		ori_vid.close()
		dst_vid.close()

		os.remove(sli_vid_path)
if __name__ == '__main__':

	start_time = time.time()
	args = utils.get_args()
	video_convert(args)
	print('Total time cost {0}s'.format(time.time() - start_time))