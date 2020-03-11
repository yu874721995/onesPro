#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@Time    : 2019/11/11 17:36
@Author  : Careslten
@Site    : 
@File    : __init__.py.py
@Software: PyCharm
'''

import requests, json, xlwt, xlrd,time,threading

def work():
    f = xlrd.open_workbook('Excel_test.xls')
    sheet = f.sheet_by_index(0)
    cols = sheet.col_values(1)
    url = ''
    b = ''
    for i in cols:
        r = requests.post('http://api.tuke.huakmall.com/user/friend/add',data={
            'access_token':'eyJhbGciOiJITUFDU0hBMjU2IiwiaXNzIjoiRWFzeVN3b29sZSIsImV4cCI6MTYxNTM2NzM3OSwic3ViIjpudWxsLCJuYmYiOjE1ODM4MzEzNzksImF1ZCI6bnVsbCwiaWF0IjoxNTgzODMxMzc5LCJqdGkiOiJ5YURPMDJ2MUZpIiwic2lnbmF0dXJlIjoiZTNmNTFmNWI5NmEzMmIwZDMyM2RhZTBiNTM1Njc1YjFjZTdmNjhjMGFkMDMwNWVhMGJhNTUyOWRjNTA3NzAxMCIsInN0YXR1cyI6MSwiZGF0YSI6ImxleWpwZGkyY3UifQ%3D%3D',
            'user_id':i,
            'remark':'test'
        })
        time.sleep(0.5)
        print(r.json())
        print('-------ok')
    print('ok')

t = threading.Thread()




# rs = len(r.json()['info']['list'])
# rs_l = r.json()['info']['list']
# # with open('tuk.xlsx','wb') as f:
# #     f.write()
# workbook = xlwt.Workbook(encoding = 'utf-8')
# worksheet = workbook.add_sheet('My Worksheet')
# for i in range(rs):
#     worksheet.write(i,1,rs_l[i]['friend_user_id'])
#     worksheet.write(i, 2, rs_l[i]['user']['name'])
# workbook.save('Excel_test.xls')



