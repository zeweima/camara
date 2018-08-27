"""
a script for cropping pictures
"""
from PIL import Image
import glob
import os
path = "C:\\Users\\FlumeLab9\\Desktop\zma\\running test\\2\\1"
filename = glob.glob(path+'\*.jpg')
saving_folder = 'C:\\Users\\FlumeLab9\\Desktop\zma\\running test\\2\\1\\new'
if not os.path.exists(saving_folder):
    os.makedirs(saving_folder)
for file in filename:
    img = Image.open(file)
    #mg.show()
    box1 = (100, 0, 1000, 100)   #(x1, y1, x2, y2)
    img = img.crop(box1)
    #img.show()
    img.save(file.replace(path,saving_folder))