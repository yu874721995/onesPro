#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@Time    : 2019/9/29 17:09
@Author  : Careslten
@Site    : 
@File    : wechat.py
@Software: PyCharm
'''
from django.http import HttpResponse
from oneGo import models
import json
import requests

def sendMsg(request):
    token = request.POST.get('token',None)
    return HttpResponse(json.dumps({'status':1,'msg':'isok'}))