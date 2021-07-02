from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
import pymysql as mysql
import json, time
from oneGo import models
import requests

from django.contrib.auth.decorators import login_required
import datetime

user_list = []


def update(request):
    return render(request, 'update_hl_time.html')

def look(request):
    return render(request, 'member-list1.html')


def commit(request):
    phone = request.POST.get('phone', None)
    times = str(time.time()).split('.')[0] + '000'
    import pymysql
    try:
        conn = pymysql.connect(
            host='120.79.154.96',
            user='root', password='Ysh@#2020',
            database='date',
            charset='utf8')
        cursor = conn.cursor()
        sql = "update js_match_maker_audit set audit_time=%s where uid=(select id from js_user where phone =%s and status=1);"
        cursor.execute(sql, [times, phone])
        conn.commit()
        cursor.close()
        conn.close()
        return HttpResponse(json.dumps({'status': 1,
                                        'msg': 'ok'}))
    except Exception as e:
        return HttpResponse(json.dumps({'status': 500,
                                        'msg': 'error'}))


def hlshengji(request):
    phone = request.POST.get('phone', None)
    times = str(time.time()).split('.')[0] + '000'
    byte_phone = phone.encode('utf-8')
    str_phone = base64.b64encode(byte_phone)
    import pymysql
    try:
        conn = pymysql.connect(
            host='120.79.154.96',
            user='root', password='Ysh@#2020',
            database='date',
            charset='utf8')
        cursor = conn.cursor()
        sql = "update js_match_maker_audit set up_time=%s where uid=(select id from js_user where mobile =%s and status=1);"
        print(times, phone)
        cursor.execute(sql, [times, str_phone])
        conn.commit()
        cursor.close()
        conn.close()
        return HttpResponse(json.dumps({'status': 1,
                                        'msg': 'okokokok'}))
    except Exception as e:
        return HttpResponse(json.dumps({'status': 500,
                                        'msg': 'error'}))


import base64


def gaihuahua(request):
    phones = request.POST.get('phones', None)
    coin = request.POST.get('coin', None)
    config = request.POST.get('config', None)
    phone = phones.split('-')[1]
    area_code = phones.split('-')[0]
    print(phone, coin, config,area_code)
    byte_phone = phone.encode('utf-8')
    str_phone = base64.b64encode(byte_phone)
    print(str_phone)
    import pymysql
    if config == '5':
        try:
            conn = pymysql.connect(
                host='121.201.57.208',
                user='root', password='Jskj@1234',
                database='tatalive_date',
                charset='utf8')
            cursor = conn.cursor()
            sql = "update js_user set coin=%s where mobile=%s and area_code = %s and status=1;"
            cursor.execute(sql, [coin,str_phone,area_code])
            conn.commit()
            cursor.close()
            conn.close()
            r = requests.get('https://dev-api.tatalive.net/index/sign?sign=2')
            if r.status_code != 200:
                return HttpResponse(json.dumps({'status': 5,
                                                'msg': '更新缓存失败'}))
            return HttpResponse(json.dumps({'status': 1,
                                            'msg': '修改成功'}))
        except Exception as e:
            print(e)
            return HttpResponse(json.dumps({'status': 500,
                                            'msg': '接口异常'}))
    if config == '1':
        if coin == '99999':
            try:
                r = requests.post('https://test-api.51dengta.net/user/auth/smsLogin', data={
                    'phone': phone,
                    'code': '80008'
                })
                token = r.json()['info']['access_token']
                r2 = requests.post('https://test-api.51dengta.net/user/account/recharge', data={
                    'access_token': token,
                    'menu_id': 8,
                    'pay_type': 1,
                    'order_src': 1,
                    'version':'1.1.3'
                })
                order_id = r2.json()['info']['order_id']
                r3 = requests.post('https://test-api.51dengta.net/pay/test', data={
                    'order_id': order_id,
                    'access_token': token
                })
                if r3.status_code != 200:
                    return HttpResponse(json.dumps({'status': 5,
                                                    'msg': '更新缓存失败'}))
                return HttpResponse(json.dumps({'status': 1,
                                                'msg': '修改成功'}))
            except Exception as e:
                print(e)
                return HttpResponse(json.dumps({'status': 500,
                                                'msg': '接口异常'}))
        else:
            try:
                # conn = pymysql.connect(
                #     host='rm-wz9syc23nmy8v2cvc6o.mysql.rds.aliyuncs.com',
                #     user='dengta_php', password='Ysh@#2021',
                #     database='testdate',
                #     charset='utf8')
                # cursor = conn.cursor()
                # sql = "update js_user set coin=%s where mobile=%s and status=1;"
                # cursor.execute(sql, [coin, str_phone])
                # conn.commit()
                # cursor.close()
                # conn.close()
                # r = requests.get('https://test-api.51dengta.net/index/sign?sign=2')
                # if r.status_code != 200:
                #     return HttpResponse(json.dumps({'status': 5,
                #                                     'msg': '更新缓存失败'}))
                r = requests.post('https://test-api.51dengta.net/common/java/updateFollow',data={
                    'mobile':phone,
                    'follow':coin,
                    'password':888888
                })
                if r.json()['result'] == True:
                    return HttpResponse(json.dumps({'status': 1,
                                                    'msg': '修改成功'}))
                else:
                    print(r.json())
                    return HttpResponse(json.dumps({'status': 500,
                                                'msg': '没改成功'}))
            except Exception as e:
                print(e)
                return HttpResponse(json.dumps({'status': 500,
                                                'msg': '接口异常'}))


    elif config == '2':
        try:
            r = requests.post('https://dev-api.51dengta.net/common/java/updateFollow', data={
                'mobile': phone,
                'follow': coin,
                'password': 888888
            })
            if r.json()['result'] == True:
                return HttpResponse(json.dumps({'status': 1,
                                                'msg': '修改成功'}))
            else:
                return HttpResponse(json.dumps({'status': 500,
                                                'msg': '没改成功'}))
        except Exception as e:
            print(e)
            return HttpResponse(json.dumps({'status': 500,
                                            'msg': '接口异常'}))
    elif config == '3':
        try:
            r = requests.post('https://uat-api.51dengta.net/common/java/updateFollow', data={
                'mobile': phone,
                'follow': coin,
                'password': 888888
            })
            if r.json()['result'] == True:
                return HttpResponse(json.dumps({'status': 1,
                                                'msg': '修改成功'}))
            else:
                return HttpResponse(json.dumps({'status': 500,
                                                'msg': '没改成功'}))
        except Exception as e:
            print(e)
            return HttpResponse(json.dumps({'status': 500,
                                            'msg': '接口异常'}))


