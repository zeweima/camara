
f = open("data1.txt",'r')
data = f.readlines()
f.close()
f = open('re.txt', 'w')
del data[0]
x = []
y = []
k=0
f.write("number\tlenth\tmean_velocity\thoop_height\n")
for i in range(len(data)):
    data[i]= data[i].replace('\n','').split('\t')
    if data[i][0] != '':
        x.append(float(data[i][2]))
        y.append(float(data[i][1]))
    else:
        k = k + 1
        f.write(str(k)+'\t')
        f.write(str((x[0]-x[-1]) * 5 / 140)+'\t')
        f.write(str((x[0]-x[-1])/len(x) * 5 / 140 / 2 * 250)+'\t')
        f.write(str((max(y)-min(y)) * 5 / 140)+'\n')
        x = []
        y = []
f.close()
