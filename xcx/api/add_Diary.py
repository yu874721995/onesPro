#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@Time    : 2019/11/13 12:07
@Author  : Careslten
@Site    : 
@File    : add_Diary.py
@Software: PyCharm
'''

from django.http import HttpResponse
from xcx import models
import json,os,time
import datetime


class addDiarys():

    def addDiary(self,request):
        ShitOfficer = request.POST.get('userId',None)
        PetName = request.POST.get('PetName',None)
        PetSex = request.POST.get('PetSex',None)
        PetType = request.POST.get('PetType',None)
        sterilization = request.POST.get('sterilization',None)
        sterilizationTime = request.POST.get('sterilizationTime',None)
        Petbirth = request.POST.get('Petbirth',None)
        PetToHome = request.POST.get('PetToHome',None)
        PetHeadimg = request.POST.get('PetHeadimg',None)
        if ShitOfficer == None or ShitOfficer =='' or PetName == None or PetName == ''\
                or PetSex == None or PetSex == ''or PetType == None or PetType == ''\
                or sterilization == None or sterilization == ''or Petbirth == None \
                or Petbirth == ''or PetToHome == None or PetToHome == '':
            return HttpResponse(json.dumps({'status':3,'msg':'参数错误'}))
        query = models.UserInfo.objects.filter(id=ShitOfficer).values()
        if len(query) == 0:
            return HttpResponse(json.dumps({'status':3,'msg':'用户不存在'}))
        dic = {
            'ShitOfficer':ShitOfficer,
            'PetName':PetName,
            'PetSex':PetSex,
            'PetType':PetType,
            'sterilization':sterilization,
            'sterilizationTime':sterilizationTime,
            'Petbirth':Petbirth,
            'PetToHome':PetToHome,
            'PetHeadimg':PetHeadimg
        }
        try:
            models.PetFiles.objects.create(**dic)
            return HttpResponse(json.dumps({'status':1,'msg':'操作成功'}))
        except Exception as e:
            return HttpResponse(json.dumps({'status':5,'msg':'数据库错误:'}))