def gaidengji(request):
    phone = request.POST.get('phone', None)
    level = request.POST.get('level', None)
    config = request.POST.get('config', None)
    print(phone, level, config)
    byte_phone = phone.encode('utf-8')
    str_phone = base64.b64encode(byte_phone)
    print(str_phone)
    import pymysql
    if config == '1':
        try:
            conn = pymysql.connect(
                host='47.112.135.201',
                user='root', password='Ysh@#2020',
                database='date',
                charset='utf8')
            cursor = conn.cursor()
            select_sql = 'select id from js_user where mobile=%s and status=1;'
            cursor.execute(select_sql, str_phone)
            user_id = cursor.fetchone()[0]

            sql = "update js_user_detail set link_level=%s where user_id=%s;"
            cursor.execute(sql, [level, user_id])
            conn.commit()
            cursor.close()
            conn.close()
            r = requests.get('https://test-api.51dengta.net/index/sign?sign=2')
            if r.status_code != 200:
                return HttpResponse(json.dumps({'status': 5,
                                                'msg': '更新缓存失败'}))
            return HttpResponse(json.dumps({'status': 1,
                                            'msg': '修改成功'}))
        except Exception as e:
            print(e)
            return HttpResponse(json.dumps({'status': 500,
                                            'msg': '接口异常'}))
    elif config == '2':
        try:
            conn = pymysql.connect(
                host='121.201.57.208',
                user='root', password='Jskj@1234',
                database='date',
                charset='utf8')
            cursor = conn.cursor()
            select_sql = 'select id from js_user where mobile=%s and status=1;'
            cursor.execute(select_sql, str_phone)
            user_id = cursor.fetchone()[0]

            sql = "update js_user_detail set link_level=%s where user_id=%s;"
            cursor.execute(sql, [level, user_id])
            conn.commit()
            cursor.close()
            conn.close()
            r = requests.get('https://dev-api.51dengta.net/index/sign?sign=2')
            if r.status_code != 200:
                return HttpResponse(json.dumps({'status': 5,
                                                'msg': '更新缓存失败'}))
            return HttpResponse(json.dumps({'status': 1,
                                            'msg': '修改成功'}))
        except Exception as e:
            print(e)
            return HttpResponse(json.dumps({'status': 500,
                                            'msg': '接口异常'}))


