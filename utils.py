from PIL import ImageFont,Image,ImageDraw
import numpy as np
import argparse
import pathlib
import math

def get_output_size(input_size,scale):
    a,b = math.ceil(input_size[0]*scale),math.ceil(input_size[1]*scale)
    return [a,b]

# [w,h]
def get_chars_size(input_size,scale,fnt):
    ow,oh = get_output_size(input_size,scale)
    cw,ch = fnt.getsize('A')
    a,b = math.ceil(ow/cw),math.ceil(oh/ch)
    return [a,b]

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

