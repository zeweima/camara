
"""
this is a script that change pictures patten to black and white and crop pictures
the threshold can be changed
"""

from PIL import Image
from PIL import ImageEnhance
import glob
import os

path = "Q:\\test\\1\\cali"
filename = glob.glob(path+'\*.jpg')
saving_folder = 'Q:\\test\\1\\crop&change'
if not os.path.exists(saving_folder):
    os.makedirs(saving_folder)
for file in filename:
    image = Image.open(file)
    image = image.convert('L')
    box1 = (409, 37, 1378, 141)  # (x1, y1, x2, y2)
    image = image.crop(box1)
    threshold = 110
    table = []
    for j in range(256):
        if j < threshold:
            table.append(0)
        else:
            table.append(1)
    image = image.point(table, '1')
    image.save(file.replace(path,saving_folder))