def zhuboshenhe(request):
    phone = request.POST.get('phone', None)
    # level = request.POST.get('level', None)
    config = request.POST.get('config', None)
    print(phone, config)
    byte_phone = phone.encode('utf-8')
    str_phone = base64.b64encode(byte_phone)
    import pymysql
    if config == '1':
        host_api = 'https://test-api.51dengta.net'
        host_live = 'https://test-live.51dengta.net'
        host_manager = 'https://test-manager.51dengta.net'
        cookie = 'Hm_lvt_02efb315917f62e7f4c7487d430572d9=1617010218; liaoadmin_language=zh-cn; liaohisi_iframe=1; liaohisi_admin_theme=8; tomcat=b70sqsl4cor22geelhak7aq53k'
        mysql_host = '47.112.135.201'
    elif config == '2':
        host_api = 'https://dev-api.51dengta.net'
        cookie = 'Hm_lvt_02efb315917f62e7f4c7487d430572d9=1617010218; liaoadmin_language=zh-cn; PHPSESSID=gmjt5e1c8ur594eg6ocd6e99g7; liaohisi_iframe=1; liaohisi_admin_theme=0'
        mysql_host = '121.201.57.208'
        host_live = 'https://dev-live.51dengta.net'
        host_manager = 'https://dev-manager.51dengta.net'
    elif config == '3':
        cookie = 'liaoadmin_language=zh-cn; PHPSESSID=9lnuhldru4qqh85h4v9o56pghh; liaohisi_iframe=1; liaohisi_admin_theme=default'
        try:
            r1 = requests.post('https://uat-api.51dengta.net/user/auth/smsLogin', json={
                'phone': phone,
                'code': 80008
            })
            time.sleep(0.5)
            token = r1.json()['info']['access_token']
            r = requests.post('https://uat-live.51dengta.net/room/Audit/apply', json={
                'access_token': token,
                'idcard': 'http://51dengta-test.oss-cn-shenzhen.aliyuncs.com/upload/images/geren_touxiang/71247043051a777b5dfb68f1106a35251609832666373.jpeg',
                'idcard_back': 'http://51dengta-test.oss-cn-shenzhen.aliyuncs.com/upload/images/geren_touxiang/a31fc6386ed606b0c4eb253fc05d1bc01609832666659.jpeg',
                'idcard_front': 'http://51dengta-test.oss-cn-shenzhen.aliyuncs.com/upload/images/geren_touxiang/dbe5c8edd712809cc4348e443a386f651609832666576.jpeg',
                'number': '421101297646464649',
                'real_name': '明年'
            })

            time.sleep(0.5)
            r2 = requests.post('https://uat-api.51dengta.net/agent/auth/login', data={
                # 'account': 'yuyuyu',
                'account': '18922871869',
                'password': 'ysh123456'
            })
            daili_token = r2.json()['info']['access_token']
            time.sleep(0.5)
            r3 = requests.post('https://uat-api.51dengta.net/agent/agent/anchorAuditList',
                               data={
                                   "page": 1,
                                   "limit": 10,
                                   "access_token": daili_token
                               })
            zhuboshenhe_id = r3.json()['info']['list'][0]['id']

            time.sleep(0.5)
            r4 = requests.post('https://uat-api.51dengta.net/agent/agent/anchorDeal',
                               data={
                                   "access_token": daili_token,
                                   "id": zhuboshenhe_id,
                                   "type": 2,
                                   "anchor_ratio": "80",
                                   "anchor_p_ratio": "10",
                                   "anchor_end_time": "2021/01/06"
                               })
            time.sleep(0.5)

            r5 = requests.post('http://uat-manager.51dengta.net/admin.php/app/person_anchor/auditedit.html?a=check',
                               data={
                                   'status': 1,
                                   'id': zhuboshenhe_id,
                                   'text': '2021/01/22',
                                   'auth[0]': 1,
                                   'auth[1]': 2
                               }, headers={
                    'cookie': cookie,
                    'x-requested-with': 'XMLHttpRequest',
                    'Host': 'uat-manager.51dengta.net'
                })
            r6 = requests.post('http://uat-manager.51dengta.net/admin.php/app/business/anchorfirst.html?a=add',
                               data={
                                   'phone': phone
                               }, headers={
                    'cookie': cookie,
                    'x-requested-with': 'XMLHttpRequest',
                    'Host': 'uat-manager.51dengta.net'
                })
            r = requests.get('https://uat-api.51dengta.net/index/sign?sign=2')
            print(r5.status_code)
            if r.status_code != 200:
                return HttpResponse(json.dumps({'status': 5,
                                                'msg': '更新缓存失败'}))
            return HttpResponse(json.dumps({'status': 1,
                                            'msg': '修改成功'}))
        except Exception as e:
            print(e)
            return HttpResponse(json.dumps({'status': 500,
                                            'msg': '接口异常'}))
    else:
        host_api = 'https://test-api.51dengta.net'
        host_live = 'https://test-live.51dengta.net'
        host_manager = 'https://test-manager.51dengta.net'
        cookie = 'liaoadmin_language=zh-cn; tomcat=vjtvc7mq1n7hb29tbh7bbdssh0; liaohisi_iframe=1; liaohisi_admin_theme=default'
        mysql_host = '47.112.135.201'

    try:
        r1 = requests.post(host_api + '/user/auth/smsLogin', json={
            'phone': phone,
            'code': 80008
        })
        time.sleep(0.5)
        token = r1.json()['info']['access_token']
        r = requests.post(host_live + '/room/Audit/apply', json={
            'access_token': token,
            'idcard': 'http://51dengta-test.oss-cn-shenzhen.aliyuncs.com/upload/images/geren_touxiang/71247043051a777b5dfb68f1106a35251609832666373.jpeg',
            'idcard_back': 'http://51dengta-test.oss-cn-shenzhen.aliyuncs.com/upload/images/geren_touxiang/a31fc6386ed606b0c4eb253fc05d1bc01609832666659.jpeg',
            'idcard_front': 'http://51dengta-test.oss-cn-shenzhen.aliyuncs.com/upload/images/geren_touxiang/dbe5c8edd712809cc4348e443a386f651609832666576.jpeg',
            'number': '421101297646464649',
            'real_name': '明年'
        })

        time.sleep(0.5)
        r2 = requests.post(host_api + '/agent/auth/login', data={
            # 'account': 'yuyuyu',
            'account': '18922871869',
            'password': 'ysh123456'
        })
        daili_token = r2.json()['info']['access_token']
        time.sleep(0.5)
        r3 = requests.post(host_api + '/agent/agent/anchorAuditList',
                           data={
                               "page": 1,
                               "limit": 10,
                               "access_token": daili_token
                           })
        zhuboshenhe_id = r3.json()['info']['list'][0]['id']

        time.sleep(0.5)
        r4 = requests.post(host_api + '/agent/agent/anchorDeal',
                           data={
                               "access_token": daili_token,
                               "id": zhuboshenhe_id,
                               "type": 2,
                               "anchor_ratio": "80",
                               "anchor_p_ratio": "10",
                               "anchor_end_time": "2021/04/06"
                           })
        time.sleep(0.5)

        r5 = requests.post(host_manager + '/admin.php/app/person_anchor/auditedit.html?a=check',
                           data={
                               'status': 1,
                               'id': zhuboshenhe_id,
                               'text':'2021/04/22',
                               'auth[0]':1,
                               'auth[1]':2
                           }, headers={
                'cookie': cookie,
                'x-requested-with': 'XMLHttpRequest',
                'Host': 'test-manager.51dengta.net'
            })
        print(r5.json())

        conn = pymysql.connect(
            host=mysql_host,
            user='root', password='Ysh@#2020',
            database='date',
            charset='utf8')
        cursor = conn.cursor()
        select_sql = 'select id from js_user where mobile=%s and status=1;'
        cursor.execute(select_sql, str_phone)
        user_id = cursor.fetchone()[0]
        sql = "update js_user set is_identified=1 where id=%s;"
        cursor.execute(sql, [user_id])
        conn.commit()
        cursor.close()
        conn.close()
        r = requests.get(host_api + '/index/sign?sign=2')
        if r5.status_code != 200:
            return HttpResponse(json.dumps({'status': 5,
                                            'msg': '更新缓存失败'}))
        return HttpResponse(json.dumps({'status': 1,
                                        'msg': '修改成功'}))
    except Exception as e:
        print(e)
        return HttpResponse(json.dumps({'status': 500,
                                        'msg': '接口异常'}))

