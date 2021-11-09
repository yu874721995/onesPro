#!/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: dxl
@file: luckDraw.py
@time: 2021/9/1 17:23
@desc: 
"""
from datetime import datetime
import random

import requests
import threading


url = "https://dev-api.51dengta.net/activity/lucky/luckDraw"
r = requests.Session()
name = []
time = []
token = []
user_id = [
5766366696,
7078388524,
7152062823,
7171943187,
7814527742,
7850199147,
7941135669,
8050870178,
8287230510,
8378731005,
8442370930,
8465248920,
8764420247,
8873280929,
8897590762,
9185027928,
9203988439,
9262125751,
9408246352,
9539518664,
9697854505,
9743962493,
9906958360
]
for i in range(10):
    url2 = "https://dev-api.51dengta.net/user/auth/smsLogin"
    payload2={'phone': '1850000000{}'.format(i),
    'code': '80008',
    'version': '1.7.3'}
    response = r.request("POST", url2, data=payload2)
    re = response.json()
    str = re['info']['access_token']
    token.append(str)
def func():
    ran = random.randint(0, 9)
    rid_random = random.randint(0, 500)
    for i in range(10):
        payload={
        'access_token': token[0],
        'times': '1',
        'to_user_id': user_id[0],
        'rid': rid_random,
        'version':'1.73'}
        try:
            response = r.request("POST", url, data=payload,timeout=30)
            re = response.json()
            str = re['info']['list'][0]['name']
            name.append(str)
            if len(name)%100 == 0:
                print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        except Exception as e:
            print(response.text)
            name.append('异常')
            continue


thead = []
for i in range(10):
    a = threading.Thread(target=func,args=[])
    thead.append(a)

for i in thead:
    i.start()
    print('线程启动{}'.format(i))

for i in thead:
    i.join()


set=set(name)
dict={}
for item in set:
    dict.update({item:name.count(item)})

gailv = []
for values in dict.values():
    gailv.append(values)

sum = 0
for i in gailv:
    sum += i

list2 = []
for i in gailv:
    list2.append(i/sum * 100)

print(dict)
print("一共{}次，概率{}".format(len(name),list2))
