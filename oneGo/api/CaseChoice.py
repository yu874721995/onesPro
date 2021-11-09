#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@Time    : 2019/7/18 20:11
@Author  : Careslten
@Site    : 
@File    : CaseChoice.py
@Software: PyCharm
'''
import requests
import datetime
from django.conf import settings
from django.http import HttpResponse
from oneGo import models
import json,os,time
from Public.JsonData import DateEncoder
from django.forms.models import model_to_dict
from ruamel import yaml
from Public.runner import runner_case
from multiprocessing import Process


class caseChoice():

    #添加产品或添加模块
    def addChoice(self,request):
        cpname = request.POST.get('cpname',None)
        types = request.POST.get('type',None)
        if cpname == '' or cpname == None or types == '' or types == None:
            return HttpResponse(json.dumps({'status':200, 'msg': '名称或类型不能为空'}))
        query_cp = models.casecp_mk.objects.filter(name=cpname,status=1,type=1).values()
        #如果已存在则无法添加
        if len(query_cp) != 0:
            return HttpResponse(json.dumps({'status':200, 'msg': '该产品已存在'}))
        if types == 1 or types == '1':
            try:
                dic = {'type':'1', 'name': cpname, }
                models.casecp_mk.objects.create(**dic)
                return HttpResponse(json.dumps({'status':1, 'msg': '操作成功'}))
            except Exception as e:
                print('error----------------1',e)
                return HttpResponse(json.dumps({'status':1, 'msg': '数据库错误'}))

            #添加模块
        else:
            subjection = request.POST.get('subjection',None)
            query_mk = models.casecp_mk.objects.filter(name=cpname, status=1, type=2, subjection=subjection).values()
            if len(query_mk) != 0:
                return HttpResponse(json.dumps({'status':200, 'msg': '该模块已存在'}))
            if subjection == '' or subjection == None:
                return HttpResponse(json.dumps({'status': 200, 'msg': '必须选择上级产品'}))
            try:
                dic = {'type':'2', 'name': cpname,'subjection':subjection }
                models.casecp_mk.objects.create(**dic)
                return HttpResponse(json.dumps({'status':1, 'msg': '操作成功'}))
            except Exception as e:
                print('error----------------1',e)
                return HttpResponse(json.dumps({'status':1, 'msg': '数据库错误'}))

    #查询产品及模块列表
    def queryForProduct(self,request):
        #仅查询产品列表
        query = models.casecp_mk.objects.filter(status=1,type=1).values()
        data = []
        for item in query:
            mores = {}
            mores['id'] = item['id']
            mores['type'] = item['type']
            mores['name'] = item['name']
            mores['create_date'] = item['create_date']
            data.append(mores)
        print('response==================',data)
        return HttpResponse(json.dumps({'status':1, 'msg': '操作成功','data':data},cls=DateEncoder))

    def queryForOur(self,request):
        querys = models.casecp_mk.objects.filter(status=1, type=1).values()
        data = []
        for items in querys:
            mores = {}
            mores['name'] = items['name']
            mores['value'] = items['id']
            query = models.casecp_mk.objects.filter(status=1, type=2,subjection=items['id']).values()
            datas = []
            for item in query:
                more = {}
                more['value'] = item['id']
                more['name'] = item['name']
                datas.append(more)
            mores['children'] = datas
            data.append(mores)
        return HttpResponse(json.dumps({'code': 0, 'data': data,'msg': 'success'}))


    #用例列表
    def caseList(self,request):
        user_id = request.session.get('user_id',None)
        page = request.POST.get('page',None)
        limit = request.POST.get('limit',None)
        fy = self.pages(page,limit)
        if user_id == None:
            return HttpResponse(json.dumps({'status':100,'msg': '登录过期'}))
        caseHost = models.user_TestCase_host.objects.all().values().order_by('status','-create_date')
        count = models.user_TestCase_host.objects.all().count()
        data = []
        #处理用例数据
        num = 0
        for i in caseHost:
            num += 1
            if num < fy[0]:
                continue
            if num > fy[1]:
                break
            case_body = {}
            case_header = {}
            case_asserts = {}
            case_data = {}
            case_data['case_id'] = i['id']
            case_data['status'] = i['status']
            case_data['caseName'] = i['caseName']
            case_data['host'] = i['host']
            case_data['create_date'] = i['create_date']
            username = models.UserInfo.objects.filter(id=i['userid']).values()[0]['username']
            case_data['username'] = username
            case_data['method'] = i['method']
            mk = models.casecp_mk.objects.filter(id=i['subjectionId']).values()[0]
            mk_name = mk['name']
            cp = models.casecp_mk.objects.filter(id=mk['subjection']).values()[0]['name']
            case_data['subjection_cp'] = cp
            case_data['subjection_mk'] = mk_name
            case_data['create_date'] = i['create_date']

            #在这里添加assert和body、header的内容
            body = models.user_TestCase_body.objects.filter(host_id=i['id'],type=1).values()
            for a in body:
                case_body[a['key']] = a['value']
            case_data['case_body'] = case_body

            header = models.user_TestCase_body.objects.filter(host_id=i['id'],type=2).values()
            for b in header:
                case_header[b['key']] = b['value']
            case_data['case_header'] = case_header

            asserts = models.user_Case_Assert.objects.filter(host_id=i['id']).values()
            asserts_count = models.user_Case_Assert.objects.filter(host_id=i['id']).count()
            for c in asserts:
                case_asserts[c['Assert_name']] = c['Assert_text']
            case_asserts['count'] = asserts_count
            case_data['case_assert'] = case_asserts


            data.append(case_data)

        return HttpResponse(json.dumps({'code':0,'count':count,'data':data,'msg':'操作成功','status':1},cls=DateEncoder))

    def zhaohu(self,request):
        id = request.POST.get('id',None)
        import requests
        from django.shortcuts import render
        r = requests.Session()
        url = 'https://manager.dengtayiduiyi.com/'
        # url = 'https://test-manager.dengtayiduiyi.com/'
        r.headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                     'cookie': settings.SHENHE_COOKIE,
                     'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
                     'x-requested-with': 'XMLHttpRequest'
                     }
        zhaohu = r.get(url+'/admin.php/app/greet/detail.html?id={}&hisi_iframe=yes'.format(id)).text
        return HttpResponse(json.dumps({'data':zhaohu,'msg':'操作成功','status':1},cls=DateEncoder))

    def shenheList(self,request):
        # token = request.GET.get('token',None)
        # if token == None:
        #     return HttpResponse(json.dumps({'status':100,'msg': '非法用户'}))
        r = requests.Session()
        url = 'https://manager.dengtayiduiyi.com/'
        # url = 'https://test-manager.dengtayiduiyi.com/'
        r.headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                     'cookie': settings.SHENHE_COOKIE,
                     'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
                     'x-requested-with': 'XMLHttpRequest'
                     }
        touxiang_shenhe = r.post(url+'/admin.php/app/user/avataraudit.html?page=1&limit=10', data={
            'status': 1
        }).json()['data']
        dongtaishenhe_shenhe = r.post(url+'/admin.php/app/content_audit/moments.html', data={
            'status': 1
        }).json()['data']
        xiangce_shenhe = r.post(url+'/admin.php/app/photo/audit.html', data={
            'status': 2
        }).json()['data']
        zhenren_renzheng = r.post(url+'/admin.php/app/content_audit/userrealauth.html',data={
            'datetime_start':'2021-11-02 10:00:00',
            'datetime_end':'2021-11-02 10:19:06'
        }).json()['data']  # 真人认证
        biaoqian_shenhe = r.post(url+'/admin.php/app/user/checktag.html', data={
            'pass_status': 1
        }).json()['data']  # 标签
        zhaohu_shenhe = r.post(url+'/admin.php/app/greet/index.html?page=1&limit=10&field=1&name=&status=-1&datetime_start=&datetime_end=&agent_user_id=0').json()['data']
        data = []
        querys = []
        if len(touxiang_shenhe) == 0 and len(dongtaishenhe_shenhe) == 0 and len(xiangce_shenhe) == 0 and len(
                zhenren_renzheng) == 0 and len(biaoqian_shenhe) == 0 and len(zhaohu_shenhe) ==0:
            return HttpResponse(json.dumps({'code':0,'count':0,'data':data,'msg':'操作成功','status':1},cls=DateEncoder))
        for i in touxiang_shenhe:
            query = {}
            query['data'] = i
            query['type'] = '头像'
            querys.append(query)
        for i in dongtaishenhe_shenhe:
            query = {}
            query['data'] = i
            query['type'] = '动态'
            querys.append(query)
        for i in xiangce_shenhe:
            query = {}
            query['data'] = i
            query['type'] = '相册'
            querys.append(query)
        for i in zhenren_renzheng:
            query = {}
            query['data'] = i
            query['type'] = '真人'
            querys.append(query)
        for i in biaoqian_shenhe:
            query = {}
            query['data'] = i
            query['type'] = '标签'
            querys.append(query)
        for i in zhaohu_shenhe:
            query = {}
            query['data'] = i
            query['type'] = '招呼'
            querys.append(query)
        for i in querys:
            print(i)
        #处理用例数据
        # num = 0
        # for i in touxiang_shenhe:
        #     case_body = {}
        #     case_header = {}
        #     case_asserts = {}
        #     case_data = {}
        #     case_data['case_id'] = i['id']
        #     case_data['status'] = i['status']
        #     case_data['caseName'] = i['caseName']
        #     case_data['host'] = i['host']
        #     case_data['create_date'] = i['create_date']
        #     username = models.UserInfo.objects.filter(id=i['userid']).values()[0]['username']
        #     case_data['username'] = username
        #     case_data['method'] = i['method']
        #     mk = models.casecp_mk.objects.filter(id=i['subjectionId']).values()[0]
        #     mk_name = mk['name']
        #     cp = models.casecp_mk.objects.filter(id=mk['subjection']).values()[0]['name']
        #     case_data['subjection_cp'] = cp
        #     case_data['subjection_mk'] = mk_name
        #     case_data['create_date'] = i['create_date']
        #
        #     #在这里添加assert和body、header的内容
        #     body = models.user_TestCase_body.objects.filter(host_id=i['id'],type=1).values()
        #     for a in body:
        #         case_body[a['key']] = a['value']
        #     case_data['case_body'] = case_body
        #
        #     header = models.user_TestCase_body.objects.filter(host_id=i['id'],type=2).values()
        #     for b in header:
        #         case_header[b['key']] = b['value']
        #     case_data['case_header'] = case_header
        #
        #     asserts = models.user_Case_Assert.objects.filter(host_id=i['id']).values()
        #     asserts_count = models.user_Case_Assert.objects.filter(host_id=i['id']).count()
        #     for c in asserts:
        #         case_asserts[c['Assert_name']] = c['Assert_text']
        #     case_asserts['count'] = asserts_count
        #     case_data['case_assert'] = case_asserts
        #
        #
        #     data.append(case_data)

        return HttpResponse(json.dumps({'code':0,'count':0,'data':querys,'msg':'操作成功','status':1},cls=DateEncoder))

    def removezhenren(self,request):
        id = request.POST.get('id', None)
        if id is None or id == '':
            return HttpResponse(json.dumps({'msg':'参数错误','status':500}))
        r = requests.Session()
        url = 'https://manager.dengtayiduiyi.com/'
        # url = 'https://test-manager.dengtayiduiyi.com/'
        r.headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                     'cookie': settings.SHENHE_COOKIE,
                     'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
                     'x-requested-with': 'XMLHttpRequest'
                     }
        rz = r.post(url + '/admin.php/app/content_audit/userRealAuthDel.html',data={'id':id})
        if rz.json()['msg'] == '操作成功':
            return HttpResponse(json.dumps({'msg': '删除成功', 'status': 1}))
        else:
            return HttpResponse(json.dumps({'msg': rz.text, 'status': 500}))

    def shijishenhe(self,request):
        import requests
        type = request.POST.get('type',None)
        status = request.POST.get('status',None)
        id = request.POST.get('id',None)
        if type ==None or status ==None or id == None:
            return HttpResponse(json.dumps({'status':500,'msg': '参数错误'}))
        r = requests.Session()
        url = 'https://manager.dengtayiduiyi.com/'
        # url = 'https://test-manager.dengtayiduiyi.com/'
        r.headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                     'cookie': settings.SHENHE_COOKIE,
                     'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
                     'x-requested-with': 'XMLHttpRequest'
                     }
        msg = ''
        if type == '头像':
            msg = r.post(url+'/admin.php/app/user/toaudit.html',data={
                'id':id,
                'status':status
            }).json()['msg']
        if type == '动态':
            if status == '1' or status == 1:
                msg = r.post(url+'/admin.php/app/content_audit/auditmoments.html?id={}'.format(id),data={
                    'audit':status,
                    'is_top':0
                }).json()['msg']
            elif status == '2' or status == 2:
                msg = r.post(url + '/admin.php/app/content_audit/auditmoments.html', data={
                    'id':id,
                    'audit': status,
                    'error_msg':'您的动态不符合规范',
                    'is_top': 0
                }).json()['msg']
        if type == '招呼':
            msg = r.post(url + '/admin.php/app/greet/audit.html', data={
                'id': id,
                'status': status
            }).json()['msg']
        if type == '相册':
            if status == 1 or status == '1':
                msg = r.post(url + '/admin.php/app/photo/toaudit.html', data={
                    'id': id,
                    'status': 2
                }).json()['msg']
            elif status == 2 or status == '2':
                msg = r.post(url + '/admin.php/app/photo/toaudit.html', data={
                    'content':'您上传的图片/视频未通过审核，请重新上传！温馨提示：涉及色情、违法的图片/视频将无法通过审核。',
                    'id': id,
                    'status': 3
                }).json()['msg']
        if type == '标签':
            if status == 1 or status == '1':
                msg = r.post(url + '/admin.php/app/user/totagaudit.html', data={
                    'id': id,
                    'status': 2
                }).json()['msg']
            elif status == 2 or status == '2':
                msg = r.post(url + '/admin.php/app/user/totagaudit.html', data={
                    'content': '与本人不符！',
                    'id': id,
                    'status': 0
                }).json()['msg']
        if msg == '操作成功':
            return HttpResponse(json.dumps({'status':200,'msg': '审核成功'}))
        else:
            return HttpResponse(json.dumps({'status': 400, 'msg': '审核失败'}))

    #分页
    def pages(self,page,limit):
        page = int(page)
        limit = int(limit)
        if page == 1:
            return (1,limit)
        begin = (page - 1) * limit + 1
        end = page * limit
        return (begin,end)

    def fuc(self,case_name):
        print(os.getpid())
        report_name = runner_case().run(case_name=case_name)
        return report_name

    #执行用例
    def batchExecution(self,request):
        user_id = request.session.get('user_id',None)
        if user_id == None:
            return  HttpResponse(json.dumps({'status':100,'msg': '登录过期'}))
        caseId = request.POST.get('caseId',None).lstrip('[').rstrip(']').split(',')
        date = self.query_case(caseId)
        # path = os.path.dirname(os.path.abspath('.')) + '/Public/case_date.yaml'

        path = os.path.abspath('.') + '/Public/case_date.yaml'
        # path = os.path.dirname(os.path.abspath('.')) + '/Public/case_date.json'
        datas = {}
        case_name = []
        num = 0
        for i in date:
            i = eval(repr(i).replace('\\',''))
            datas[num] = i
            case_name.append(i['caseName'])
            num += 1
        try:
            with open(path,'w',encoding='utf-8') as f:
                yaml.dump(datas,f,Dumper=yaml.RoundTripDumper)
            # result = yaml.safe_dump(datas, encoding='utf-8', allow_unicode=True, default_flow_style=False)
            # open(path,'wb').write(result)

            # with open(path,'w') as f:
            #     json.dump(datas,f)
            #     f.close()
            isOk = True
        except Exception as e:
            print('error-----------------------------:',e)
            return HttpResponse(json.dumps({'status':500,'msg': '~出错了，请重试'}))
        # self.query_case(caseId)
        # 执行测试
        # p = Process(target=self.fuc, args=case_name)
        report_name = ''
        try:
            report_name = runner_case().run(case_name=case_name)
            # p.start()
            print(2321321321321321321321)

        except Exception as e:
            print(1111111111111111111,e)
        dic = {
            'report_name':report_name,'becuxe_id':str(caseId),'type':1
        }
        try:
            models.Case_report.objects.create(**dic)
        except Exception as e:
            print(23213213123123213213213213,e)
            return HttpResponse(json.dumps({'status':500,'msg': '出错了，请重试'}))
        return HttpResponse(json.dumps({'status': 1, 'msg': '操作成功'}))







    #获取需要执行的用例数据
    def query_case(self,caseId):
        case_data = models.user_TestCase_host.objects.filter(id__in=caseId,status=1)
        data = []
        for i in case_data:
            i = model_to_dict(i)
            case_body = {}
            case_header = {}
            case_asserts = {}
            case_data = {}
            case_data['case_id'] = i['id']
            case_data['status'] = i['status']
            case_data['caseName'] = i['caseName']
            case_data['host'] = i['host']
            username = models.UserInfo.objects.filter(id=i['userid']).values()[0]['username']
            case_data['method'] = i['method']

            # 在这里添加assert和body、header的内容
            body = models.user_TestCase_body.objects.filter(host_id=i['id'], type=1).values()
            for a in body:
                case_body[a['key']] = a['value']
            case_data['case_body'] = case_body
            header = models.user_TestCase_body.objects.filter(host_id=i['id'], type=2).values()
            for b in header:
                case_header[b['key']] = b['value']
            case_data['case_header'] = case_header
            asserts = models.user_Case_Assert.objects.filter(host_id=i['id']).values()
            asserts_count = models.user_Case_Assert.objects.filter(host_id=i['id']).count()
            for c in asserts:
                case_asserts[c['Assert_name']] = c['Assert_text']
            case_data['case_assert'] = case_asserts
            data.append(case_data)
        return data

    def zhenrenlist(self, request):
        r = requests.Session()
        url = 'https://manager.dengtayiduiyi.com/'
        # url = 'https://test-manager.dengtayiduiyi.com/'
        r.headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                     'cookie': settings.SHENHE_COOKIE,
                     'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
                     'x-requested-with': 'XMLHttpRequest'
                     }
        now_time = datetime.datetime.now()
        new_time = now_time.strftime('%Y-%m-%d %H:%M:%S')
        yes_time = now_time + datetime.timedelta(days=-1)
        old_time = yes_time.strftime('%Y-%m-%d %H:%M:%S')
        zhenren_renzheng = r.post(url + '/admin.php/app/content_audit/userrealauth.html', data={
            'datetime_start': old_time,
            'datetime_end': new_time
        }).json()['data']  # 真人认证
        querys = []
        if len(zhenren_renzheng) == 0:
            return HttpResponse(
                json.dumps({'code': 0, 'count': 0, 'data': querys, 'msg': '操作成功', 'status': 1}, cls=DateEncoder))
        for i in zhenren_renzheng:
            query = {}
            query['id'] = i['id']
            query['touxiang'] = i['avatar']
            query['image'] = i['photo']
            querys.append(query)
        return HttpResponse(
            json.dumps({'code': 0, 'count': 0, 'data': querys, 'msg': '操作成功', 'status': 1}, cls=DateEncoder))