def guizu(request):
    phone = request.POST.get('phone', None)
    level = request.POST.get('level', None)
    config = request.POST.get('config', None)
    print(phone, level, config)
    byte_phone = phone.encode('utf-8')
    str_phone = base64.b64encode(byte_phone)
    print(str_phone)
    import pymysql
    if config == '1':
        try:
            r2 = requests.post('https://test-api.51dengta.net/user/auth/smsLogin', data={
                'phone': phone,
                'code': '80008'
            })
            token = r2.json()['info']['access_token']
            r = requests.post('https://test-api.51dengta.net/user/noble/renew', data={
                'access_token': token,
                'pay_type': '1',
                'noble_id': level,
                'type': '3m',
                'order_src': '1'
            })
            id = r.json()['info']['order_id']
            r1 = requests.post('https://test-api.51dengta.net/pay/test', data={
                'order_id': id, 'access_token': token
            })
            if r1.status_code != 200:
                return HttpResponse(json.dumps({'status': 5,
                                                'msg': '更新缓存失败'}))
            return HttpResponse(json.dumps({'status': 1,
                                            'msg': '修改成功'}))
        except Exception as e:
            print(e)
            return HttpResponse(json.dumps({'status': 500,
                                            'msg': '接口异常'}))
    elif config == '2':
        try:
            r2 = requests.post('https://dev-api.51dengta.net/user/auth/smsLogin', data={
                'phone': phone,
                'code': '80008'
            })
            token = r2.json()['info']['access_token']
            print(r2.json())
            r = requests.post('https://dev-api.51dengta.net/user/noble/renew', data={
                'access_token': token,
                'pay_type': '1',
                'noble_id': level,
                'type': '3m',
                'order_src': '1'
            })
            print(r.json())
            id = r.json()['info']['order_id']
            r1 = requests.post('https://dev-api.51dengta.net/pay/test', data={
                'order_id': id, 'access_token': token
            })
            print(r1.json())
            if r1.status_code != 200:
                return HttpResponse(json.dumps({'status': 5,
                                                'msg': '更新缓存失败'}))
            return HttpResponse(json.dumps({'status': 1,
                                            'msg': '修改成功'}))
        except Exception as e:
            print(e)
            return HttpResponse(json.dumps({'status': 500,
                                            'msg': '接口异常'}))
    elif config == '3':
        try:
            r2 = requests.post('https://uat-api.51dengta.net/user/auth/smsLogin', data={
                'phone': phone,
                'code': '80008'
            })
            token = r2.json()['info']['access_token']
            r = requests.post('https://uat-api.51dengta.net/user/noble/renew', data={
                'access_token': token,
                'pay_type': '1',
                'noble_id': level,
                'type': '3m',
                'order_src': '1'
            })
            id = r.json()['info']['order_id']
            r1 = requests.post('https://uat-api.51dengta.net/pay/test', data={
                'order_id': id, 'access_token': token
            })
            if r1.status_code != 200:
                return HttpResponse(json.dumps({'status': 5,
                                                'msg': '更新缓存失败'}))
            return HttpResponse(json.dumps({'status': 1,
                                            'msg': '修改成功'}))
        except Exception as e:
            print(e)
            return HttpResponse(json.dumps({'status': 500,
                                            'msg': '接口异常'}))


