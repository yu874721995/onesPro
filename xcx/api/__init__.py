#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@Time    : 2019/11/11 17:36
@Author  : Careslten
@Site    : 
@File    : __init__.py.py
@Software: PyCharm
'''

import requests, json, xlwt, xlrd,time

# r = requests.post('http://api.tuke.huakmall.com/user/friend/index',data={
#     'access_token':'eyJhbGciOiJITUFDU0hBMjU2IiwiaXNzIjoiRWFzeVN3b29sZSIsImV4cCI6MTYxNTI3NTYwNywic3ViIjpudWxsLCJuYmYiOjE1ODM3Mzk2MDcsImF1ZCI6bnVsbCwiaWF0IjoxNTgzNzM5NjA3LCJqdGkiOiJ2NDU3RzFIUURsIiwic2lnbmF0dXJlIjoiNmM1NWI0OGE1YzUyZDEwMmYzOGU4OGUwNGVmYzhmY2FkNWJhMDdhY2IyYjgyMjM0NDM5YjA2YTJjNTczNzhhYSIsInN0YXR1cyI6MSwiZGF0YSI6IjJpanU0cnhqYXQifQ%3D%3D',
#     'limit':10000,
#     'page':1
# })
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
# f = xlrd.open_workbook('Excel_test.xls')
# sheet = f.sheet_by_index(0)
# cols = sheet.col_values(2)
# url = ''
# b = ''
# for i in range(len(cols)):
#     b = b + '"'+str(cols[i]).split('.')[0] +'"'+ ','
# print(b)

