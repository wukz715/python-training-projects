#-*- coding:utf-8 -*-

import os
import time
import json
import requests
import traceback
#线程
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
from queue import Queue

#定义线程池,方式1
executor = ThreadPoolExecutor(10)
executor2 = ThreadPoolExecutor(10)
#实例化队列
queue = Queue()

# 存放数据的根目录
dir_path = os.path.join('up_100')

#IP池，使用多个IP请求，避免B站反爬
def get_http_session(pool_connections=2,pool_maxsize=10,max_retries=3):
    '''
    :param pool_connections: 要缓存的urllib3链接池的数量
    :param pool_maxsize:最大连接数
    :param max_retries:最大重试次数
    :return:连接池
    '''
    session = requests.session()
    #适配器
    adapter = requests.adapters.HTTPAdapter(pool_connections=pool_connections,pool_maxsize=pool_maxsize,max_retries=max_retries)
    session.mount('http://',adapter)
    session.mount('https://',adapter)
    return session

def save_file(filepath,content):
    #保存结果文件，a为追加模式
    #a -> w,a为追加，w为覆盖写入，a不能用于重复拉去
    with open(filepath,'w') as f:
        f.write(content)

def make_dir(name):
    #创建目录
    up_dir = os.path.join(dir_path,name)
    if not os.path.exists(up_dir):
        os.mkdir(up_dir)
    return up_dir

def log(content,level,filepath):
    if level == "error":
        with open(filepath,'a') as f:
            f.write(content)
    elif level == 'fail':
        with open(filepath,'a') as f:
            f.write(content)

def read_json(filepath):
    with open(filepath,'r') as f:
        res = f.read()
    return json.loads(res)

def get_up_owner_base_info(name,uid):
    try:
        url = f"https://api.bilibili.com/x/space/arc/search?mid={uid}&ps=30&tid=0&pn=1&keyword=&order=pubdate&jsonp=jsonp"
        r = get_http_session().get(url, timeout=100)

        if r.status_code == 200:
            up_dir = make_dir(name)
            filepath = os.path.join(up_dir, f'{uid}-base-info.json')
            content = json.dumps(r.json(), indent=4, ensure_ascii=False)
            save_file(filepath, content)
            print(f"{name} up主信息保存成功")
            #将信息推送到队列中
            global queue
            queue.put(name,uid,filepath)
        else:
            fail_str = f"name:[{name}],uid:[{uid}],url:[{url}]"
            log(fail_str,'Fail','base_info_fail.log')
    except Exception as e:
        log(traceback.format_exc(), 'Error', 'base_info_Error.log')

def get_info_from_json(up_info):
    for up in up_info:
        uid = up['uid']
        name = up["name"]
        get_up_owner_base_info(name,uid)


def get_upowner_video_barrage_info(name,uid,filepath):
    res = read_json(filepath)
    vlist = res['data']['list']['vlist']
    for v in vlist:
        bvid = v['bvid']
        url = f"https://api.bilibili.com/x/player/pagelist?bvid={bvid}&jsonp=jsonp"
        #对应get函数使用适配器，请求url，设定超时时间
        player = get_http_session().get(url,timeout=10)
        player = player.json()
        #json数据
        data = player['data']
        #若无数据，直接返回
        if not data:
            return
        #遍历数据
        for d in data:
            try:
                cid = d['cid']
                #弹幕
                barrage_url = f'https://api.bilibili.com/x/v1/dm/list.so?oid={cid}'
                r = get_http_session().get(barrage_url,timeout=10)
                #弹幕->xml
                #保存路径
                uid_dir_path = os.path.join(dir_path,name)
                if not os.path.exists(uid_dir_path):
                    os.mkdir(uid_dir_path)
                #弹幕文件路径
                barrage_path = os.path.join(uid_dir_path,f'barrage_{uid}.xml')
                r.encoding = 'utf-8'
                #保存内容
                content = r.text
                save_file(barrage_path,content)
                print(f'video name:{name} barrage save success.')
            except Exception as e:
                log(traceback.format_exc(), 'Error', 'video_barrage_info.log')
                error_str = f"name:[{name}],uid:[{uid}]"
                log(error_str, 'error', 'barrage_info_fail.log')

def get_all_barrage_info(upowner_json):
    for bar in upowner_json:
        name = bar['name']
        uid = bar['uid']
        filepath = os.path.join(dir_path, f'{name}/{uid}-base-info.json')
        executor.submit(get_upowner_video_barrage_info,name,uid,filepath)
        #为了避免请求频繁，所以设置请求间隔
        time.sleep(1)

def get_video_comment_info(name,uid,filepath):
    res = read_json(filepath)
    vlist = res['data']['list']['vlist']
    for v in vlist:
        bvid = v['bvid']
        aid = v['aid']
        url = f"https://api.bilibili.com/x/player/pagelist?bvid={bvid}&jsonp=jsonp"
        # 对应get函数使用适配器，请求url，设定超时时间
        player = get_http_session().get(url, timeout=10)
        player = player.json()
        # json数据
        data = player['data']
        # 若无数据，直接返回
        if not data:
            return
        # 遍历数据
        for d in data:
            try:
                # 评论
                comment_url = f'https://api.bilibili.com/x/reply?jsonp=jsonp&type=1&oid={aid}&sort=1'
                r = get_http_session().get(comment_url, timeout=10)
                #
                if r.status_code == 200:
                    # 保存路径
                    uid_dir_path = os.path.join(dir_path, name)
                    if not os.path.exists(uid_dir_path):
                        os.mkdir(uid_dir_path)
                    # 弹幕文件路径                                                        
                    commet_path = os.path.join(uid_dir_path, f'commit_{uid}.json')
                    content = json.dumps(r.json(),indent = 4,ensure_ascii=False)
                    save_file(commet_path, content)
                    print(f'video name:{name} comment save success.')
            except Exception as e:
                log(traceback.format_exc(), 'Error', 'video_commint_info.log')
                error_str = f"name:[{name}],uid:[{uid}]"
                log(error_str, 'error', 'comment_info_fail.log')

def get_all_comment_info(upowner_json):
    for bar in upowner_json:
        name = bar['name']
        uid = bar['uid']
        filepath = os.path.join(dir_path, f'{name}/{uid}-base-info.json')
        #通过线程池执行操作
        executor2.submit(get_video_comment_info, name, uid, filepath)
        # 为了避免请求频繁，所以设置请求间隔
        time.sleep(1)


#方式二：使用线程池，
def video_info_task():
    with ThreadPoolExecutor(max_workers=10) as executor:
        while True:
            global queue
            name,uid,filepath = queue.get()
            executor.submit(get_video_comment_info,name,uid,filepath)
            queue.task_done()
            time.sleep(2)


if __name__ == "__main__":
    up_owner = read_json('power_up_100.json')
    # get_info_from_json(up_owner)
    # get_all_barrage_info(up_owner)
    get_all_comment_info(up_owner)
    # Thread(target=video_info_task).start()
