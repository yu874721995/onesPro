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
    xml = request.raw_data()
    print(xml)
    print(request)
    return HttpResponse('ss')