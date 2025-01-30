
# coding: utf-8

# In[2]:


import numpy as np
import pandas as pd
from pandas import DataFrame,Series
import matplotlib.pyplot as plt
#CDNOW_master.txt


# ### 第一部分：数据类型处理
# 数据加载
# 
# 字段含义：
# user_id:用户ID
# order_dt:购买日期
# order_product:购买产品的数量
# order_amount:购买金额
# 
# 观察数据
# 
# -- 查看数据的数据类型
# -- 数据中是否存储在缺失值
# -- 将order_dt转换成时间类型
# -- 查看数据的统计描述
# 
# 计算所有用户购买商品的平均数量
# 
# 计算所有用户购买商品的平均花费
# 
# 在源数据中添加一列表示月份:astype('datetime64[M]')

# In[3]:


#数据的加载
#\s+ 表示N个不同的空格
df = pd.read_csv('C:/Users/liyutong/Desktop/CDNOW_master.txt',header=None,sep='\s+',names=['user_id','order_dt','order_product','order_amount'])
df


# In[4]:


df.info()


# In[5]:


#无空值，处理时间数据
#order_dt       69659 non-null  int64  -时间类型

df['order_dt']=pd.to_datetime(df['order_dt'],format='%Y%m%d')


# In[6]:


df.info()


# In[7]:


df.describe()


# In[8]:


# 基于order_dt取出其中的月份
df['order_dt'].astype('datetime64[M]')


# In[9]:


df['month']=df['order_dt'].astype('datetime64[M]')
df.head()


# ### 第二部分：按月数据分析
# 
# 用户每月花费的总金额
# 
# 绘制曲线图展示
# 
# 所有用户每月的产品购买量
# 
# 所有用户每月的消费总次数
# 
# 统计每月的消费人数

# In[10]:


#用户每月花费的总金额  
df.groupby(by='month')['order_amount'].sum()


# In[11]:


#绘制曲线图展示
df.groupby(by='month')['order_amount'].sum().plot()


# In[12]:


#所有用户每月的产品购买量
df.groupby(by='month')['order_product'].sum().plot()


# In[13]:


#所有用户每月的消费总次数
df.groupby(by='month')['order_product'].count().plot()


# In[14]:


#统计每月的消费人数,nunique()表示统计去重后的个数
df.groupby(by='month')['user_id'].nunique().plot()


# ### 第三部分：用户个体消费数据分析
# 
# 用户消费总金额和消费总次数的统计描述
# 
# 用户消费金额和消费产品数量的散点图
# 
# 各个用户消费总金额的直方分布图(消费金额在1000之内的分布)
# 
# 各个用户消费的总数量的直方分布图(消费商品的数量在100次之内的分布)

# In[15]:


#用户消费总金额和消费总次数的统计描述
df.groupby(by='user_id')['order_amount'].sum()


# In[16]:


#消费总次数
df.groupby(by='user_id')['order_amount'].count()


# In[17]:


#用户消费金额和消费产品数量的散点图
user_amount_sum = df.groupby(by='user_id')['order_amount'].sum()
user_product_sum = df.groupby(by='user_id')['order_product'].sum()
plt.scatter(user_product_sum,user_amount_sum)


# In[18]:


#各个用户消费总金额的直方分布图(消费金额在1000之内的分布)
df.groupby(by='user_id').sum().query('order_amount <= 1000')['order_amount']
df.groupby(by='user_id').sum().query('order_amount <= 1000')['order_amount'].hist()


# In[19]:


#各个用户消费的总数量的直方分布图(消费商品的数量在100次之内的分布)
df.groupby(by='user_id').sum().query('order_product <= 100')['order_product'].hist()


# ### 第四部分：用户消费行为分析
# - 用户第一次消费的月份分布，和人数统计
#     - 绘制线形图
# - 用户最后一次消费的时间分布，和人数统计
#     - 绘制线形图
# - 新老客户的占比
#     - 消费一次为新用户
#     - 消费多次为老用户
#         - 分析出每一个用户的第一个消费和最后一次消费的时间
#             - agg(['func1','func2']):对分组后的结果进行指定聚合
#         - 分析出新老客户的消费比例
# - 用户分层
#     - 分析得出每个用户的总购买量和总消费金额and最近一次消费的时间的表格rfm
#     - RFM模型设计
#         - R表示客户最近一次交易时间的间隔。
#             - /np.timedelta64(1,'D')：去除days
#         - F表示客户购买商品的总数量,F值越大，表示客户交易越频繁，反之则表示客户交易不够活跃。
#         - M表示客户交易的金额。M值越大，表示客户价值越高，反之则表示客户价值越低。
#         - 将R，F，M作用到rfm表中
#     - 根据价值分层，将用户分为：
#         - 重要价值客户
#         - 重要保持客户
#         - 重要挽留客户
#         - 重要发展客户
#         - 一般价值客户
#         - 一般保持客户
#         - 一般挽留客户
#         - 一般发展客户
#             - 使用已有的分层模型即可rfm_func

# In[28]:


# 用户第一次消费的月份分布，和人数统计
#第一次消费的月份，将用户进行分组找到每一个用户消费月份的最小值就是用户第一次消费的月份
df.groupby(by='user_id')['month'].min()


# In[26]:


df.groupby(by='user_id')['month'].min().value_counts()#人数统计
df.groupby(by='user_id')['month'].min().value_counts().plot()


# In[29]:


#用户最后一次消费的时间分布，和人数统计
df.groupby(by='user_id')['month'].max()


# In[30]:


#人数统计
df.groupby(by='user_id')['month'].max().value_counts().plot()

