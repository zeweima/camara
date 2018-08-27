import numpy as np

f = open ('impact.txt', 'r')
data = f.readlines()
f.close()
impact = []
hoop = []
IM = []
for i in range(len(data)):
    data[i] = data[i].replace('\n','')
    if data[i] == '********':
        hoop.append(impact)
        impact = []
        IM.append(hoop)
        hoop = []
    else:
        if data[i] == '#':
            hoop.append(impact)
            impact = []
        else:
            data[i] = data[i].split('\t')
            for j in range(len(data[i])):
                data[i][j] = float(data[i][j])
            impact.append(data[i])
f = open('hoop1.txt','w')
f.write('tra:\tpoint\tv\'_x\tv\'_y\tv_x\tv_y\tdelat_v^2\tlength\tangle1\tangle2\n')
for i in range(len(IM)):
    for j in range(len(IM[i])):
        f.write(str(i)+ '\t' + str(j) + '\t')
        vx = np.abs(IM[i][j][0][0] - IM[i][j][1][0]) / 2 * 5 / 140 / 2 * 250
        vy = np.abs(IM[i][j][0][1] - IM[i][j][1][1]) / 2 * 5 / 140 / 2 * 250
        v2x = np.abs(IM[i][j][2][0] - IM[i][j][3][0]) / 2 * 5 / 140 / 2 * 250
        v2y = np.abs(IM[i][j][2][1] - IM[i][j][3][1]) / 2 * 5 / 140 / 2 * 250
        angle1 = np.degrees(np.arctan(vy/vx))
        angle2 = np.degrees(np.arctan(v2x/v2y))
        if j >= 1:
            length = np.abs((IM[i][j][1][0] + IM[i][j][2][0]) / 2 - (IM[i][j-1][1][0] + IM[i][j-1][2 ][0]) / 2) * 5 / 140
        else:
            length = 0
        delta_v2 = ((v2x**2+v2y**2)-(vx**2 + vy**2)) * 0.5 * 0.008
        f.write(str(vx) + '\t' + str(vy) + '\t' + str(v2x) + '\t' + str(v2y) + '\t' + str(delta_v2) + '\t' + str(
            length) + '\t' + str(angle1) + '\t' + str(angle2) + '\n')