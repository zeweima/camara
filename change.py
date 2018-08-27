"""
this is a script that change pictures to black and white
the threshold can be changed
"""

from PIL import Image
from PIL import ImageEnhance
import glob
import os
path = "C:\\Users\\FlumeLab9\\Desktop\\zma\\running test\\2\\1"
filename = glob.glob(path+'\*.jpg')
saving_folder = 'C:\\Users\\FlumeLab9\\Desktop\\zma\\running test\\2\\1\\new'
if not os.path.exists(saving_folder):
    os.makedirs(saving_folder)
for file in filename:
    image = Image.open(file)
    image = image.convert('L')
    threshold = 100
    table = []
    for j in range(256):
        if j < threshold:
            table.append(0)
        else:
            table.append(1)
    image = image.point(table, '1')
    image.save(file.replace(path, saving_folder))