def login(request):
    return render(request, 'login.html')


def diary_login(request):
    print('??????????????????????????????????????????????????')
    return render(request, 'login_diary.html')


def index(request):
    session_user = request.session.get('username', None)
    if session_user is None:
        return render(request, 'login.html')
    return render(request, 'index.html')


def diary_index(request):
    session_user = request.session.get('username', None)
    if session_user is None:
        return render(request, 'login_diary.html')
    return render(request, 'index_diary.html')


def goRegister(request):
    return render(request, 'register.html')


def register(request):
    username = request.POST.get('userName', None)
    password = request.POST.get('password', None)
    query = models.UserInfo.objects.filter(user=str(username))
    if query.__len__() >= 1:
        return HttpResponse(json.dumps({'status': 2,
                                        'msg': '用户已注册'}))
    elif query.__len__() == 0:
        try:
            models.UserInfo.objects.create(user=username, password=password)
            session_username = models.UserInfo.objects.filter(user=username).values()
            request.session['user_id'] = session_username[0]['id']
            request.session['username'] = session_username[0]['user']
            request.session['is_login'] = True
            request.session.set_expiry(30 * 60)
            return HttpResponse(json.dumps({'status': 1,
                                            'msg': '注册成功', 'data': username}))
        except Exception as e:
            return HttpResponse(json.dumps({'status': 3,
                                            'msg': '注册失败'}))


def deleteHistory(request):
    user_id = request.session.get('user_id', None)
    if user_id is None or user_id == '1':
        return HttpResponse(json.dumps({'status': 200, 'msg': '登录超时'}))
    case_id = request.POST.get('caseId', None)
    models.user_body.objects.filter(host_id_id=case_id).update(status=0)
    models.user_host.objects.filter(id=case_id).update(status=0)
    return HttpResponse(json.dumps({'status': 1, 'msg': '操作成功'}))


def x():
    # 查询
    a = models.UserInfo.objects.all()  # 查询所有数据
    print(a)
    b = models.UserInfo.objects.all().values('user')  # 查询user列所有数据
    c = models.UserInfo.objects.all().values_list('id', 'user')  # 取出id和user列，并生成一个列表
    d = models.UserInfo.objects.get(id=1)  # 查询单条？？
    d = models.UserInfo.objects.get(user='yu')
    # 增
    e = models.UserInfo.objects.create(user='yu', password='123456') or models.UserInfo(user='yu', password='123456')
    # 或者
    dic = {'user': 'yu', 'password': '123456'}
    models.UserInfo.objects.create(**dic)
    # 删除
    models.UserInfo.objects.filter(user='yu').delete()
    # 改
    models.UserInfo.objects.filter(user='yu').update(password='12345678')
    # 或者
    s = models.UserInfo.objects.get(user='yu')
    s.pwd = '123456'
    s.save()
    # 获取个数
    models.UserInfo.objects.filter(name='yu').count()
    models.UserInfo.objects.filter(id__gt=1)  # id大于1
    models.UserInfo.objects.filter(id__lt=10)  # ID小于10
    models.UserInfo.objects.filter(id__lt=10, id__gt=1)  # id小于10且id大于1

    # in
    models.UserInfo.objects.filter(id__in=[11, 22, 33])  # in11,22,33
    models.UserInfo.objects.exclude(id__in=[11, 22, 33])  # not in

    # 匹配
    models.UserInfo.objects.filter(user__contains='yu')
    models.UserInfo.objects.filter(user__icontains='yu')
    models.UserInfo.objects.exclude(name__icontains="ven")
    # bettwen and
    models.UserInfo.objects.filter(id__range=[1, 2])  # 范围bettwen and
    # order by
    models.UserInfo.objects.filter(name='seven').order_by('id')
    models.UserInfo.objects.filter(name='seven').order_by('-id')
    # limit
    q = models.UserInfo.objects.all()[10:20]
    # group by
    from django.db.models import Count, Min, Max, Sum
    models.UserInfo.objects.filter(c1=1).values('id').annotate(c=Count('num'))

    # #时间格式的用法
    # #from django.db import models
    # s = models.DatetimeFeild
    # auto_now = True ：则每次更新都会更新这个时间
    # auto_now_add则只是第一次创建添加，之后的更新不再改变。
    # 例如：
    # class UserInfo(models.Model):
    #     name = models.CharField(max_length=32)
    #     ctime = models.DateTimeField(auto_now=True)
    #     uptime = models.DateTimeField(auto_now_add=True)
    # null = True,允许该列为空
    # blank = True 允许admin后台中为空
    '''新增加表中字段时，设置默认值，不会导致表中数据错乱'''
    # #ip
    # ip = models.GenericIPAddressField(protocol="ipv4", null=True, blank=True)
    # #img图片
    # img = models.ImageField(null=True, blank=True, upload_to="upload")

    # 连表
    # 一对多：models.ForeignKey(其他表)
    # 多对多：models.ManyToManyField(其他表)
    # 一对一：models.OneToOneField(其他表)


