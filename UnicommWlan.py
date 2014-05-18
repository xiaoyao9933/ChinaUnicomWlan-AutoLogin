#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# Auto login the unicomm wlan 
# By Lu CHAO(me@chao.lu) ,2013 10 12.

from urllib2 import build_opener,HTTPCookieProcessor
from urllib import urlencode
from cookielib import CookieJar
import time,sys
from random import random
global loop
global count
loop=True
count=0
def LoginWlan(user,password,address):
    index_page = "http://202.106.46.37/"
    global loop,count
    try:
        #获得一个cookieJar实例
        cj = CookieJar()
        #cookieJar作为参数，获得一个opener的实例
        opener=build_opener(HTTPCookieProcessor(cj))
        #伪装成一个正常的浏览器，避免有些web服务器拒绝访问。
        opener.addheaders = [('User-agent','Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')]
        #生成Post数据，含有登陆用户名密码。
        data = urlencode({"username":user,"password":password,"passwordType":6,"wlanuserip":"","userOpenAddress":address,"checkbox":0,"basname":"","setUserOnline":"","sap":"","macAddr":"","bandMacAuth":0,"isMacAuth":"","basPushUrl":"http%253A%252F%252F202.106.46.37%252F","passwordkey":""})
        #以post的方法访问登陆页面，访问之后cookieJar会自定保存cookie
        opener.open(index_page,timeout=20)
        #以带cookie的方式访问页面ss
        op=opener.open("http://202.106.46.37/login.do",data,timeout=20)
        #读取页面源码
        data= op.read()
        if 'success' in data:
            print "%s : Logsin Success"%(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        elif u"此账号已在线！" in data.decode('utf-8'):
            count=count+1 
        else:
            print "%s :Failed "%(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
            print data.decode('utf-8')
            loop=False
        opener.close()
        return
    except Exception,e:
        print str(e)
file=open("/var/log/autologin.log",'w')
sys.stdout=file
sys.stderr=file
while loop:
#在这里更改你的用户名,密码,归属地
    LoginWlan("你的用户名","你的密码","bj")
    file.flush()
    if count%10==1:
        print "%s :Count %d"%(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),count)
    elif count>10000:
        count=0
    else:
        None    
    time.sleep(20+int(random()*5))
