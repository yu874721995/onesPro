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
    openid = request.GET.get('openid', None)
    signature = request.GET.get('signature', None)
    timestamp = request.GET.get('timestamp', None)
    nonce = request.GET.get('nonce', None)
    wechat = WechatBasic(token='yu874721995')
    body_text = request.body
    wechat.parse_data(body_text)
    try:
        if wechat.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
            message = wechat.get_message()
            print(message.content)
            if message.type == 'text':
                if message.content == 'wechat':
                    response = wechat.response_text(u'^_^')
                else:
                    x = urllib.parse.quote(message.content)
                    link = urllib.request.urlopen(
                        "http://nlp.xiaoi.com/robot/webrobot?&callback=__webrobot_processMsg&data=%7B%22sessionId%22%3A%22ff725c236e5245a3ac825b2dd88a7501%22%2C%22robotId%22%3A%22webbot%22%2C%22userId%22%3A%227cd29df3450745fbbdcf1a462e6c58e6%22%2C%22body%22%3A%7B%22content%22%3A%22" + x + "%22%7D%2C%22type%22%3A%22txt%22%7D")
                    html_doc = link.read().decode()
                    reply_list = re.findall(r'\"content\":\"(.+?)\\r\\n\"', html_doc)
                    response_xiaoi = reply_list[-1]
                    print(response_xiaoi)
                    response_o = response_xiaoi.replace(r'\"','')
                    response_o = response_xiaoi.replace(r'\n', '')
                    if '我是小i机器人' in response_xiaoi:
                        response_o = response_xiaoi.replace('我是小i机器人','我是老母亲')
                    if '我是机器人' in response_xiaoi:
                        response_o = response_xiaoi.replace('我是机器人', '哈哈哈哈哈恍恍惚惚')
                    if '小i' in response_xiaoi:
                        response_o = response_xiaoi.replace('小i', '老母亲')
                    if '小i机器人' in response_xiaoi:
                        response_o = response_xiaoi.replace('小i机器人', '老母亲')
                    response = wechat.response_text(response_o)
            elif message.type == 'image':
                response = wechat.response_text(u'图片')
            else:
                response = wechat.response_text(u'这么难的问题，你不是为难我胖虎吗')
    except Exception as e:
        print(e)
        return HttpResponse(wechat.response_text(u'这么难的问题，你不是为难我胖虎吗'))
    print(response)
    return HttpResponse(response)