# -*- coding : utf-8 -*-
# @Auther    : Careslten
# @time      : 2020/12/28 10:36
# @File      : daili.py
# @SoftWare  : dengTa


import requests
import pymysql
import json, time, os

import pymysql


def sql_excute(sql, *args, type='one'):
    data = ''
    try:
        conn = pymysql.connect(
            host='47.112.135.201',
            user='root', password='Ysh@#2020',
            database='date',
            charset='utf8')
        cursor = conn.cursor()
        try:
            if type == 'one':
                cursor.execute(sql, args)
                data = cursor.fetchone()
            elif type == 'all':
                cursor.execute(sql, args)
                data = cursor.fetchall()
                print('232323232323', data)
            else:
                cursor.execute(sql, args)
        except Exception as e:
            print(5, e)
            conn.rollback()
        conn.commit()
        cursor.close()
        conn.close()
        return data
    except Exception as e:
        print(e)


def fetch_upUid(user_id):  # 查询送礼人上级uid
    up_uid = ''
    sql = 'select p_user_id from js_user_link where user_id = %s'
    data = sql_excute(sql, user_id)
    if data == None:
        up_uid = '7619766383'
        print('送礼人上级是等Ta自营代理商')
    else:
        up_uid = data[0]
    return up_uid


def fetch_gift_upUid(uid):  # 查询收礼人上级UId，如果收礼人非代理商，还需要查询上级代理商是谁
    daili_uid = ''
    gift_uid = ''
    sql = 'select p_user_id from js_user_link where user_id = %s'
    data = sql_excute(sql, uid)
    if data == None:
        gift_uid = '7619766383'
        print('收礼人上级是等Ta自营代理商')
    else:
        gift_uid = data[0]
    if_sql = 'select * from js_user_agent where user_id = %s'
    if_data = sql_excute(if_sql, gift_uid)
    if if_data == None:
        daili_sql = 'select agent_user_id from js_user where id = %s'
        datas = sql_excute(daili_sql, gift_uid)
        daili_uid = datas[0]
    else:
        daili_uid = gift_uid
    return gift_uid, daili_uid


def get_terr(uid, gift_uid, daili_uid):  # 查询该代理商分红比例
    fenhong = ''
    shangjifenhong = ''
    shangji = ''
    daili_account = ''
    daili_pwd = ''
    daili_fenc = ''
    dashang_fenc = ''
    r = requests.post(
        'https://test-manager.51dengta.net/admin.php/app/user/agent.html?page=1&limit=1000&field=name&value=&status=-1&signuptime=-1',
        headers={
            'cookie': 'liaoadmin_language=zh-cn; tomcat=9ik17jf418vmv8fq27lm16nflj; liaohisi_iframe=1; liaohisi_admin_theme=default',
            'x-requested-with': 'XMLHttpRequest',
            'Host': 'test-manager.51dengta.net'
        })
    daili_list = r.json()['data']

    for i in daili_list:
        if i['user_id'] == daili_uid:
            daili_account = i['account']
            daili_pwd = i['password']
            daili_fenc = i['agent_ratio']
            dashang_fenc = i['superior_ratio']
    import base64
    pwd = base64.b64decode(daili_pwd).decode("utf-8")
    r1 = requests.post('https://test-api.51dengta.net/agent/auth/login', data={
        'account': daili_account,
        'password': pwd
    })

    daili_token = r1.json()['info']['access_token']

    daili_name = r1.json()['info']['user_info']['nickname']
    r2 = requests.post('https://test-api.51dengta.net/agent/agent/anchorList', data={
        'access_token': daili_token,
        'limit': '1000'
    })
    zhubo_list = r2.json()['info']['list']
    for i in zhubo_list:
        if i['user_id'] == uid:
            fenhong = i['anchor_ratio']
            shangjifenhong = i['anchor_p_ratio']
            shangji = i['pname']
            break

    r3 = requests.post('https://test-api.51dengta.net/agent/agent/separateSet', data={
        'access_token': daili_token
    })
    yonghufenhong = r3.json()['info']['user_ratio']
    yonghushangjifenzhong = r3.json()['info']['user_parent_ratio']
    print('上级名字是：', shangji)
    print('--主播分红', fenhong)
    print('--主播上级分红', shangjifenhong)
    print('--代理商分成', daili_fenc)
    print('--打赏者分成', dashang_fenc)
    print('--用户分成', yonghufenhong)
    print('--用户上级分成', yonghushangjifenzhong)
    print('--代理商名称:', daili_name)
    return fenhong, shangjifenhong, daili_fenc, dashang_fenc, yonghufenhong, yonghushangjifenzhong, daili_name


