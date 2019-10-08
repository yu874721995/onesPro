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
import urllib.request
import re


def sendMsg(request):
    response = None
    try:

        openid = request.GET.get('openid',None)
        signature = request.GET.get('signature',None)
        timestamp = request.GET.get('timestamp',None)
        nonce = request.GET.get('nonce',None)
        wechat = WechatBasic(token='yu874721995')
        body_text = request.body

        if wechat.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
            wechat.parse_data(body_text)
            message = wechat.get_message()
            print(message.content)
            if message.type == 'text':
                if message.content == 'wechat':
                    response = wechat.response_text(u'^_^')
                else:
                    response = wechat.response_text(u'别问，问就是没调好')
            elif message.type == 'image':
                response = wechat.response_text(u'图片')
            else:
                response = wechat.response_text(u'未知')
    except Exception as e:
        print(e)

    # x = input("主人：")
    # x = urllib.parse.quote(x)
    # link = urllib.request.urlopen(
    #     "http://nlp.xiaoi.com/robot/webrobot?&callback=__webrobot_processMsg&data=%7B%22sessionId%22%3A%22ff725c236e5245a3ac825b2dd88a7501%22%2C%22robotId%22%3A%22webbot%22%2C%22userId%22%3A%227cd29df3450745fbbdcf1a462e6c58e6%22%2C%22body%22%3A%7B%22content%22%3A%22" + x + "%22%7D%2C%22type%22%3A%22txt%22%7D")
    # html_doc = link.read().decode()
    # reply_list = re.findall(r'\"content\":\"(.+?)\\r\\n\"', html_doc)
    # print("小i：" + reply_list[-1])
    return HttpResponse(response)
    # try:
    #     xml = request.body
    #     print(xml)
    #     print(type(xml))
    #     print(request)
    # except Exception as e:
    #     print(e)
    # return HttpResponse('ss')