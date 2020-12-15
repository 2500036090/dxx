
# 读取文件
##读取mysql数据库数据
conn = pymysql.connect( #创建数据库连接
                       host = "172.16.1.120", 
                       port = 3310, 
                       user = 'dxxcreditdbuser', 
                       passwd = 'DxxCreditDbUser@0823019',
                       db = 'dataanalysis_dev',  
                       charset="utf8"  
)
cursor = conn.cursor()
sql_query = 'SELECT * FROM 数据指标_二级维度_0909'
df_info = pd.read_sql(sql_query, con=conn) #(128860, 33)
conn.close()


# 可视化
## 相关关系
%matplotlib inline
def corr_of_label(df,label):
    corrmat = df.corr()
    top_corr_features = corrmat.index[abs(corrmat[label])>0.01]
    plt.figure(figsize=(10,10))
    colormap=plt.cm.RdBu
    g = sns.heatmap(df[top_corr_features].corr(),annot=True,cmap=colormap)
corr_of_label(df_new,'label')

#分类变量：计数、分布
sns.countplot(x = 'grade', order = ['B', 'C', 'D', 'A', 'G', 'E', 'F'], data = df)

# 分类变量特征label的关系探究
# 了解贷款等级和违约情况的相关性
sns.set(rc={'figure.figsize':(20,10)})
sns.countplot(x = 'purpose', hue = 'isDefault',hue_order = [0,1],data = df)

#查看连续型变量在不同y值上的分布
fig, ((ax1, ax2)) = plt.subplots(1, 2, figsize=(15, 6))
data_train.loc[data_train['isDefault'] == 1] \
    ['loanAmnt'].apply(np.log) \
    .plot(kind='hist',
          bins=100,
          title='Log Loan Amt - Fraud',
          color='r',
          xlim=(-3, 10),
         ax= ax1)
data_train.loc[data_train['isDefault'] == 0] \
    ['loanAmnt'].apply(np.log) \
    .plot(kind='hist',
          bins=100,
          title='Log Loan Amt - Not Fraud',
          color='b',
          xlim=(-3, 10),
         ax=ax2)

#







#pandas

#类别变量及数值变量
numerical_fea = list(data_train.select_dtypes(exclude=['object']).columns)
category_fea = list(filter(lambda x: x not in numerical_fea,list(data_train.columns)))
#区别数值型变量中的连续性变量和离散型变量
#过滤数值型类别特征
def get_numerical_serial_fea(data,feas):
    numerical_serial_fea = []  #连续性
    numerical_noserial_fea = [] #离散型
    for fea in feas:
        temp = data[fea].nunique()
        if temp <= 10:
            numerical_noserial_fea.append(fea)
            continue
        numerical_serial_fea.append(fea)
    return numerical_serial_fea,numerical_noserial_fea
def plot(data_train):
    ##变量分类
    numerical_fea = list(data_train.select_dtypes(exclude=['object']).columns)
    category_fea = list(filter(lambda x: x not in numerical_fea,list(data_train.columns)))
    numerical_serial_fea,numerical_noserial_fea = get_numerical_serial_fea(data_train,numerical_fea)
    #类别数据可视化
    for i in range(0,len(numerical_noserial_fea),2):
        f, [ax1,ax2] = plt.subplots(1, 2, figsize=(20, 5))
        sns.countplot(x=numerical_noserial_fea[i],  data=data_train,ax=ax1)
        sns.countplot(x=numerical_noserial_fea[i+1],  data=data_train,ax=ax2)
    #数值型变量可视化
    ##注意第一个参数不是0就是1
    for i in range(1,len(numerical_serial_fea),2):
        f, [ax1,ax2] = plt.subplots(1, 2, figsize=(20, 5))
        data_train[numerical_serial_fea[i]].hist(ax=ax1)
        data_train[numerical_serial_fea[i+1]].hist(ax=ax2)。
numerical_serial_fea,numerical_noserial_fea = get_numerical_serial_fea(data_train,numerical_fea)。

#数值型连续型变量可视化
f = pd.melt(data_train, value_vars=numerical_serial_fea)
g = sns.FacetGrid(f, col="variable",  col_wrap=2, sharex=False, sharey=False)
g = g.map(sns.distplot, "value")



# 提取非数值列
s = train.apply(lambda x:x.dtype)
tecols = s[s=='object'].index.tolist()
# 类别特征编码
te = TargetEncoder(cols=tecols)   #对类别变量进行编码
tf = te.fit_transform(train, target)  
df = te.transform(test) 

#分箱
# 通过除法映射到间隔均匀的分箱中，每个分箱的取值范围都是loanAmnt/1000
data['loanAmnt_bin1'] = np.floor_divide(data['loanAmnt'], 1000)
## 通过对数函数映射到指数宽度分箱
data['loanAmnt_bin2'] = np.floor(np.log10(data['loanAmnt']))
#分位数分箱
data['loanAmnt_bin3'] = pd.qcut(data['loanAmnt'], 10, labels=False)

## 举例归一化过程
#伪代码
for fea in [要归一化的特征列表]：
    data[fea] = ((data[fea] - np.min(data[fea])) / (np.max(data[fea]) - np.min(data[fea])))


