#-*- coding:utf-8 -*-
'''
auth:zhong
date:20200703
'''
import os
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib  import pyplot as plt
from matplotlib.font_manager import FontProperties

#数据目录
dirpath = "/Users/walter/python-workplace/testing-project-analyze-data/test/document"
#如果目录不存在，自动创建
if not os.path.exists(dirpath):
    os.mkdir(dirpath,"wb")

# 添加中文支持
font = FontProperties(fname="/Library/Fonts/Songti.ttc", size=12)

#读入两个表格数据
data = pd.read_csv(os.path.join(dirpath,"athlete_events.csv"))
regions = pd.read_csv(os.path.join(dirpath,"noc_regions.csv"))
#合并表格
merged = pd.merge(data,regions,on="NOC",how="left")

#金牌获得者的年龄分布,因为这个是数值统计，纵轴y只能是count数量，横轴x就是我们的age数据了
def gold_medals():
    #过滤金牌数据
    gold_medal = merged[merged.Medal == "Gold"]
    #过滤年龄为null的值，保证数据的年龄有值
    gold_medal = gold_medal[np.isfinite(gold_medal['Age'])]
    #绘制图表,设置画布大小
    plt.figure(figsize=(10,5))
    # 设置紧凑型布局
    plt.tight_layout()
    #执行统计绘图
    sns.countplot(gold_medal['Age'])
    # 设置图表信息
    plt.title("金牌年龄分布", fontproperties=font, fontsize=16)
    #  设置x轴的刻度字体大小
    plt.xticks(fontproperties=font,fontsize=8)
    # 保存图片
    plt.savefig("goldMedals.jpg")
    # 展示结果
    # plt.show()

#女子田径数据分析
def female_athletics():
    #女性+夏季运动会
    women_df = merged[(merged.Sex == 'F') & (merged.Season =='Summer')]
    #x轴为年份，y轴为奖牌数
    sns.set(style='darkgrid')
    plt.figure(figsize=(10,5))
    #统计柱状图
    sns.countplot(x="Year",data=women_df)
    plt.title("每届夏季奥运会女子奖牌",fontproperties=font)
    #  设置x轴的刻度字体大小
    plt.xticks(fontproperties=font, fontsize=8)
    # 保存图片
    # plt.savefig("female_athletics.jpg")
    # 展示结果
    plt.show()
    print(women_df["ID"].loc[ women_df["Year"] == '1900'].count())

#金牌获得者身高和体重的关系
def gold_height_and_weight():
    #金牌获得者，且身高体重皆不为空的数据
    not_null_gold_medals = merged[(merged["Medal"] == "Gold") & (merged['Height'].notnull()) & (merged['Weight'].notnull())]
    #设定绘图大小
    plt.figure(figsize=(10,5))
    #散点图
    sns.scatterplot(x="Height",y="Weight",data=not_null_gold_medals)
    plt.title("金牌获得者身高与体重关系",fontproperties=font)
    plt.savefig("gold_height_and_weight.jpg")
    plt.show()

#男运动员随时间的变化
def athletes_over_time():
    #性别+夏季运动会
    men_over_time = merged[(merged.Sex == "M") & (merged.Season == "Summer")]
    #根据年份统计性别出现的次数
    men_part = men_over_time.groupby('Year')['Sex'].value_counts()
    plt.figure(figsize=(10,5))
    #折线图
    men_part.loc[:,'M'].plot()
    plt.title('男性运动员人数随时间变化',fontproperties=font)
    plt.savefig("men_over_time.jpg")
    plt.show()

#######################################################
#女运动员随时间的变化
def athletes_over_time2():
    women_over_time = merged[(merged.Sex == "F") & (merged.Season == "Summer")]
    # 根据年份统计性别出现的次数
    women_part = women_over_time.groupby('Year')['Sex'].value_counts()
    plt.figure(figsize=(10, 5))
    # 折线图
    women_part.loc[:, 'F'].plot()
    plt.title('女性运动员人数随时间变化', fontproperties=font)
    plt.savefig("women_over_time.jpg")
    plt.show()

#男性运动员年龄随时间变化
def athletes_over_ages():
    # 性别+夏季运动会
    men_over_age = merged[(merged.Sex == "M") & (merged.Season == "Summer") & (merged.Age.notnull())]
    plt.figure(figsize=(10, 5))
    #箱型图
    sns.boxplot('Year',"Age",data=men_over_age)
    plt.title('男性运动员年龄随时间变化', fontproperties=font)
    #  设置x轴的刻度字体大小
    plt.xticks(fontproperties=font, fontsize=8)
    plt.savefig("men_over_age.jpg")
    plt.show()

#男性运动员体重随时间变化
def athletes_over_weight():
    men_over_weight = merged[(merged.Sex == "M") & (merged.Season == "Summer") & (merged.Age.notnull())]
    plt.figure(figsize=(10, 5))
    #点-折线图
    sns.pointplot('Year','Weight',data=men_over_weight)
    plt.title('男性运动员体重随时间变化', fontproperties=font)
    #  设置x轴的刻度字体大小
    plt.xticks(fontproperties=font, fontsize=8)
    plt.savefig("men_over_weight.jpg")
    plt.show()



if __name__ == "__main__":
    # gold_medals()
    # female_athletics()
    # gold_height_and_weight()
    # athletes_over_time()
    # athletes_over_ages()
    athletes_over_weight()
