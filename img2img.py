import cv2
import numpy as np
import utils
from PIL import ImageFont,Image,ImageDraw
import img2txt
import font
def bgrimg2charimg(img,args):
    chars = img2txt.bgrimg2chars(img,args)

    h, w, _ = img.shape
    ret = Image.new("RGB", utils.get_output_size([w,h],args.scale), color=(255, 255, 255))
    d = ImageDraw.Draw(ret)

    txt = '\n'.join(chars)
    d.multiline_text((0, 0), txt, font=font.default_font, fill=(0, 0, 0), spacing=0)
    return ret


def bgrimg2charimg_color(img, args):
    h, w, _ = img.shape
    fnt = font.default_font
    chars_size = utils.get_chars_size([w,h],args.scale,fnt)
    img = cv2.resize(img, chars_size, 0.5, 0.5, cv2.INTER_AREA)
    img2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    chars = img2txt.gray2chars(img2, args)
    ret = Image.new("RGB", tuple(utils.get_output_size([w,h],args.scale)), (255, 255, 255))

    d = ImageDraw.Draw(ret)
    cw,ch = fnt.getsize('A')
    for row in range(chars_size[1]):
        for col in range(chars_size[0]):
            tmp = img[row][col]
            # bgr color to rgb color
            color = tuple(tmp[::-1])
            d.text((col*cw, row*ch), chars[row][col], fill=color, font=fnt)
    return ret

def convert(args):
    input_path = args.input
    output_path = args.output
    img = cv2.imread(input_path)

    if args.need_color:
        img = bgrimg2charimg_color(img, args)
    else:
        img = bgrimg2charimg(img, args)

    if output_path == '':
        output_path = utils.output_name_generator(input_path)
        # img.save(output_path)
    # cv2.imwrite(output_path, np.array(img))
    img.save(output_path)


if __name__ == '__main__':
    args = utils.get_args()
    convert(args)
