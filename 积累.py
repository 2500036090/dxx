
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
