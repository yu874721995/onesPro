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
from wechat_sdk.messages import (
    TextMessage, VoiceMessage, ImageMessage, VideoMessage, LinkMessage, LocationMessage, EventMessage
)


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
            if isinstance(message, TextMessage):
                x = urllib.parse.quote(message.content)
                link = urllib.request.urlopen(
                    "http://nlp.xiaoi.com/robot/webrobot?&callback=__webrobot_processMsg&data=%7B%22sessionId%22%3A%22ff725c236e5245a3ac825b2dd88a7501%22%2C%22robotId%22%3A%22webbot%22%2C%22userId%22%3A%227cd29df3450745fbbdcf1a462e6c58e6%22%2C%22body%22%3A%7B%22content%22%3A%22" + x + "%22%7D%2C%22type%22%3A%22txt%22%7D")
                html_doc = link.read().decode()
                reply_list = re.findall(r'\"content\":\"(.+?)\\r\\n\"', html_doc)
                response_xiaoi = reply_list[-1]
                print(response_xiaoi)
                response_o = response_xiaoi.replace(r'\"', '')
                response_o = response_xiaoi.replace(r'\n', '')
                if '我是小i机器人' in response_xiaoi:
                    response_o = response_xiaoi.replace('我是小i机器人', '我是老母亲')
                if '我是机器人' in response_xiaoi:
                    response_o = response_xiaoi.replace('我是机器人', '哈哈哈哈哈恍恍惚惚')
                if '小i' in response_xiaoi:
                    response_o = response_xiaoi.replace('小i', '老母亲')
                if '小i机器人' in response_xiaoi:
                    response_o = response_xiaoi.replace('小i机器人', '老母亲')
                response = wechat.response_text(response_o)
            elif isinstance(message, VoiceMessage):
                response = wechat.response_text(content=u'语音信息')
            elif isinstance(message, ImageMessage):
                response = wechat.response_text(content=u'图片信息')
            elif isinstance(message, VideoMessage):
                response = wechat.response_text(content=u'视频信息')
            elif isinstance(message, LinkMessage):
                response = wechat.response_text(content=u'链接信息')
            elif isinstance(message, LocationMessage):
                response = wechat.response_text(content=u'地理位置信息')
            elif isinstance(message, EventMessage):  # 事件信息
                if message.type == 'subscribe':  # 关注事件(包括普通关注事件和扫描二维码造成的关注事件)
                    if message.key and message.ticket:  # 如果 key 和 ticket 均不为空，则是扫描二维码造成的关注事件
                        response = wechat.response_text(content=u'用户尚未关注时的二维码扫描关注事件')
                    else:
                        response = wechat.response_text(u'谢谢长得这么好看还这么可爱的你来关注老母亲，以后让我们一起变美吧，嘻嘻')
                elif message.type == 'unsubscribe':
                    response = wechat.response_text(content=u'取消关注事件')
                elif message.type == 'scan':
                    response = wechat.response_text(content=u'用户已关注时的二维码扫描事件')
                elif message.type == 'location':
                    response = wechat.response_text(content=u'上报地理位置事件')
                elif message.type == 'click':
                    response = wechat.response_text(content=u'自定义菜单点击事件')
                elif message.type == 'view':
                    response = wechat.response_text(content=u'自定义菜单跳转链接事件')
                elif message.type == 'templatesendjobfinish':
                    response = wechat.response_text(content=u'模板消息事件')
            else:
                response = wechat.response_text(u'这么难的问题，你不是为难我胖虎吗')
    except Exception as e:
        print(e)
        return HttpResponse(wechat.response_text(u'这么难的问题，你不是为难我胖虎吗'))
    print(response)
    return HttpResponse(response)