from PIL import Image, ImageDraw, ImageFont
import pathlib
import numpy

# 使用的字符集合
def get_char_set():
    with open('char_origin.txt','r') as f:
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
    img = Image.new("RGB",size_,color=(255,255,255))
    d = ImageDraw.Draw(img)
    d.text((0,0),str(c),font=fnt,fill='#000000')
#     img.save('.tmp/char_'+str(ord(c))+'.jpg')
    return img

# 获取字符的稠密分数，分数越小，留白越少
def get_score(img):
    pix = numpy.array(img)
    height,width,dim = pix.shape
    size = pix.size
    ret = 0
    for row in pix:
        for tmp in row:
#             print(tmp)
            ret += sum(tmp)/(255*3)
    return ret/size

def score_cmp_key(tmp):
    return tmp[0]

def main():
    # pathlib.Path('./.tmp').mkdir(parents=True,exist_ok=True)
    char_list = list(get_char_set())
    score = []
    fnt = ImageFont.load_default()
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
    main()