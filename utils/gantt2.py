import matplotlib.pyplot as plt
import numpy as np
ax=plt.gca()
[ax.spines[i].set_visible(False) for i in ["top","right"]]

colors = ['red', 'purple', 'blue', 'yellow', 'green', 'orange', 'brown', 'gold', 'darkgreen', 'darkred', 'pink', 'seagreen', 'deepskyblue','black', 'mediumseagreen', 'peru', 'tan', 'chocolate', 'aqua']
colors = colors * 10
# colors = ['red', 'black', 'darkred', 'purple', 'green', 'blue'] * 4

def gatt(m,t):
    """甘特图
    m机器集
    t时间集
    """
    for j in range(len(m)):#工序j
        i=m[j]-1#机器编号i
        if j==0:
            plt.barh(i,t[j])
            plt.text(np.sum(t[:j+1])/8,i,'J%s\nT%s'%((j+1),t[j]),color="white",size=8)
        else:
            plt.barh(i,t[j],left=(np.sum(t[:j])))
            plt.text(np.sum(t[:j])+t[j]/8,i,'J%s\nT%s'%((j+1),t[j]),color="white",size=8)

records = [['Mechine-0', {'job': 3, 'begin': 0, 'end': 1}, {'job': 4, 'begin': 3, 'end': 4}, {'job': 5, 'begin': 8, 'end': 10}, {'job': 8, 'begin': 11, 'end': 13}, {'job': 1, 'begin': 13, 'end': 15}, {'job': 2, 'begin': 15, 'end': 16}, {'job': 7, 'begin': 20, 'end': 21}, {'job': 5, 'begin': 21, 'end': 22}], ['Mechine-1', {'job': 2, 'begin': 0, 'end': 6}, {'job': 0, 'begin': 6, 'end': 7}, {'job': 3, 'begin': 7, 'end': 13}, {'job': 9, 'begin': 13, 'end': 14}, {'job': 7, 'begin': 14, 'end': 20}, {'job': 3, 'begin': 20, 'end': 21}, {'job': 7, 'begin': 21, 'end': 27}], ['Mechine-2', {'job': 0, 'begin': 0, 'end': 4}, {'job': 5, 'begin': 4, 'end': 8}, {'job': 2, 'begin': 8, 'end': 12}, {'job': 1, 'begin': 12, 'end': 13}, {'job': 3, 'begin': 13, 'end': 14}, {'job': 0, 'begin': 14, 'end': 13}, {'job': 5, 'begin': 13, 'end': 17}, {'job': 4, 'begin': 17, 'end': 16}, {'job': 2, 'begin': 16, 'end': 20}, {'job': 5, 'begin': 20, 'end': 19}, {'job': 8, 'begin': 19, 'end': 23}, {'job': 8, 'begin': 23, 'end': 22}, {'job': 4, 'begin': 22, 'end': 26}, {'job': 1, 'begin': 26, 'end': 25}, {'job': 7, 'begin': 27, 'end': 26}, {'job': 9, 'begin': 26, 'end': 25}, {'job': 5, 'begin': 25, 'end': 24}, {'job': 6, 'begin': 24, 'end': 25}], ['Mechine-3', {'job': 8, 'begin': 8, 'end': 11}, {'job': 6, 'begin': 11, 'end': 13}, {'job': 1, 'begin': 15, 'end': 21}], ['Mechine-4', {'job': 4, 'begin': 0, 'end': 3}, {'job': 8, 'begin': 3, 'end': 8}, {'job': 2, 'begin': 20, 'end': 25}], ['Mechine-5', {'job': 8, 'begin': 0, 'end': 1}, {'job': 9, 'begin': 1, 'end': 3}, {'job': 9, 'begin': 3, 'end': 9}, {'job': 1, 'begin': 9, 'end': 8}, {'job': 7, 'begin': 8, 'end': 10}, {'job': 6, 'begin': 10, 'end': 11}, {'job': 0, 'begin': 11, 'end': 13}, {'job': 9, 'begin': 14, 'end': 15}, {'job': 6, 'begin': 15, 'end': 21}, {'job': 4, 'begin': 21, 'end': 20}, {'job': 6, 'begin': 21, 'end': 20}, {'job': 9, 'begin': 20, 'end': 19}, {'job': 4, 'begin': 20, 'end': 19}, {'job': 0, 'begin': 19, 'end': 18}, {'job': 0, 'begin': 18, 'end': 24}, {'job': 3, 'begin': 24, 'end': 26}]]

zldsg = [0] * 20
# for r in records:
#     zldsg += len(r)-1
print(zldsg)

n = 0
for i in range(len(records)):
    for r in records[i][1:]:
        n += 1
        plt.barh(i, r['end']-r['begin'], left = r['begin'], color = colors[r['job']])
        # plt.text(r['begin'], i, str(n), color="black",size=8)

plt.savefig("整整70个job.png", dpi=800)
plt.show()
