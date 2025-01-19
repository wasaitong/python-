
# coding: utf-8

# # 美国各州人口密度分析

# In[2]:


import numpy as np
import pandas as pd


# In[14]:


#读入文件
#abb -州的全称和简称的对应关系
abb=pd.read_csv('C:/Users/liyutong/Desktop/state-abbrevs.csv')
abb.head()


# In[12]:


# 洲的简称和面积表，包括面积和年龄信息
population=pd.read_csv('C:/Users/liyutong/Desktop/state-population.csv')
population.head()


# In[13]:


# 洲的全称和面积表
areas=pd.read_csv('C:/Users/liyutong/Desktop/state-areas.csv')
areas.head()


# In[15]:


display(abb.head(),population.head(),areas.head())


# ## 合并pop和ann两个表，用abbreviation 和 state/region 两列
# 
# pop放左边，因为pop的数据最完整

# In[27]:


#根据某一列或几列来合并
#默认合并的规则是查找字段名称相同的列(因为这两列名字不一样，所以要用left_on指定)
#合并的列在内容上，要存在一对一，一对多，多对多的关系
#默认用inner合并，但是为了确保保留所有数据，要用外合并

temp=pd.merge(left=population,right=abb,left_on='state/region', right_on='abbreviation',how='outer')


# In[21]:


abb.abbreviation.unique()


# In[22]:


population['state/region'].unique()


# In[24]:


#找到两列的差异值
set(population['state/region'].unique())-set(abb.abbreviation.unique())


# ## 查看存在缺失数的列

# In[28]:


#population     state abbreviation  有空值
temp.isnull().any()


# ## 找到至少包含一个空值的行

# In[30]:


temp.loc[temp.isnull().any(axis=1)]


# In[33]:


#查看是哪一列存在空值
temp.loc[temp.isnull().any(axis=1),'state/region'].unique()


# ## 为找到的这些state/region的state项补上正确的值，从而去掉这一列的所有NAN

# In[34]:


temp.head()


# In[ ]:


#state对应的是全称
#经过分析只有'PR', 'USA'对应的state有空值，所以只需要填写这两组数据
#usa---》》usa
#PR -->>


# In[37]:


#从另一张表中找PR对应的值
set(areas['state'])-set(abb['state'])


# In[43]:


#找到state/region中等于PR的列，将这列对应的state赋值为Puerto Rico
temp.loc[temp['state/region']=='PR','state']='Puerto Rico'


# In[46]:


#查看使得state为空的轴还有哪些
temp.loc[temp['state'].isnull(),'state/region'].unique()


# ## 合并各州面积数据areas,使用左合并

# In[ ]:


#由于USA是全美国的数据，不需要保留，可以删除
#把sate/region=USA的数据删除


# In[47]:


#找到所有的USA index
USA_index=temp.loc[temp['state/region']=='USA'].index


# In[49]:


#删除
pop_abb=temp.drop(labels=USA_index).copy()
pop_abb


# In[50]:


pop_abb.isnull().any()


# In[51]:


pop_abb=pop_abb.drop(labels=['abbreviation'],axis=1)


# ## 继续寻找population中存在缺失数据的列

# In[53]:


# 由于2000之前，并没有统计过PR洲的人口数据，所以删除
pop_abb.loc[pop_abb.population.isnull()]


# In[55]:


#删除人口为空的所有行
pop_abb.dropna(inplace=True)


# In[56]:


pop_abb


# In[57]:


areas


# In[60]:


## pop_abb表和 areas表进行合并,用外合并保证数据的完整
total=pd.merge(left=pop_abb,right=areas,how='outer')


# In[62]:


#查看空值
#查看后没有缺失数据的行，如果有话还需要进一步数据清洗
total.isnull().any()


# ## 找出2010年的全民人口数据，df.query(查询语句)

# In[64]:


pop_2010_total=total.query('year==2010 & ages=="total"')


# In[71]:


con1=total.year==2010
con2=total.ages=='total'

total.loc[con1&con2]


# ## 对查询结果进行处理，以state列作为新的行索引：set_index

# In[74]:


#人口密度=人口总数/面积
total['density']=total['population']/total['area (sq. mi)']


# In[78]:


density_df=total.query('year==2012 &ages=="total"').sort_values('density',ascending=False)
density_df.set_index('state').head()

