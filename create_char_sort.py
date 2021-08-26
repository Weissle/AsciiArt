from PIL import Image, ImageDraw, ImageFont
import pathlib
import numpy
import utils
import argparse

def get_args():
	parser = argparse.ArgumentParser(description="Given the char set ,\
		this script will create a char list which may better than those defined by human.")
	parser.add_argument("char_path",type=str,help="The path to the chars list")
	# parser.add_argument("ttf_path",nargs='?',type=str,help="The path to the ttf file (optional)",default='None')
	return parser.parse_args()

# 使用的字符集合
def get_char_set(path):
	with open(path,'r') as f:
		all_char = str()
		for line in f:
			if line.startswith('#'):
				continue
			line = line.strip()
			all_char += line
	all_char+= ' '
	return set(all_char)

# 生成字符图片
def get_image(c,fnt):
	size_ = fnt.getsize(str(c))
	print(size_)
	img = Image.new("L",size_,color=(255))
	d = ImageDraw.Draw(img)
	d.text((0,0),str(c),font=fnt)
#	 img.save('.tmp/char_'+str(ord(c))+'.jpg')
	return img

# 获取字符的稠密分数，分数越小，留白越少
def get_score(img):
	pix = numpy.array(img)
	return numpy.sum(pix)

def score_cmp_key(tmp):
	return tmp[0]

def main(char_path):
	# pathlib.Path('./.tmp').mkdir(parents=True,exist_ok=True)
	char_list = list(get_char_set(char_path))
	fnt = utils.load_font()

	score = []
	for i in range(len(char_list)):
		c = char_list[i]
		img = get_image(c,fnt)
		score.append([get_score(img),c])
	score.sort(key=score_cmp_key)
	output = [tmp[1] for tmp in score]
	output = ''.join(output)
	f = open('char_sorted.txt','w+')
	f.write(output)
	f.close()

if __name__ == "__main__":
	args = get_args()
	main(args.char_path)