def sendgift_room(phone=None, uid=None, rid=None):
    if phone == None or uid == None or rid == None:
        phone = str(input('输入送礼者手机号'))
        uid = str(input('输入收礼者uid'))
        rid = str(input('输入房间'))
    r = requests.post('https://test-api.51dengta.net/user/auth/smsLogin', data={
        'phone': phone,
        'code': '80008'
    })
    token = r.json()['info']['access_token']
    user_id = r.json()['info']['user_id']
    r1 = requests.post('https://test-api.51dengta.net/room/room/sendGift', data={
        'id': '10',
        'uid': uid,
        'rid': rid,
        'access_token': token
    })
    if r1.json()['result'] != True:
        return HttpResponse(json.dumps({'status': 500, 'msg': '送花花没有成功', 'error': r1.json()['msg']}))
    # xiaofei = fetch_upUid(user_id)
    # shangji = fetch_gift_upUid(uid)[0]
    # daili = fetch_gift_upUid(uid)[1]
    # fenhong = get_terr(uid,shangji,daili)
    # #计算应有分红
    # gift_num = 100
    # xiaofei_shangji = gift_num/10 * int(fenhong[3]) / 100
    # zhubo_shangji = gift_num/10 * int(fenhong[2]) * int(fenhong[1]) / 100 /100
    # zhubo = gift_num/10 * int(fenhong[2]) * int(fenhong[0]) / 100 / 100
    # dailishang = (gift_num/10 * fenhong[2] / 100) - zhubo_shangji - zhubo
    # print('上级分红:',xiaofei_shangji)
    # print('主播上级分红:', zhubo_shangji)
    # print('主播分红:', zhubo)
    # print('代理商分红:', dailishang)
    xiaofei = fetch_upUid(user_id)
    fetch = fetch_gift_upUid(uid)
    shangji = fetch[0]
    daili = fetch[1]
    fenhong = get_terr(uid, shangji, daili)
    daili_name = fenhong[6]
    # 计算应有分红
    shoulishenfen_sql = 'select link_level from js_user_detail where user_id = %s'
    if_data = sql_excute(shoulishenfen_sql, uid)[0]
    shoulishangji_name_sql = 'select name from js_user where id = %s'
    gift_shoulishangji_name_sql = 'select name from js_user where id = %s'
    try:
        name = sql_excute(shoulishangji_name_sql, xiaofei)[0]
    except Exception as e:
        name = '等Ta自营'

    try:
        gift_name = sql_excute(gift_shoulishangji_name_sql, fetch[0])[0]
    except Exception as e:
        gift_name = '等Ta自营'
    gift_num = 166
    if int(if_data) > 0:
        print('收礼人身份为主播')
        xiaofei_shangji = gift_num / 10 * int(fenhong[3]) / 100
        print('消费者上级分红:', xiaofei_shangji)
        zhubo_shangji = gift_num / 10 * int(fenhong[2]) * int(fenhong[1]) / 100 / 100
        print('收礼者上级分红:', zhubo_shangji, '名字是:{}'.format(gift_name))
        zhubo = gift_num / 10 * int(fenhong[2]) * int(fenhong[0]) / 100 / 100
        print('收礼者分红:', zhubo)
        dailishang = (gift_num / 10 * fenhong[2] / 100) - zhubo_shangji - zhubo
        print('代理商分红:', dailishang, '代理商是：{}'.format(daili_name))
        return {1: '消费上级分红：{}'.format(xiaofei_shangji), 'name': '消费者上级名称:{}'.format(name),
                2: '主播上级分红：{}'.format(zhubo_shangji), 'gift_name': '收礼者上级名称:{}'.format(gift_name),
                3: '收礼人分成:{}'.format(zhubo), 4: '代理分成：{}'.format(dailishang),
                'daili_name': '代理商名称:{}'.format(daili_name)}

    else:
        print('收礼人身份为用户')
        xiaofei_shangji = gift_num / 10 * int(fenhong[3]) / 100
        print('消费者上级分红:', xiaofei_shangji)
        zhubo_shangji = gift_num / 10 * int(fenhong[2]) * int(fenhong[5]) / 100 / 100
        print('收礼者上级分红:', zhubo_shangji, '名字是:{}'.format(name))
        zhubo = gift_num / 10 * int(fenhong[2]) * int(fenhong[4]) / 100 / 100
        print('收礼者分红:', zhubo)
        dailishang = (gift_num / 10 * fenhong[2] / 100) - zhubo_shangji - zhubo
        print('代理商分红:', dailishang, '代理商是：{}'.format(daili_name))
        return {1: '消费上级分红：{}'.format(xiaofei_shangji), 'name': '消费者上级名称:{}'.format(name),
                2: '主播上级分红：{}'.format(zhubo_shangji), 'gift_name': '收礼者上级名称:{}'.format(gift_name),
                3: '收礼人分成:{}'.format(zhubo), 4: '代理分成：{}'.format(dailishang),
                'daili_name': '代理商名称:{}'.format(daili_name)}


