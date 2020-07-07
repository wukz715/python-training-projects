#-*- codingLutf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os



#设置plt的风格
plt.style.use("ggplot")

def read_data():
    '''
    从csv文件中读取数据，之后进行数据清理、补全
    :return: 数据清洗后的数据
    '''
    movie = pd.read_csv("docs/tmdb_5000_movies.csv")
    credit = pd.read_csv("docs/tmdb_5000_credits.csv")
    movie_keys = ['genres','keywords','production_companies','spoken_languages']
    credit_keys = ['cast','crew']
    for k in movie_keys:
        get_json_list(movie,k)

    for c in credit_keys:
        get_json_list(credit,c)
    #合并数据
    all_data = pd.merge(movie,credit,left_on='id',right_on='movie_id',how='left')
    #清理合并后重复的数据title
    #title_x重命名title，title_y去除
    all_data.rename(columns={'title_x':'title'},inplace=True)
    all_data.drop('title_y',axis=1,inplace=True)
    #检验是否存在为空数据
    nas = pd.DataFrame(all_data.isnull().sum())
    null_data = nas[nas.sum(axis=1)>0].sort_values(by=[0],ascending=False)
    # print(null_data)
    #输出为：
    '''
    homepage      3091
    tagline        844
    overview         3
    runtime          2
    release_date     1
    '''
    #定位release_ date为空的数据
    # print(all_data.loc[all_data['release_date'].isnull(),'title'])
    #修复release_ date为空的数据，release_date=2014-6-1，数据结果是网上搜索查询后结果
    all_data['release_date'] = all_data['release_date'].fillna('2014-6-1')
    #同理，修复runtime、overview数据
    #runtime,将runtime seriesl列的mean赋值给缺失部分
    # print(all_data.loc[all_data['runtime'].isnull(), 'title'])
    #df.mean()等价于df.mean(0)。把轴向数据求平均，得到每列数据的平均值。
    #df.mean(1)按照另外一个axis的方向来求平均，得到每行数据的平均值。
    all_data['runtime'] = all_data['runtime'].fillna(all_data['runtime'].mean())
    #新增两列数据，展示年份和月份
    all_data['release_year'] = pd.to_datetime(all_data['release_date'],format='%Y-%m-%d').dt.year
    all_data['release_month'] = pd.to_datetime(all_data['release_date'], format='%Y-%m-%d').dt.month
    nas2 = pd.DataFrame(all_data.isnull().sum())
    null_data2 = nas2[nas2.sum(axis=1) > 0].sort_values(by=[0], ascending=False)
    return all_data

def get_movies_genres(all_data):
    # strip移除字符串首尾的字符串，replace是替换,split是间隔
    all_data['genres'] = all_data['genres'].str.strip('[]').str.replace(' ', '').str.replace("'", "")
    # 输出list，没有则输出str
    all_data['genres'] = all_data['genres'].str.split(',')
    # 数据写入list
    genres_data = []
    for i in all_data['genres']:
        genres_data.extend(i)
    return list(set(genres_data))


def get_json_list(table,name):
    # apply 会将json.loads这个方法应用到table[name]中
    table[name] = table[name].apply(json.loads)
    #遍历表格，将改列的数据换成数据中name的对象集组成的列表
    for index,i in zip(table.index,table[name]):
        l = []
        for _ in i:
            l.append(_['name'])
        table.loc[index,name] = str(l)

def get_max_num_of_movies(all_data):
    '''
    获取数量最多前10种电影类型
    :输出数量最多的电影统计图
    '''
    # #strip移除字符串首尾的字符串，replace是替换,split是间隔
    # all_data['genres'] = all_data['genres'].str.strip('[]').str.replace(' ','').str.replace("'","")
    # #输出list，没有则输出str
    # all_data['genres'] = all_data['genres'].str.split(',')
    # #数据写入list
    # genres_data = []
    # for i in all_data['genres']:
    #     genres_data.extend(i)
    # #计数，Series增加一类数据

    #生成电影类型list，如前五：['Action', 'Adventure', 'Fantasy', 'ScienceFiction', 'Adventure']
    genres_data = get_movies_genres(all_data)
    gen_list = pd.Series(genres_data).value_counts()[:10].sort_values(ascending=False)
    gen_data = pd.DataFrame(gen_list)
    #这步将定义一个Total的数据，怎么进行转换的呢？
    gen_data.rename(columns={0:"Total"},inplace=True)
    #绘图
    plt.subplots(figsize=(10,8))
    #柱状图
    sns.barplot(y=gen_data.index,x='Total',data=gen_data,palette='GnBu_d')
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.xlabel('Total',fontsize=12)
    plt.ylabel('Genres',fontsize=12)
    plt.title('Top 10 genres',fontsize=12)
    plt.show()
    plt.savefig('Top_10_genres.jpg')