#在前三个月用户的流失率高


# 新老客户的占比
# 
# 消费一次为新用户
# 
# 消费多次为老用户
# 
# 分析出每一个用户的第一个消费和最后一次消费的时间
# 
# agg(['func1','func2']):对分组后的结果进行指定聚合
# 
# 分析出新老客户的消费比例

# In[ ]:


#新老客户的占比


# In[31]:


#根据用户的消费时间判定新老用户
#如果用户第一次消费时间和最后一次消费时间一样，则为新用户，否则是老用户


# In[35]:


new_old_user_df=df.groupby(by='user_id')['order_dt'].agg(['min','max']) #agg对分组后的数据进行指定聚合
new_old_user_df['min']==new_old_user_df['max'] #True 表示新用户，False表示老用户


# In[36]:


#统计新老个数
(new_old_user_df['min']==new_old_user_df['max']).value_counts()


# 用户分层
#     - 分析得出每个用户的总购买量和总消费金额and最近一次消费的时间的表格rfm
#     - RFM模型设计
#         - R表示客户最近一次交易时间的间隔。
#             - /np.timedelta64(1,'D')：去除days
#         - F表示客户购买商品的总数量,F值越大，表示客户交易越频繁，反之则表示客户交易不够活跃。
#         - M表示客户交易的金额。M值越大，表示客户价值越高，反之则表示客户价值越低。
#         - 将R，F，M作用到rfm表中

# In[37]:


rfm =df.pivot_table(index='user_id',aggfunc={'order_product':'sum','order_amount':'sum','order_dt':'max'})


# In[38]:


rfm


# In[44]:


#计算R，最近一次的交易时间间隔
max_dt=df['order_dt'].max()
-(df.groupby(by='user_id')['order_dt'].max()-max_dt)
rfm['R']=-(df.groupby(by='user_id')['order_dt'].max()-max_dt)/np.timedelta64(1,'D')


# In[45]:


rfm


# In[46]:


rfm.drop(labels='order_dt',axis=1,inplace=True)


# In[47]:


rfm.head()


# In[49]:


rfm.columns=['M','F','R']
rfm


# In[56]:


def rfm_func(x):
    #存储存储的是三个字符串形式的0或者1
    level = x.map(lambda x :'1' if x >= 0 else '0')
    label = level.R + level.F + level.M
    d = {
        '111':'重要价值客户',
        '011':'重要保持客户',
        '101':'重要挽留客户',
        '001':'重要发展客户',
        '110':'一般价值客户',
        '010':'一般保持客户',
        '100':'一般挽留客户',
        '000':'一般发展客户'
    }
    result = d[label]
    return result


# In[57]:


#df.apply(func):可以对df中的行或者列进行某种（func）形式的运算
rfm['label'] = rfm.apply(lambda x : x - x.mean()).apply(rfm_func,axis = 1)
rfm.head()


# In[58]:


rfm.head()


# ### 第五部分：用户的生命周期
# - 将用户划分为活跃用户和其他用户
#     - 统计每个用户每个月的消费次数
#     - 统计每个用户每个月是否消费，消费记录为1否则记录为0
#         - 知识点：DataFrame的apply和applymap的区别
#             - applymap:返回df
#             - 将函数做用于DataFrame中的所有元素(elements)
#             - apply:返回Series
#             - apply()将一个函数作用于DataFrame中的每个行或者列
#     - 将用户按照每一个月份分成：
#         - unreg:观望用户（前两月没买，第三个月才第一次买,则用户前两个月为观望用户）
#         - unactive:首月购买后，后序月份没有购买则在没有购买的月份中该用户的为非活跃用户
#         - new:当前月就进行首次购买的用户在当前月为新用户
#         - active:连续月份购买的用户在这些月中为活跃用户
#         - return:购买之后间隔n月再次购买的第一个月份为该月份的回头客

# In[62]:


#统计每个用户每个月的消费次数
user_month_count_df=df.pivot_table(index='user_id',values='order_dt',aggfunc='count',columns='month').fillna(0)
user_month_count_df.head()


# In[64]:


#统计每个用户每个月是否消费，消费记录为1否则记录为0
df_purchase = user_month_count_df.applymap(lambda x:1 if x >= 1 else 0)
df_purchase.head()


# In[65]:


#将df_purchase中的原始数据0和1修改为new，unactive......,返回新的df叫做df_purchase_new
#固定算法
def active_status(data):
    status = []#某个用户每一个月的活跃度
    for i in range(18):
        
        #若本月没有消费
        if data[i] == 0:
            if len(status) > 0:
                if status[i-1] == 'unreg':
                    status.append('unreg')
                else:
                    status.append('unactive')
            else:
                status.append('unreg')
                    
        #若本月消费
        else:
            if len(status) == 0:
                status.append('new')
            else:
                if status[i-1] == 'unactive':
                    status.append('return')
                elif status[i-1] == 'unreg':
                    status.append('new')
                else:
                    status.append('active')
    return status

pivoted_status = df_purchase.apply(active_status,axis = 1) 
pivoted_status.head()


# In[66]:


df_purchase_new = DataFrame(data=pivoted_status.values.tolist(),index=df_purchase.index,columns=df_purchase.columns)
df_purchase_new


# 每月【不同活跃】用户的计数
# 
# purchase_status_ct = df_purchase_new.apply(lambda x : pd.value_counts(x)).fillna(0)
# 
# 转置进行最终结果的查看

# In[67]:


purchase_status_ct = df_purchase_new.apply(lambda x : pd.value_counts(x)).fillna(0)
purchase_status_ct


# In[68]:


purchase_status_ct.T

