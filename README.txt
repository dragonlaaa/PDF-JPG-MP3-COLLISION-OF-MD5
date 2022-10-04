针对任意的MP3，JPG以及PDF生成MD5碰撞文件
需要在ubuntu下安装 mutool 工具
产生碰撞：
python2 mp3jpgpdf.py 1.mp3 1.jpg 1.pdf
验证结果：
md5sum collision.*