def sendgift_msg(phone=None, uid=None):
    if phone == None or uid == None:
        phone = str(input('输入送礼者手机号'))
        uid = str(input('输入收礼者uid'))
    r = requests.post('https://test-api.51dengta.net/user/auth/smsLogin', data={
        'phone': phone,
        'code': '80008'
    })
    token = r.json()['info']['access_token']
    user_id = r.json()['info']['user_id']

    r1 = requests.post('https://test-api.51dengta.net/chat/person/sendGift', data={
        'id': '10',
        'uid': uid,
        'access_token': token
    })
    if r1.json()['result'] != True:
        return HttpResponse(json.dumps({'status': 500, 'msg': '送花花没有成功', 'error': r1.json()['msg']}))

    xiaofei = fetch_upUid(user_id)
    fetch = fetch_gift_upUid(uid)
    shangji = fetch[0]
    daili = fetch[1]
    fenhong = get_terr(uid, shangji, daili)
    daili_name = fenhong[6]
    # 计算应有分红
    shoulishenfen_sql = 'select link_level from js_user_detail where user_id = %s'
    if_data = sql_excute(shoulishenfen_sql, uid)[0]
    shoulishangji_name_sql = 'select name from js_user where id = %s'
    gift_shoulishangji_name_sql = 'select name from js_user where id = %s'
    try:
        name = sql_excute(shoulishangji_name_sql, xiaofei)[0]
    except Exception as e:
        name = '等Ta自营'

    try:
        gift_name = sql_excute(gift_shoulishangji_name_sql, fetch[0])[0]
    except Exception as e:
        gift_name = '等Ta自营'
    gift_num = 166
    if int(if_data) > 0:
        print('收礼人身份为主播')
        xiaofei_shangji = gift_num / 10 * int(fenhong[3]) / 100
        print('消费者上级分红:', xiaofei_shangji)
        zhubo_shangji = gift_num / 10 * int(fenhong[2]) * int(fenhong[1]) / 100 / 100
        print('收礼者上级分红:', zhubo_shangji, '名字是:{}'.format(gift_name))
        zhubo = gift_num / 10 * int(fenhong[2]) * int(fenhong[0]) / 100 / 100
        print('收礼者分红:', zhubo)
        dailishang = (gift_num / 10 * fenhong[2] / 100) - zhubo_shangji - zhubo
        print('代理商分红:', dailishang, '代理商是：{}'.format(daili_name))
        return {1: '消费上级分红：{}'.format(xiaofei_shangji), 'name': '消费者上级名称:{}'.format(name),
                2: '主播上级分红：{}'.format(zhubo_shangji), 'gift_name': '收礼者上级名称:{}'.format(gift_name),
                3: '收礼人分成:{}'.format(zhubo), 4: '代理分成：{}'.format(dailishang),
                'daili_name': '代理商名称:{}'.format(daili_name)}

    else:
        print('收礼人身份为用户')
        xiaofei_shangji = gift_num / 10 * int(fenhong[3]) / 100
        print('消费者上级分红:', xiaofei_shangji)
        zhubo_shangji = gift_num / 10 * int(fenhong[2]) * int(fenhong[5]) / 100 / 100
        print('收礼者上级分红:', zhubo_shangji, '名字是:{}'.format(name))
        zhubo = gift_num / 10 * int(fenhong[2]) * int(fenhong[4]) / 100 / 100
        print('收礼者分红:', zhubo)
        dailishang = (gift_num / 10 * fenhong[2] / 100) - zhubo_shangji - zhubo
        print('代理商分红:', dailishang, '代理商是：{}'.format(daili_name))
        return {1: '消费上级分红：{}'.format(xiaofei_shangji), 'name': '消费者上级名称:{}'.format(name),
                2: '主播上级分红：{}'.format(zhubo_shangji), 'gift_name': '收礼者上级名称:{}'.format(gift_name),
                3: '收礼人分成:{}'.format(zhubo), 4: '代理分成：{}'.format(dailishang),
                'daili_name': '代理商名称:{}'.format(daili_name)}


def sign(request):
    datas = []
    sendgift = ''
    sign = request.GET.get('sign', None)
    phone = request.GET.get('phone', None)
    uid = request.GET.get('uid', None)
    rid = request.GET.get('rid', None)
    times = time.time() * 1000 - 10000
    print(times)
    if sign == '1':
        sendgift = sendgift_msg(phone, uid)
    elif sign == '2':
        sendgift = sendgift_room(phone, uid, rid)
    try:
        sql = 'select CAST(money  AS CHAR),remark from js_account_journal where ctime > %s'
        data = sql_excute(sql, times, type='all')
        for i in data:
            dicts = {}
            dicts['num'] = i[0]
            dicts['name'] = i[1]
            datas.append(dicts)
        if sign == '1':
            return HttpResponse(json.dumps({'status': 1, 'msg': '私聊送花花', 'info': sendgift, 'database': datas}))
        elif sign == '2':
            return HttpResponse(json.dumps({'status': 1, 'msg': '直播间送花花', 'info': sendgift, 'database': datas}))
    except Exception as e:
        print(e)
        return HttpResponse(json.dumps({'status': 500, 'msg': '报错了哥'}))
