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
from django.shortcuts import render

def sendMsg(request):
    try:
        xml = request.body
        print(xml)
        print(request)
    except Exception as e:
        print(e)
    return HttpResponse('ss')