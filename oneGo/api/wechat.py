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
from wechat_sdk import WechatBasic


def sendMsg(request):
    token = request.GET.get('token',None)
    openid = request.GET.get('openid',None)
    signature = request.GET.get('signature',None)
    timestamp = request.GET.get('timestamp',None)
    nonce = request.GET.get('nonce',None)
    wechat = WechatBasic(token=token)
    body_text = request.body
    if wechat.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
        wechat.parse_data(body_text)
        message = wechat.get_message()

        response = None
        if message.type == 'text':
            if message.content == 'wechat':
                response = wechat.response_text(u'^_^')
            else:
                response = wechat.response_text(u'文字')
        elif message.type == 'image':
            response = wechat.response_text(u'图片')
        else:
            response = wechat.response_text(u'未知')
    return HttpResponse(response)
    # try:
    #     xml = request.body
    #     print(xml)
    #     print(type(xml))
    #     print(request)
    # except Exception as e:
    #     print(e)
    # return HttpResponse('ss')