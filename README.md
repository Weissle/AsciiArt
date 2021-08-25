# Ascii Art #

## Status ##
&emsp;&emsp;Usable. But the output video is slient.
&emsp;&emsp;可用，但目前视频转换后无声音。

## Why ##
&emsp;&emsp;Existing similar tools are slow. I am planning to use multi-threads to shorten the process.  
&emsp;&emsp;目前已有的工具速度太慢，准备使用多线程提高生成的速度。

## Requirements ##
&emsp;&emsp;This tool need opencv, Pillow and numpy. Just install them by pip.  
&emsp;&emsp;需要opencv,pillow和numpy,通过pip安装之后即可使用。

## How To Use ##
```
-i input file name.
-o output file name.(Optional)
-c Add it if you need color but not grayscale.
```
### For image ###
`python img2img.py -i {image_path} -o {output_path} -c`
### For video ###
`python video2video.py -i {image_path} -o {output_path} -c`

