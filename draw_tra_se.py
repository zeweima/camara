import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

saving_folder = 'Q:\\test\\1\\trajectory'
if not os.path.exists(saving_folder):
    os.makedirs(saving_folder)
df1 = pd.read_csv("Q:\\test\\1\\new\\data.csv")
df1 = df1.sort_values(by=['particle', 'frame'])
temp = []
for row in df1.iterrows():
  index, data = row
  temp.append(data.tolist())
temp = np.array(temp)
begin = 0
end = 0
for i in range(len(temp)):
    sequence = temp[begin][10]
    if i+1 == len(temp) or sequence != temp[i+1][10]:
        end = i
        plt.title(str(int(temp[begin][10])))
        plt.xlim(0, 1000)
        plt.ylim(150, 0)
        plt.gca().set_aspect('equal')
        plt.plot(temp[begin:end, 2], temp[begin:end, 1])
        plt.savefig(saving_folder + '\\' + str(int(temp[begin][10])) + '.jpg', dpi=300)
        print(end-begin, temp[begin][10])
        plt.clf()
        plt.close()
        begin = end + 1