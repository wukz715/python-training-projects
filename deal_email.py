#-*- coding:utf-8 -*-

import os
import pandas as pd
import yagmail
import poplib
from email.parser import  Parser
from email.header import decode_header
from twilio.rest import Client

#结果文档存放路径
excel_path="./result"
if not os.path.exists(excel_path):
    os.mkdir(excel_path)

def excel_analyze(excel_name):
    #过滤数据，key为excel表中的负责人名字，key值则是需要发送的邮箱地址（真实有效的邮箱）
    name = {
        "陈文":"13672460170@163.com",
        "白鹏":"1606795362@qq.com"
    }
    data = pd.read_excel(excel_name,sheet_name='Sheet')
    for name,email in name.items():
        df = data.loc[data['负责人'] == name]
        file_path = os.path.join(excel_path,f'{name}.xlsx')
        writer = pd.ExcelWriter(file_path)
        df.to_excel(writer,"num1")
        writer.save()
        if email:
            #如果存在邮件地址，则发送邮件
            send_email(email,name,file_path)

#自动发送邮件
def send_email(email,name,file_name):
    '''
    登陆smtp邮箱
    user-邮箱账号
    password-密码
    host-邮箱smtp服务器地址
    return:null
    '''
    yag = yagmail.SMTP(
        user = "13672460170@sina.cn",
        password = "c66a521b7941a5c7",
        host = "smtp.sina.com"
    )
    #邮件内容
    contents = [
        f"Dear {name}:",
        "你的汇报数据如附件所示，请查收！",
        file_name    #发送附件
    ]
    #发送邮件
    '''
    to：收件信箱
    subject：邮件主题
    contents：邮件内容
    '''
    yag.send(to=email,subject='Python自动发送邮件',contents=contents)

#链接邮箱 POP收件服务器
def connect_email():
    '''
    user :邮箱账号
    password：邮箱授权码
    host：邮箱POP3服务器地址
    '''
    user = "13672460170@sina.cn",
    password = "c66a521b7941a5c7",
    host = "pop.sina.com"
    #开始链接POP3服务器
    server = poplib.POP3(host)
    #打开调试信息
    server.set_debuglevel(1)
    #打印欢迎语句
    print(server.getwelcome().decode("UTF-8"))
    #进行身份验证
    server.user(user)
    server.pass_(password)
    return  server

#获取邮箱中最新邮件
def get_email_content(server):
    #获取邮箱邮件总数和占用服务器资源大小
    email_num,email_size = server.stat()
    print("*"*100)
    print(f"Email Num:{email_num},Emali Size:{email_size}")
    #根据索引id获取邮件信息
    rsp,msglines,msgsize = server.retr(email_num)
    #拼接邮件内容并对邮件内容进行GBK解码
    msg_content = b'\r\n'.join(msglines).decode("GB2312")
    #把电子邮件内容解析为Message对象
    msg = Parser().parsestr(msg_content)
    #关闭服务链接，释放资源
    server.close()
    return msg

def parser_subject(msg):
    #解析邮件主题
    subject = msg['Subject']
    #解析邮件
    value,charset = decode_header(subject)[0]
    #如果指定了字符集，则使用此字符集解码
    if charset:
        value = value.decode(charset)
    print(f"邮件主题:{value}")
    return value

def guess_charset(msg):
    charset = msg.get_charset()
    if not charset:
        content_type = msg.get('Content-Type','').lower()
        pos = content_type.find('charset=')
        if pos > 0 :
            charset = content_type[pos + 8:].strip()
    return  charset

def parser_content(msg,indent=0):
    #解析邮件内容
    #如果有多个段落，那么就需要每个部分进行解析
    if msg.is_multipart():
        #get_payload()可以知道第几部分
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            print(f"{' ' * indent * 4 }第{n+1}部分")
            print(f"{' ' * indent * 4}{'-' * 50}")
            #递归方式
            parser_content(part,indent+1)
    else:
        content_type = msg.get_content_type()
        if content_type == 'text/plain' or content_type == 'text/html':
            content = msg.get_payload(decode=True)
            #猜测字符集
            charset = guess_charset(msg)
            if charset:
                content = content.decode(charset)
                print(f"{' ' * indent * 4 }邮件内容:{content}")
        else:
            print(f"{' ' * indent * 4}附件内容:{content_type}")

def send_message():
    #发送短信
    '''
    使用Twilio网站进行发送短信
    需要在Twilioh获取sid、token和平台发送的"号码"
    '''
    #平台sid
    amount_sid = ""
    #平台token
    auth_token = ""
    #客户端实例化
    client = Client(amount_sid,auth_token)
    #发送消息,from发送手机号，to接收手机号，body是短信内容，加号+和区号不能省略，因为是全球使用的
    message = client.message.create(
        to="", #接收信息的手机号，+和区号不能够省略
        from_="",  #twilio分配的手机号，+号不能省略
        body="这是来自python自动化的短信。"
    )


if __name__ == "__main__":
    # excel_analyze("渠道数据分析总表.xlsx")
    # send_email("13672460170@163.com","zhong","./result/陈文.xlsx")
    server = connect_email()
    msg = get_email_content(server)
    parser_subject(msg)
    parser_content(msg)
