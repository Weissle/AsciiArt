import cv2
import numpy
import utils
from PIL import ImageFont,Image,ImageDraw
import img2img
import time 
from subprocess import Popen,PIPE
from img2img import bgrimg2charimg,bgrimg2charimg_color
import multiprocessing

class multiprocess_warp(cvt_func,frame,cfg):
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

	frames = []
	while True:
		ret,frame = vid.read()
		if ret == False:
			break
		frames.append(frame)
	
	frames_output = [None]*len(frames)

	cpu_num = multiprocessing.cpu_count()
	cpu_num = max(1,cpu_num)
	pool = multiprocessing.Pool(processes=cpu_num)
	for i in range(len(frames)):
		# frames_output[i] = pool.apply_async(cvt_func,args=(frames[i],cfg))
		frames_output[i] = pool.apply_async(multiprocess_convert,args=(cvt_func,frames[i],cfg))
		# frames_output = pool.starmap_async(cvt_func,[(fr,cfg) for fr in frames],len(frames))
	
	pool.close()

	output_process = Popen(['ffmpeg.exe','-y','-f','image2pipe','-vcodec','mjpeg','-r',str(fps),'-i','-','-vcodec','libx265','-qscale','5','-r',str(fps),output_path],stdin=PIPE)

	for res in frames_output:
		fr = res.get()
		fr.save(output_process.stdin,format='jpeg')
	pool.join()

	output_process.stdin.close()
	output_process.wait()
	print(time.time()-starttime)

	vid.release()
	cv2.destroyAllWindows()

if __name__ == '__main__':
	args = utils.get_args()
	need_color = args.need_color
	if need_color:
		cvt_func = bgrimg2charimg_color
	else:
		cvt_func = bgrimg2charimg
	video_convert(args.input,args.output,cvt_func)