def relation_movies_genres_vs_time(all_data):
    '''
    统计不同电影类型和时间的关系
    :param all_data:
    :输出 电影类型和时间的关系统计图
    '''

    #获取年份范围
    year_min = all_data['release_year'].min()
    year_max = all_data['release_year'].max()
    #生成年份数据
    gen_years = pd.DataFrame(index=genres_type,columns=range(year_min,year_max+1))
    #设置null的数值改为0
    gen_years.fillna(value=0,inplace=True)
    #创建数组
    int_years_array = np.array(all_data['release_year'])
    #num年
    num=0
    #统计
    for i in all_data['genres']:
        for j in list(i):
            if j :
                gen_years.loc[j,int_years_array[num]]= gen_years.loc[j,int_years_array[num]] + 1
        num += 1
    #筛选数据,此处只是根据2006的数据进行了一个数据的排序，以方便查看
    gen_years = gen_years.sort_values(by=2006,ascending=False)
    #选取后10年，还有前50年的数据
    gen_years = gen_years.iloc[0:10,-49:-1]
    #折线图
    plt.subplots(figsize=(10,8))
    plt.plot(gen_years.T)
    plt.title('Genres VS Years',fontsize=12)
    plt.xticks(range(1969,2020,5))
    #图例
    plt.legend(gen_years.T)
    plt.savefig('relation_movies_genres_vs_time.jpg')
    plt.show()

def get_mean(cn):
    #计算平均值的平均值
    means = []
    for mt in movie_types:
        part_data.groupby(mt, as_index=True)[cn].mean()
    # 获取是该电影类的数据，即mt=1的数据
    mean_l = [m[1] for m in means]
    return mean_l

def get_count(part_data,cn):
    #计算平均值的平均值
    means = []
    for mt in movie_types:
        part_data.groupby(mt, as_index=True)[cn].count()
    # 获取是该电影类的数据，即mt=1的数据
    mean_l = [m[1] for m in means]
    return mean_l

def relation_genres_vs_movies(all_data):
    '''
    获取电影类型和电影本身的关系
    :param all_data: 原始数据
    :输出：关系图
    '''
    #重新获取数据
    part_data = all_data[['title','vote_average','vote_count','release_year','popularity','budget','revenue']].reset_index(drop=True)
    #获取最xxx的电影
    #收入最高的电影：Avatar 《阿凡达》
    part_data.loc[part_data['revenue'] == part_data['revenue'].max()]['title']
    #最受欢迎的电影：Minions 小黄人
    part_data.loc[part_data['popularity'] == part_data['popularity'].max()]['title']
    #评分最高的电影：肖申克的救赎
    part_data.loc[part_data['vote_average'] == part_data['vote_average'].max()]['title']

    # 生成电影类型list，如前五：['Action', 'Adventure', 'Fantasy', 'ScienceFiction', 'Adventure']
    genres_data = get_movies_genres(all_data)
    #一步电影可能有多种类型，创建新类型记录该类型，即是该类型的电影置为1
    movie_types = genres_data
    print("movie_type:",movie_types)
    '''
    movie_types=['Action', 'Adventure', 'Fantasy', 'ScienceFiction'....
    all_data['genres']的数据为
    0       [Action, Adventure, Fantasy, ScienceFiction]
    1                       [Adventure, Fantasy, Action]
    2                         [Action, Adventure, Crime]
    获取第一个Actions时，检验all_data中是否存在这个数据，是是则在这列mt打上1
    '''
    for mt in movie_types:
        part_data['mt'] = 0
        z = 0
        for g in all_data['genres']:
            if mt in list(g):
                part_data.loc[z,mt] = 1
            else:
                part_data.loc[z,mt] = 0
            z += 1
    print("part_data:",part_data)

    #所有电影的平均分的平均分
    #创建数据集
    mean_data = pd.DataFrame(movie_types)
    mean_data.rename(columns={0:'genres'},inplace=True)
    #vote_average:评分，popularity：受欢迎程度，budget：预算，revenue：利润
    for n in ['vote_average','popularity','budget','revenue']:
        means = []
        for mt in movie_types:
            _ = part_data.groupby(mt, as_index=True)[n].mean()
            means.append(_)
        # 获取是该电影类的数据，即mt=1的数据
        mean_l = [h[1] for h in means]
        mean_data['mean_'+n] = mean_l
    #计算数量
    for m in ['vote_count']:
        means_count = []
        for mt2 in movie_types:
            x = part_data.groupby(mt2, as_index=True)[m].mean()
            means_count.append(x)
        # 获取是该电影类的数据，即mt=1的数据
        mean_ls = [m[1] for m in means_count]
        mean_data['vote_count'] = mean_ls
    #处理空数据
    mean_data.replace('','none',inplace=True)
    print("mean_data:",mean_data.head(5))
    #绘图
    f,ax = plt.subplots(figsize=(10,8))
    ax1 = f.add_subplot(111)
    #创建一个子图，具有不可见的x轴和独立的y轴，他们与原始子图（ax1）是相反的
    ax2 =ax1.twinx()
    g1 = sns.factorplot(x='genres',y='mean_vote_average',data=mean_data,ax=ax1,color='red')
    g2 = sns.factorplot(x='genres', y='mean_popularity', data=mean_data, ax=ax2, color='blue')

    ax1.axes.set_ylabel('vote_average')
    ax1.axes.set_ylim(4,7)
    ax1.set_xticklabels(mean_data['genres'],rotation=90)

    ax2.axes.set_ylabel('popularity')
    ax2.axes.set_ylim(0,40)
    plt.savefig('relation_genres_vs_movies.jpg')
    plt.show()


if __name__ == "__main__":
    # read_data()
    # get_movies_genres(read_data())
    # get_max_num_of_movies(read_data())
    # relation_movies_genres_vs_time(read_data())
    relation_genres_vs_movies(read_data())
