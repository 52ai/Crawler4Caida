import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

x = np.arange(1, 12)
y = x ** 2 + 4
plt.title("Matplotlib demo")
plt.xlabel("时间(分钟)")
plt.ylabel("金额($)")
plt.plot(x,y)
plt.show()
