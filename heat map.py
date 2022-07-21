import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#按照utf-8编码读入结果csv文件
#f = pd.read_csv('instance1 st  t0结果对比.csv')
f = pd.read_csv('instance1 st  alpha结果对比.csv')
f.head()

#pivot = f.pivot(index='Step',columns='T0',values='Processing time')
pivot = f.pivot(index='Step',columns='Alpha',values='Processing time')

#绘制热度图
sns.heatmap(pivot,annot= True,fmt= "d",linewidths= 1.6,cmap="RdPu")
#sns.heatmap(pivot,cmap= "RdBu_r")

plt.show()