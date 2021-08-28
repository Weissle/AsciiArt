import cv2
import numpy as np
import utils
import os
import font
import math

def gray2chars(img,args):
    char_list = font.chars_list
    ret = []
    idxes = ((img/255) * (len(char_list)-1)).astype(int)
    for row in idxes:
        ret.append(''.join([ char_list[tmp] for tmp in row ]))
    return ret

def bgrimg2chars(img,args):
    h,w,_ = img.shape
    chars_size = tuple(utils.get_chars_size([w,h],args.scale,font.default_font))
    img = cv2.resize(img,chars_size,0.5,0.5,cv2.INTER_AREA)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    return gray2chars(img,args)

def convert(args):

    input_path = args.input
    output_path = args.output

    img = cv2.imread(input_path)

    chars = bgrimg2chars(img,args)

    f = open(output_path,'w+')
    f.write('\n'.join(chars))