
# coding: utf-8

# # 美国2012年总统候选人政治献金数据分析

# In[41]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ## 读取数据

# In[ ]:


pd.read.csv('C:/Users/liyutong/Desktop/美国政治献金/contb_01.csv')
pd.read.csv('C:/Users/liyutong/Desktop/美国政治献金/contb_02.csv')
pd.read.csv('C:/Users/liyutong/Desktop/美国政治献金/contb_03.csv')


# In[2]:


import os


# In[3]:


root='C:/Users/liyutong/Desktop/美国政治献金/'


# In[11]:


party_df=""
contdf_list=[]
for fname in os.listdir(root):
    fpath=os.path.join(root,fname)
    if fname.endswith('.csv'):
        contdf_list.append(pd.read_csv(fpath))
    elif fname.endswith('.xlsx'):
        party_df=pd.read_excel(fpath,index_col=0)
    else:
        print('其他文件不读取')


# In[23]:


# 拼接
contb=pd.concat(contdf_list,ignore_index=True)
contb.head()


# In[24]:


contb.info()


# In[25]:


party_df.info()


# In[26]:


party_df.head()


# ## 看哪些候选人更受欢迎，哪些党派更受欢迎

# 合并表，可以使用merge（）

# In[ ]:


# 观察contb表中没有候选人所在的党派信息，需要将党派信息匹配到contb表中


# In[29]:


contb_party=pd.merge(left=contb,right=party_df,left_on='cand_nm',right_on='names',how='outer')


# In[31]:


contb_party.head(1)


# 使用pd.unique()函数查看colums:查看某一列有哪些元素

# In[32]:


#查看有多少个党派参与了竞选
#可以看到有四个党派参与了竞选，分别是'Republican', 'Democrat', 'Reform', 'Libertarian'
contb_party.party.unique()


# 使用value_counts()函数，统计party列中各个元素出现的次数

# In[43]:


#查看党派的支持度，可以查看支持的次数，可以查看支持的钱数（两个维度）
#contb中，每一行是一次计数，可以直接对party列进行计数
#查看支持的次数
contb_party.party.value_counts()


# In[45]:


contb_party.party.value_counts().plot(kind='bar')


# In[40]:


#查看支持的钱数,根据党派分组，求和
contb_party.groupby('party')['contb_receipt_amt'].sum()


# In[46]:


contb_party.groupby('party')['contb_receipt_amt'].sum().plot(kind='bar')


# In[49]:


# contb_receipt_dt 
#pandas 的日期格式是可以运算的
contb_party.info()


# In[ ]:


# contb_receipt_dt 目前是object 


# In[50]:


import datetime


# In[51]:


datetime.datetime(2022,2,11)


# In[53]:


# pandas的to_datetime函数，可以批量转换符合时间格式的字符串为时间类型
pd.to_datetime('2022-02-11')


# In[55]:


#备注：20-JUN-11 是一个标准的欧式时间格式，日-月-年，只要是标准的时间格式字符串
#都可以用pd.to_datetime进行批量转换
#假设20-JUN-11 是不符合标准时间格式的，因为业务表的记录过程中，难免会出现一些人为的错误操作

contb_party.contb_receipt_dt


# 查看日期格式，并将其转换为pandas的日期格式，通过函数加map方式进行转换

# In[ ]:


Sereis.map(function)


# In[68]:


months_dict={'JAN':1,'FEB':2,'MAR':3,'APR':4,'MAY':5,'JUN':6,'JUL':7,'AUG':8,
        'SEP':9,'OCT':10,'NOV':11,'DEC':12}


# In[69]:


#20-JUN-11---2011-6-11
#因为mon 是英文不是数字
def transform_date_string(x):
    #判断接收的X是否为一个字符串对象
    if isinstance(x,str):
        day,mon,year =x.split('-')
        month=months_dict[mon]
        return'20%d-%d-%d'%(int(year),int(month),int(day))
    


# In[70]:


transform_date_string('20-JUN-11')


# In[72]:


date_string=contb_party.contb_receipt_dt.map(transform_date_string)


# 将原数据进行覆盖

# In[74]:


contb_party.contb_receipt_dt=pd.to_datetime(date_string)


# In[76]:


contb_party.sort_values(by='contb_receipt_dt',inplace=True)


# 得到转换后的数据，可以计算每一天各政党政治献金数目

# In[78]:


contb_party.head()


# In[80]:


#先按天分组，再按政党分组
group_df=contb_party.groupby(by=['contb_receipt_dt','party'])['contb_receipt_amt'].sum()


# ##  一般涉及到两个以上分组情况，转成透视表进行查看
# 
# 使用unstack()将上面所得数据中的party从一级索引变成列索引，unstack('party')

# In[87]:


piovt_table=group_df.unstack()
#空值填充成0.0
piovt_table.fillna(value=0.0,inplace=True)


# In[85]:


piovt_table.plot(kind='line')


# 因为上图看不出什么结论，可以计算各个党派累计政治献金，cumsum()累加函数

# In[89]:


piovt_table.cumsum().plot(kind='line')


# 把时间作为列，党派作为行来观察，做一个转置

# In[90]:


piovt_table.T


# 使用stack 把party变成二级行索引，注意所有值都不能为NAN，需要填充为0

# In[91]:


piovt_table.stack()


# 查看候选人姓名cand_nm和政治献金捐赠者职业contbr_occupation，以及捐赠情况，能看出各个候选人主要的支持者分布情况

# In[98]:


# groupby cand_nm 和contbr_occupation 统计 contb_receipt_amt
group_df2=contb_party.groupby(by=['cand_nm','contbr_occupation'])['contb_receipt_amt'].sum()


# In[99]:


group_df2


# 查看老兵主要支持谁：DISABLED VETERAN
# 
# 考察Series索引

# In[107]:


condtion=contb_party.contbr_occupation=='DISABLED VETERAN'

good_man=contb_party.loc[condtion,'cand_nm'].value_counts()


# In[111]:


good_man_df=good_man.reset_index()
good_man_df.columns=['count_num','cand_nm']
good_man_df


# 找出各个候选人的捐赠者中，捐赠金额最大的人的职业以及捐赠额

# In[120]:


#先找最大值
max_amt=contb_party.contb_receipt_amt.max()


# In[121]:


condtion=contb_party.contb_receipt_amt==max_amt


# In[123]:


condtion.sum()


# In[124]:


contb_party.loc[condtion]


# In[ ]:


#使用query()查询


# In[125]:


contb_party.query('contb_receipt_amt==%f'%(max_amt))

