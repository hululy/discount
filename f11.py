import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from bokeh.plotting import figure,show,output_file
from bokeh.models import ColumnDataSource

'''导入数据'''
import xlrd
df = pd.read_excel('f11.xlsx',sheet_name=0)
df.fillna(0,inplace=True)
df.index = df['update_time']
df['date'] = df.index.day

'''双十一当天在售商品占比情况'''
# 筛选数据
data1 = df[['id','title','店名','date']]

# 统计不同商品销售开始、结束日期
d1 = data1[['id','date']].groupby(by='id').agg(['min','max'])['date']

# 筛选双十一当天在售商品id
id_11 = data1[data1['date']==11]['id']
d2 = pd.DataFrame({'id':id_11,'双十一当天是否售卖':True})

# 合并数据
id_data = pd.merge(d1,d2,left_index=True,right_on='id',how='left')
id_data.fillna(False,inplace=True)

# 计算双十一当天参与活动的商品占比
m = len(d1)
m_11 = len(id_11)
m_pre = m_11/m

'''商品销售计划分类'''
id_data['type'] = '待分类'
id_data['type'][(id_data['min']<11)&(id_data['max']>11)] = 'A'
id_data['type'][(id_data['min']<11)&(id_data['max']==11)] = 'B'
id_data['type'][(id_data['min']==11)&(id_data['max']>11)] = 'C'
id_data['type'][(id_data['min']==11)&(id_data['max']==11)] = 'D'
id_data['type'][id_data['双十一当天是否售卖']==False] = 'F'
id_data['type'][id_data['max']<11]= 'E'
id_data['type'][id_data['min']>11] = 'G'

# 计算不同销售类别的商品数量
result1 = id_data['type'].value_counts()
result1 = result1.loc[['A','B','C','D','E','F','G']]
print(result1)

from bokeh.palettes import brewer
colori = brewer['YlGn'][7]
plt.axis('equal')
plt.pie(result1,labels=result1.index,autopct='%.2f%%',colors=colori,
        startangle=90,radius=1.5,counterclock=False)
plt.show()









