#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@Time    : 2019/11/12 16:43
@Author  : Careslten
@Site    : 
@File    : loginAndRegite.py
@Software: PyCharm
'''

from django.http import HttpResponse
from xcx import models
import json,os,time
import logging
import datetime
from Public.JsonData import DateEncoder
from django.forms.models import model_to_dict
from ruamel import yaml


logger = logging.getLogger(__name__)

class login_and_reg():


    def getUserInfo(self,request):
        logger.info('request_body:',request)
        nikeName = request.POST.get('nikeName',None)
        openId = request.POST.get('openId',None)
        sex = request.POST.get('sex',None)
        headimg = request.POST.get('headImg',None)
        print(request.POST)
        if nikeName == None or openId == None or sex == None or headimg ==None or nikeName == '' or openId == '' or sex == '' or headimg == '':
            return HttpResponse(json.dumps({'status':3,'msg':'参数错误'}))
        query = models.UserInfo.objects.filter(wxopenid=openId).values()
        if len(query) == 1:
            data = ''
            for item in query:
                data = item['id']
            models.UserInfo.objects.filter(wxopenid=openId).update(old_login_time=datetime.datetime.today())
            return HttpResponse(json.dumps({'status':1,'data':data}))
        elif len(query) == 0:
            dic = {
                'usernikename':nikeName,
                'sex':sex,
                'headimg':headimg,
                'wxopenid':openId
            }
            try:
                models.UserInfo.objects.create(**dic)#创建用户
                query = models.UserInfo.objects.filter(wxopenid=openId).values()
                datas = ''
                for item in query:
                    datas = item['id']
                return HttpResponse(json.dumps({'status':1,'data':datas}))
            except Exception as e:
                logger.error(e)
                print(e)
                return HttpResponse(json.dumps({'status':5,'msg':'数据库错误'}))


