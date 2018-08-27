import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

lena = mpimg.imread('0-3816.jpg')
f = open("pre.txt",'r')
data = f.readlines()
f.close()
f = open('re.txt', 'w')
X = []
Y = []
x = []
y = []
lable = []
k=0
f.write("number\tlenth\tmean_velocity\thoop_height\n")
for i in range(len(data)):
    data[i]= data[i].replace('\n','').split('\t')
    if data[i][0] != '':
        x.append(float(data[i][2]))
        y.append(float(data[i][1]))
    else:
        lable.append(data[i-1][10])
        X.append(x)
        Y.append(y)
        x = []
        y = []
lable.append(data[i-1][10])
X.append(x)
Y.append(y)
f.close()
plt.figure()
for i in range(len(X)):
    plt.plot(X[i], Y[i], linewidth=1, label=lable[i])
plt.legend()
plt.imshow(lena, cmap='Greys_r')
plt.show()
