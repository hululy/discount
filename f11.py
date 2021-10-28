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
id_data['type'][(id_data['min']<11)&(id_data['max']>11)] = 'A'   # 一直在售
id_data['type'][(id_data['min']<11)&(id_data['max']==11)] = 'B'   # 双十一后停止销售
id_data['type'][(id_data['min']==11)&(id_data['max']>11)] = 'C'   # 双十一当天开始销售
id_data['type'][(id_data['min']==11)&(id_data['max']==11)] = 'D'   # 仅双十一当天销售
id_data['type'][id_data['双十一当天是否售卖']==False] = 'F'   # 仅双十一当天不销售
id_data['type'][id_data['max']<11]= 'E'   # 双十一前停止销售
id_data['type'][id_data['min']>11] = 'G'   # 双十一后开始销售

# 计算不同销售类别的商品数量
result1 = id_data['type'].value_counts()
result1 = result1.loc[['A','B','C','D','E','F','G']]
#print(result1)

# 各类别占比图
from bokeh.palettes import brewer
colori = brewer['YlGn'][7]
plt.axis('equal')
plt.pie(result1,labels=result1.index,autopct='%.2f%%',colors=colori,
        startangle=90,radius=1.5,counterclock=False)
#plt.show()

'''未参加双十一当天销售的商品去向'''
id_not11 = id_data[id_data['双十一当天是否售卖'] == False]
df_not11 = id_not11[['id','type']]
data_not11 = pd.merge(df_not11,df,on='id',how='left')   # 找到双十一当天未销售的商品对应的原始数据
id_con1 = id_data['id'][id_data['type']=='F'].values

data_con2 = data_not11[['id','title','date']].groupby(by=['id','title']).count()
title_count = data_con2.reset_index()['id'].value_counts()
id_con2 = title_count[title_count>1].index

data_con3 = data_not11[data_not11['title'].str.contains('预售')]
id_con3 = data_con3['id'].value_counts().index

print('未参与双十一当天销售的商品中：%i个为暂时下架商品，%i个为重新下架商品，%i个为预售商品'
      %(len(id_con1),len(id_con2),len(id_con3)))

'''真正参与双十一活动的商品及品牌情况（真正参与活动的商品 = 双十一当天在售商品 + 预售商品）'''
data_11sale = id_11
id_11sale_final = np.hstack((data_11sale,id_con3))
result2_i = pd.DataFrame({'id':id_11sale_final})   # 真正参与双十一活动的商品

x1 = pd.DataFrame({'id':id_11})
x1_df = pd.merge(x1,df,on='id',how='left')
brand_11sale = x1_df.groupby('店名')['id'].count()   # 不同品牌参与双十一当天销售的商品数量

x2 = pd.DataFrame({'id':id_con3})
x2_df = pd.merge(x2,df,on='id',how='left')
brand_ys = x2_df.groupby('店名')['id'].count()   # 不用品牌参与预售的商品数量

result2_data = pd.DataFrame({'当天参与活动商品数量':brand_11sale,
                            '预售商品数量':brand_ys})
result2_data['总量'] = result2_data['当天参与活动商品数量'] + result2_data['预售商品数量']
result2_data.sort_values(by='总量',ascending=False,inplace=True)

'''堆叠图制作'''
from bokeh.models import HoverTool
from bokeh.core.properties import value

lst_brand = result2_data.index.tolist()
lst_type = result2_data.columns.tolist()[:2]
colors = ['red','green']

result2_data.index.name = 'brand'
result2_data.columns = ['sale_on_11','presell','sum']
source = ColumnDataSource(result2_data)
hover = HoverTool(tooltips=[('品牌','@brand'),
                            ('双十一当天参与活动的商品数量','@sale_on_11'),
                            ('预售商品数量','@presell'),
                            ('真正参与双十一活动的商品总数','@sum')])

output_file('project11_pic1.html')
p = figure(x_range=lst_brand,plot_width=900,plot_height=350,
           title='各个品牌参与双十一活动的情况',
           tools=[hover,'reset,xwheel_zoom,pan,crosshair'])
p.vbar(top='sum',x='brand',source=source,
             width=0.9,
             #color=colors,alpha=0.7,
             #legend=[value(x) for x in lst_type],
             muted_color='black',
             muted_alpha=0.2)
show(p)











