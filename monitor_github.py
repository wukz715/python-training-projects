#-*- coding:utf-8 -*-
'''
本脚跟是通过持续监控github 的api来查看项目是否更新，若是项目更新后则打开项目url进行查看，并且拉取代码至本地
date：20200703
author：zhong
'''
import os
import time
import requests
from selenium import webdriver

def minotor_github_project(user,project_name):
    #github的api链接，数据展示为json格式数据
    api = "https://api.github.com/repos/" + user + '/' + project_name
    #github的页面展示页面
    weburl = "https://github.com/" + user + '/' + project_name
    #旧时间
    old_time = None
    while True:
        r = requests.get(api)
        if r.status_code != 200:
            print("github api 请求失败,api="+api)
            break
        #判断项目是否更新，对比更新时间是否有变化即可
        now_time = r.json()['updated_at']
        #如果old_time为空，则将now_time赋予给它，此场景只存在第一次监控时
        if not old_time:
            old_time = now_time

        #判断更新时间是否有变化
        if old_time < now_time:
            print("项目更新来")
            # 实例化
            driver = webdriver.Chrome()
            driver.get(weburl)
            #系统执行git pull的操作
            os.system(f"cd /Users/walter/Git/{project_name} && git pull")
            print("命令执行完毕")
    #为了避免循环太过于频繁，设定10分钟跟新一次
    time.sleep(600)

if __name__ == "__main__":
    minotor_github_project('wukz715','python-training-projects')
