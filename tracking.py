"""
script for tracking particles
"""

from __future__ import division, unicode_literals, print_function  # for compatibility with Python 2 and 3

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas import DataFrame, Series  # for convenience
import pylab

import pims
import trackpy as tp

picture_path = "C:\\Users\\FlumeLab9\\Desktop\\zma\\running test\\2\\4"
csv_savingpathing = "C:\\Users\\FlumeLab9\\Desktop\\zma\\running test\\2"

# Optionally, tweak styles.
mpl.rc('figure',  figsize=(10, 6))
mpl.rc('image', cmap='gray')

frames = pims.ImageSequence(picture_path + '/*.jpg', as_grey=True)
print(frames[0])

#plt.imshow(frames[1])
#f = tp.locate(frames[0], 29, minmass=5500, invert=True)

for i in range(int(len(frames)/1)):
    f = tp.locate(frames[i], 47, minmass=6000, invert=True)
    tp.annotate(f, frames[i])
    #plt.figure()  # make a new figure

f = tp.batch(frames[0: 4480], 47, minmass=6000, invert=True);
'''
    tp.batch(frames[A:B], diameter <usually prime number>, minmass <an number describe the difference of the light, invert <track black particles or white particles>)
    frames[the sequence number of beginning picture,the sequence number of ending picture]
'''
t = tp.link_df(f, 30, memory=15)
'''
    link point to trajectory
    f: get from tp.batch
    30: the max displacement of the particle
    memory: the max frames that a particle can disappear
'''
t.to_csv(csv_savingpathing + "\\data.csv")

plt.figure()
tp.plot_traj(t);
print(t)

pylab.show()