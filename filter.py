"""
this script is used to filter the trajectories and get the velocity, impact energy, hoop length, hoop height
input file is the csv file we get from tracking particles
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import scipy.ndimage


saving_folder = 'Q:\\test\\1\\trajectory_filter'
if not os.path.exists(saving_folder):
    os.makedirs(saving_folder)
csvfile = "Q:\\test\\1\\crop&change\\data.csv"
framerate = 160
mass = 1
scale = 35/2.4



df1 = pd.read_csv(csvfile)
df1 = df1.sort_values(by=['particle', 'frame'])
temp = []
for row in df1.iterrows():
  index, data = row
  temp.append(data.tolist())
temp = np.array(temp)
begin = 0
end = 0
f = open(saving_folder+'\\''data.txt', 'a')
f.write(csvfile+'\n')
f.write('particle\tx_1\ty_1\tx_2\ty_2\tx_3\ty_3\tx_4\ty_4\tv_1x\tx_1y\tv_2x\tx_2y\timpact_angle\treflection_angle\timpact_energy\thoop_length\thoop_height\n')
for i in range(len(temp)):
    sequence = temp[begin][10]
    if i+1 == len(temp) or sequence != temp[i+1][10]:
        low_x = []
        low_y = []
        number = []
        impact_x = []
        impact_y = []
        impact_number = []
        end = i
        plt.title(str(int(temp[begin][10])))
        plt.xlim(0, 1000)
        plt.ylim(120, 0)
        filtered = scipy.ndimage.gaussian_filter(temp[begin:end, 1], 2)
        for j in range(2,len(filtered)-2):
            if filtered[j]>=filtered[j-2] and filtered[j]>=filtered[j+2]:
                low_x.append(temp[begin + j][2])
                low_y.append(filtered[j])
                number.append(begin+j)
        for j in range(1, len(number)):
            if number[len(number)-j] == number[len(number)-j-1]+1 and low_y[len(number)-j]>70:
                if temp[number[j - 1]][2]>=500 or temp[number[j - 1]][2]<=500:                       # this order need to be gotten rid of if the glass are changed
                    f.write(str(int(temp[begin][10])) + '\t')
                    f.write(str(temp[number[len(number) - j - 1] - 2][2] / scale) + '\t' +
                            str(filtered[number[len(number) - j - 1] - 2-begin] / scale) + '\t' +
                            str(temp[number[len(number) - j] - 1][2] / scale) + '\t' +
                            str(filtered[number[len(number) - j - 1]-begin] / scale) + '\t' +
                            str(temp[number[len(number) - j]][2] / scale) + '\t' +
                            str(filtered[number[len(number) - j]-begin] / scale) + '\t' +
                            str(temp[number[len(number) - j] + 2][2] / scale) + '\t' +
                            str(filtered[number[len(number) - j]-begin + 2] / scale) + '\t')
                    v_1x = abs(temp[number[len(number) - j - 1] - 2][2] - temp[number[len(number) - j] - 1][2]) / 2 * framerate / scale
                    v_1y = abs(filtered[number[len(number) - j - 1] - 2-begin] - filtered[number[len(number) - j - 1]-begin]) / 2 * framerate / scale
                    v_2x = abs(temp[number[len(number) - j]][2]-temp[number[len(number) - j] + 2][2]) / 2 * framerate / scale
                    v_2y = abs(filtered[number[len(number) - j]-begin] - filtered[number[len(number) - j]-begin + 2]) / 2 * framerate / scale
                    f.write(str(v_1x) + '\t' + str(v_1y) + '\t' + str(v_2x) + '\t' + str(v_2y) + '\t')
                    f.write(str(abs((v_1x*v_1x+v_1y*v_1y)-(v_2x*v_2x+v_2y*v_2y)) / 2 * mass) + '\t')
                    f.write(str(np.degrees(np.arctan(v_1y/v_1x))) + '\t' + str(np.degrees(np.arctan(v_2y/v_2x))) + '\t')
                    impact_x.append(temp[number[len(number) - j] - 1][2] / 2 + temp[number[len(number) - j]][2] / 2)
                    impact_y.append(filtered[number[len(number) - j - 1]-begin] / 2 + filtered[number[len(number) - j]-begin] / 2)
                    impact_number.append(number[len(number) - j])
                    if len(impact_number)>1:
                        f.write(str(abs(impact_x[-1]-impact_x[-2]))+'\t')
                        low = 10000
                        for k in range(impact_number[-1],impact_number[-2]):
                            if filtered[k - begin]<low:
                                low = filtered[k - begin]
                        f.write(str(abs(impact_y[-1]-low)) + '\n')
                    else:
                        f.write('-1\t-1\n')

        plt.scatter(temp[begin:end, 2],scipy.ndimage.gaussian_filter(temp[begin:end, 1], 2))
        plt.scatter(low_x, low_y, color='r')
        plt.savefig(saving_folder + '\\' + str(int(temp[begin][10])) + '.jpg', dpi=300)
        print(end-begin, temp[begin][10])
        plt.clf()
        plt.close()
        begin = end + 1
f.close()