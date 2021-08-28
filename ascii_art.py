import video2video
import img2img
import img2txt
import utils
import os
import time
import pathlib

image_ext = { 'png','jpeg','jpg','bmp' }
video_ext = { 'mp4','flv','mkv','avi','mov' }
txt_ext = {'txt'}

def check_type(ext:str):
	ext = ext.lower()
	if ext in image_ext:
		return 'image'
	elif ext in video_ext:
		return 'video'
	elif ext in txt_ext:
		return 'txt'
	else:
		return 'unknown'


def convert(args):
	if args.output == '':
		args.output = utils.output_name_generator(args.input)
	input_ext = os.path.splitext(args.input)[1]
	output_ext = os.path.splitext(args.output)[1]
	input_type = check_type(input_ext[1:])
	output_type = check_type(output_ext[1:])

	print('Input and output files should be image or video file. ')
	# if input is img , output type could be img or txt
	if input_type == 'image' and output_type == 'txt':
		img2txt.convert(args)	
	elif input_type == 'image' and output_type == 'image':
		img2img.convert(args)
	# if input is video, output type should be video
	elif input_type == 'video' and output_type == 'video':
		video2video.convert(args)
	else:
		print('Input file\'s extension is not corresponding to output\'s ' )
		exit(0)
	
if __name__ == '__main__':

	start_time = time.time()
	args = utils.get_args()
	convert(args)
	print('Total time cost {0}s'.format(time.time() - start_time))
	print('Output file is place at {0}'.format(pathlib.Path(args.output).absolute()))