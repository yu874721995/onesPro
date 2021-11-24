import hashlib
import random
import platform

from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
import json, time
import pymysql
from pymysql import OperationalError, ProgrammingError
import oss2
from django.conf import settings
from oneGo import models
import requests

from django.contrib.auth.decorators import login_required
import datetime
import logging

# 获取一个logger对象
logger = logging.getLogger(__name__)

user_list = []


def update(request):
    return render(request, 'update_hl_time.html')
def returnshenhe(request):
    return render(request, 'shenhe.html')
def zhenren(request):
    return render(request, 'zhenren.html')

def look(request):
    return render(request, 'look.html')

def mysql_path(config_value, sql=None, args: list = None, operate = '1'):
    '''
    :param config_value: 环境
    :param sql: sql语句
    :param args: sql语句参数
    :param operate: 操作 1：查询，2：更新，3：插入，4，删除
    :return:
    '''
    if config_value == '1':  # 等他 测试
        host = 'rm-wz9syc23nmy8v2cvc6o.mysql.rds.aliyuncs.com'
        user = 'dengta_php'
        password = 'Ysh@#$2021'
        database = 'testdate'
    elif config_value == '2':  # 等他 dev
        host = '121.201.57.208'
        user = 'root'
        password = 'Ysh@#$2021'
        database = 'chinese_date'
    elif config_value == '3':  # 等他 uat
        host = 'rm-wz9syc23nmy8v2cvc6o.mysql.rds.aliyuncs.com'
        user = 'dengta_php'
        password = 'Ysh@#$2021'
        database = 'predate'
    elif config_value == '4':  # 纯净版 test
        host = 'rm-wz9syc23nmy8v2cvc6o.mysql.rds.aliyuncs.com'
        user = 'dengta_php'
        password = 'Ysh@#$2021'
        database = 'chinese_test_date'
    elif config_value == '5':  # 纯净版 dev
        host = '121.201.57.208'
        user = 'root'
        password = 'Ysh@#$2021'
        database = 'chinese_date'
    elif config_value == '6':  # 纯净版 uat
        host = 'rm-wz9syc23nmy8v2cvc6o.mysql.rds.aliyuncs.com'
        user = 'dengta_php'
        password = 'Ysh@#$2021'
        database = 'chinese_uat_date'
    result = None
    try:
        db = pymysql.connect(
            host=host,
            user=user,
            port=3306,
            password=password,
            database=database,
            charset='utf8')
        cursor = db.cursor()
        try:
            logger.info('执行sql：{}，{}'.format(sql,args))
            cursor.execute(sql, args)
            if operate == '1':
                result = cursor.fetchall()
            else:
                db.commit()
                result = cursor.rowcount
        except:
            db.rollback()
            cursor.close()
            db.close()
            logger.info("sql执行错误")
            raise Exception("sql执行错误")
        cursor.close()
        db.close()
    except OperationalError as e:
        logger.info("数据库连接失败")
        raise Exception("数据库连接失败")
    except ProgrammingError as e:
        logger.info("sql语法错误")
        raise Exception("sql语法错误")
    except Exception as e:
        logger.error("数据库异常:{}".format(str(e)))
        raise Exception("数据库异常:{}".format(str(e)))
    return result

def houtai(config_value):
    url = 'https://test-manager.dengtayiduiyi.com/admin.php/system/publics/index.html'
    if config_value == '4':  # 等他 测试
        url = 'https://test-manager.dengtayiduiyi.com/admin.php/system/publics/index.html'
        user = 'admin'
        paw = '123456'
    elif config_value == '5':
        url = 'https://dev-manager.dengtayiduiyi.com/admin.php/system/publics/index.html'
        user = 'admin'
        paw = '123456'
    elif config_value == '6':
        url = 'https://uat-manager.dengtayiduiyi.com/admin.php/system/publics/index.html'
        user = 'admin'
        paw = '123456'
    r = requests.post(url + '/common/java/updateFollow', data={
        'username': user,
        'password': paw,
        '__token__': 'f68d3a03deb9a9340b653b39123caf0b'
    })
    print(r.text)
def commit(request):
    phone = request.POST.get('phone', None)
    times = str(time.time()).split('.')[0] + '000'
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


def flower_update(request):
    phones = request.POST.get('phones', None)
    coin = request.POST.get('coin', None)
    config = request.POST.get('config', None)
    logger.info('开始修改花花，手机号：{}  数量：{} 环境：{}'.format(phones,coin,config))
    if phones == '':
        return HttpResponse(json.dumps({'status': 500,
                                        'msg': '请输入必填项'}))
    elif phones[0] == 't':
        phones = user_phone(phones, config)

    if config == '7' or config == '8' or config =='9':
        try:
            area_code = phones.split('-')[0]
            phone = phones.split('-')[1]
        except:
            return HttpResponse(json.dumps({'status': 500,
                                            'msg': '手机号码格式为86-1xxxxxxxxxx'}))
        byte_phone = phone.encode('utf-8')
        str_phone = base64.b64encode(byte_phone)
        try:
            sql = "update js_user set coin=%s where mobile=%s and area_code = %s and status=1;"
            mysql_path(config,sql,[coin,str_phone,area_code],'2')
            r = requests.get(url_config(config)+'/index/sign?sign=2')
            if r.status_code != 200:
                return HttpResponse(json.dumps({'status': 5,
                                                'msg': '更新缓存失败'}))
            return HttpResponse(json.dumps({'status': 1,
                                            'msg': '修改成功'}))
        except Exception as e:
            return HttpResponse(json.dumps({'status': 500,
                                            'msg': '接口异常'}))
    try:
        r = requests.post(url_config(config)+'/common/java/updateFollow',data={
            'mobile':phones,
            'follow':coin,
            'password':888888
        })
        if r.json()['result'] == True:
            logger.info('修改成功')
            return HttpResponse(json.dumps({'status': 1,
                                            'msg': '修改成功'}))
        else:
            return HttpResponse(json.dumps({'status': 500,
                                        'msg': '后台接口报错:'+r.json()['msg']}))
    except Exception as e:
        return HttpResponse(json.dumps({'status': 500,
                                        'msg': str(e)}))

def gaidengji(request):
    phone = request.POST.get('phone', None)
    level = request.POST.get('level', None)
    config = request.POST.get('config', None)
    byte_phone = phone.encode('utf-8')
    str_phone = base64.b64encode(byte_phone)
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

def information_gifts(request):
    from_user = request.POST.get('from_user', None)
    to_user = request.POST.get('to_user', None)
    information_gifts_operate = request.POST.get('information_gifts_operate', None)
    information_gifts_num = request.POST.get('information_gifts_num', None)
    information_gifts_config = request.POST.get('information_gifts_config', None)
    if information_gifts_num == '':
        information_gifts_num = 1
    if information_gifts_operate == '1':
        logger.info('进入发消息，发送者：{}  接收者：{} 数量：{}  环境：{}'.format(from_user,to_user,information_gifts_num,information_gifts_config))
    elif information_gifts_operate == '2':
        logger.info('进入送礼物，发送者：{}  接收者：{} 价值：{}  环境：{}'.format(from_user, to_user, information_gifts_num,
                                                             information_gifts_config))
    url = url_config(information_gifts_config)
    phone = user_phone(from_user,information_gifts_config)
    try:
        logger.info('{}充值花花:'.format(phone) + '1000000')
        r = requests.get(url + "/common/java/updateFollow?mobile={}&follow=5000000&password=888888".format(phone))
        if r.json()['result'] == True:
            logger.info('充值成功')
        else:
            logger.error('充值失败')
            return HttpResponse(json.dumps({'status': 500,
                                            'msg': '后台接口报错:' + r.json()['msg']}))
    except Exception as e:
        logger.error('充值出错')
        return HttpResponse(json.dumps({'status': 500,
                                        'msg': str(e)}))
    else:
        try:
            if information_gifts_operate == '1':
                logger.info('批量发消息，入参：发送者{}，接收者{}，数量{}'.format(from_user, to_user, information_gifts_num))
                if len(information_gifts_num) > 3:
                    logger.warning('消息过大')
                    return HttpResponse(json.dumps({'status': 400,
                                                    'msg': '发送失败,消息过大'}))
                for i in range(1,int(information_gifts_num)+1):
                    r = requests.post(url + '/index/sign', data={
                        'sign': '7',
                        'to': to_user,
                        'from': from_user,
                        'msg': i,
                        'ext[message_type]': '2'
                    })

                    if r.text != 'ok':
                        logger.error('发送失败')
                        return HttpResponse(json.dumps({'status': 400,
                                                    'msg': '发送失败'}))
                    else:
                        logger.info('发送成功' + str(i))
            else:
                logger.info('批量送礼物，入参：发送者{}，接收者{}，数量{}'.format(from_user, to_user, information_gifts_num))
                r = requests.post(url + '/user/auth/smsLogin', data={
                    'phone': phone,
                    'code': 80008,  #
                    'version': '2.0.1'
                })
                token = r.json()['info']['access_token']
                r_giftList = requests.get(url + "/room/room/giftList?access_token={}&page=1&limit=200&cate_id=1".format(token))
                gift_dict = {}
                for i in r_giftList.json()['info']['list']:
                    gift_dict[i['coin']] = i['id']
                dict3 = {}
                for i in sorted(gift_dict,reverse=True):
                    dict3[i] = gift_dict[i]
                for key,value in dict3.items():
                    while True:
                        if int(information_gifts_num) - int(key) > 0:
                            information_gifts_num = int(information_gifts_num) - int(key)
                            requests.get(url + "/chat/person/sendGift?access_token={}&id={}&project_id=4&uid={}&version=2.0.1".format(token,value,to_user))
                            logger.info('送礼物，价值：' + str(key) + ' 花花，还需赠送：{}花花'.format(information_gifts_num) )
                            continue
                        elif int(information_gifts_num) - int(key)  < 0:
                            break
                        else:
                            requests.get(
                                url + "/chat/person/sendGift?access_token={}&id={}&project_id=4&uid={}&version=2.0.1".format(
                                    token, value,to_user))
                            logger.info('送礼物，价值：{} 花花，赠送完成'.format(str(key)))
                            return HttpResponse(json.dumps({'status': 200,
                                                            'msg': '成功'}))
        except Exception as e:
            return HttpResponse(json.dumps({'status': 500,
                                            'msg': str(e)}))
        else:
            return HttpResponse(json.dumps({'status': 200,
                                            'msg': '成功'}))

def user_phone(phone_user,config2):
    '''
    :param phone_user: 手机号或id
    :param config2: 环境
    :return:
    '''
    logger.info('转换手机号和id，手机号或id：{} 环境：{}'.format(phone_user,config2))
    phone2_base64 = str(base64.b64encode(phone_user.encode('utf-8')),'utf-8')
    try:
        sql = 'SELECT id FROM js_user WHERE status = 1 and mobile = %s'
        result = mysql_path(config2,sql,phone2_base64)
        if len(result) == 0 :
            sql = 'SELECT mobile FROM js_user WHERE status = 1 and id = %s'
            result = mysql_path(config2, sql, phone_user)
            logger.info(result)
            if result[0] == '':
                return '查询结果为空'
            result2 = str(base64.b64decode(result[0][0]),'utf-8')
            return result2
        else:
            return result[0][0]
    except Exception as e:
        logger.info('服务器错误')
        return '服务器错误'

def url_config(config):
    '''

    :param config:环境
    :return: url
    '''
    if config == '1' :
        return 'https://test-api.51dengta.net'
    elif config == '2':
        return 'https://dev-api.51dengta.net'
    elif config == '3':
        return 'https://uar-api.51dengta.net'
    elif config == '4':
        return 'https://test-api.dengtayiduiyi.com'
    elif config == '5':
        return 'https://dev-api.dengtayiduiyi.com'
    elif config == '6':
        return 'https://uat-api.dengtayiduiyi.com'
    else:
        logger.error('环境输入有误，默认为纯净test')
        return 'https://test-api.dengtayiduiyi.com'

def code(config):
    if config == '1' or config == '4':
        return 80008
    elif config == '2' or config == '3':
        return 80008
    elif config == '1' or config == '4':
        return 80008
    else:
        logger.error('环境输入有误，自动默认为纯净test')
        return 'https://test-api.dengtayiduiyi.com'

def user_id_phone(request):
    phone_user = request.POST.get('selectPhone', None)
    config2 = request.POST.get('selectConfig', None)
    logger.info('查询手机号和id，手机号或id：{} 环境：{}'.format(phone_user,config2))
    if phone_user == '' or config2 == '':
        return HttpResponse(json.dumps({'status': 500,
                                        'msg': '缺少必填'}))

    value = user_phone(phone_user,config2)
    logger.info('查询成功')
    return HttpResponse(json.dumps({'status': 200,
                                     'msg': value}))

def get_agent(request):
    config = request.POST.get('config',None)
    sql = '''
        SELECT
            share_code,
            NAME 
        FROM
            `js_user` 
        WHERE
            is_agent = 1
            and status = 2
            and name != '等他自营'
	'''
    query = mysql_path(config,sql)
    info = list()
    for i in query:
        info.append({'share_code':i[0],'agent_name':i[1]})
    logger.info(info)
    return HttpResponse(json.dumps({'status': 200,
                                     'data': info}))



def auto_registration(request):
    auto_phone = request.POST.get('auto_phone', None)
    auto_sex = request.POST.get('auto_sex', None)
    auto_name = request.POST.get('auto_name', None)
    auto_number = request.POST.get('auto_number', None)
    auto_config = request.POST.get('auto_config', None)
    auto_agent = request.POST.get('auto_agent', None)
    auto_network = request.POST.get('auto_network', None)
    auto_image_if = request.POST.get('auto_image_if', None)
    #阿里云oss配置 勿改
    auth = oss2.Auth('LTAI4GCspfLFXsjouCA1bsNQ', 'dbPk1HGN86fo5WTZCSomHNO9NENM9u')
    bucket = oss2.Bucket(auth, 'https://oss-cn-shenzhen.aliyuncs.com', '51dengta-test')
    oss_path = 'https://51dengta-test.oss-cn-shenzhen.aliyuncs.com'
    logger.info('手机号：{}，性别：{}，昵称：{}，数量：{}，环境:{},代理商的邀请码：{},上级的id：{} '
                .format(auto_phone,auto_sex,auto_name,auto_number,auto_config,auto_agent,auto_network))
    try:
        from Public.b import checkArray
        checkArray(request.POST,auto_phone='phone',auto_config='str')
    except Exception as e:
        return HttpResponse(json.dumps({'status': 500,
                                'msg':str(e)}))
    if auto_network != '':
        sql = 'select share_code FROM js_user where id = %s'
        result = mysql_path(auto_config,sql,auto_network)
        auto_network = result[0]
    else:
        auto_network = auto_agent
    if auto_number == '':
        auto_number = 1
    elif len(auto_number) > 3:
        return HttpResponse(json.dumps({'status': 500,
                                        'msg': '注册数量不允许超过1000'}))
    if auto_name == '':
        ming = '赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜戚谢邹喻柏水窦章云苏潘葛奚范彭郎鲁韦昌马苗凤花方俞任袁柳酆鲍史唐费廉岑薛雷贺倪汤滕殷罗毕郝邬' \
               '安常乐于时傅皮卞齐康伍余元卜顾孟平黄和穆萧尹姚邵湛汪祁毛禹狄米贝明臧计伏成戴谈宋茅庞熊纪舒屈项祝董梁杜阮蓝闵席季麻强贾路娄危江童颜郭梅盛林刁钟徐邱骆高夏蔡田樊胡凌' \
               '霍虞万支柯昝管卢莫经房裘缪干解应宗丁宣贲邓郁单杭洪包诸左石崔吉钮龚程嵇邢滑裴陆荣翁荀羊於惠甄麴家封芮羿储靳汲邴糜松井段富巫乌焦巴弓牧隗山谷车侯宓蓬全郗班仰秋仲伊宫宁仇栾' \
               '暴甘钭厉戎祖武符刘景詹束龙叶幸司韶郜黎蓟薄印宿白怀蒲邰从鄂索咸籍赖卓蔺屠蒙池乔阴欎胥能苍双闻莘党翟谭贡劳逄姬申扶堵冉宰郦雍舄璩桑桂濮牛寿通边扈燕冀郏浦尚农温别庄晏柴瞿阎充慕' \
               '连茹习宦艾鱼容向古易慎戈廖庾终暨居衡步都耿满弘匡国文寇广禄阙东殴殳沃利蔚越夔隆师巩厍聂晁勾敖融冷訾辛阚那简饶空曾毋沙乜养鞠须丰巢关蒯相查後荆红游竺权逯盖益桓公万俟司马上官欧阳夏' \
               '侯诸葛闻人东方赫连皇甫尉迟公羊澹台公冶宗政濮阳淳于单于太叔申屠公孙仲孙轩辕令狐钟离宇文长孙慕容鲜于闾丘司徒司空亓官司寇仉督子车颛孙端木巫马公西漆雕乐正壤驷公良拓跋夹谷宰父谷梁晋楚闫' \
               '法汝鄢涂钦段干百里东郭南门呼延归海羊舌微生岳帅缑亢况后有琴梁丘左丘东门西门商牟佘佴伯赏南宫墨哈谯笪年爱阳佟第五言福百家姓终'
        M = "".join(random.choice(ming) for i in range(4))
        auto_name = M
    elif len(auto_name) > 5:
        return HttpResponse(json.dumps({'status': 500,
                                        'msg': '昵称字符不允许大于5'}))
    url = url_config(auto_config)
    pics = 'https://chinese-dengta.oss-cn-shenzhen.aliyuncs.com/upload/images/geren_touxiang/user_audit.png'
    list_id = []
    times = time.time()
    for i in range(int(auto_number)):
        path = os.path.dirname(os.path.abspath(__file__)) + '/image/{}.jpg'.format(random.randint(1, 10))
        try:
            logger.info('开始注册用户{}'.format(i+1))
            r = requests.post(url+'/user/auth/smsLogin',data={
                'phone': int(auto_phone)+i,
                'code': '80008',
                'version': '2.0.1',
                'share_code':auto_network
            })
            token = r.json()['info']['access_token']
            user_id = r.json()['info']['user_id']
            logger.info('登录成功，手机号：{}'.format(int(auto_phone)+i))
            requests.post(url + '/user/user/completeProfile',data={
                'access_token': token,
                'name': '{}{}'.format(auto_name,i+1),
                'sex': auto_sex,
                'version': '2.0.1'})
            logger.info('完善资料，性别：{}，昵称：{}{}'.format(auto_sex,auto_name,i))
            if auto_sex == '2':
                requests.get(url + '/user/auth/userPhotoAuth?access_token={}&pics={}'.format(token,pics)) # 设置真人认证
                logger.info('设置真人认证')
                tag_list = requests.get(url + '/user/tag/list?access_token={}'.format(token)) # 获取标签列表
                tag = tag_list.json()['info']['list'][0]['items'][0]['id'] #取第一个标签id
                # 设置标签
                requests.post(url + '/user/tag/set',data={
                    'access_token': token,
                    'tag_json': [tag],
                    'version': '2.0.1'})
                logger.info('设置标签 id：{}'.format(tag))
                image_name = str(times) + 'image' + str(i)
                m = hashlib.md5()
                b = image_name.encode(encoding='utf-8')
                m.update(b)
                image_md5 = m.hexdigest()
                image_path = 'upload/fix_image/{}.jpg'.format(image_md5)
                result_image = bucket.put_object_from_file(image_path, path)
                if result_image.status != 200:
                    raise Exception('上传图片失败了', result_image.status)
                image_url = oss_path + '/' + image_path
                # 完善资料
                r = requests.post(url + '/user/user/edit', data={
                    'access_token': token,
                    'avatar': image_url,
                    'birth_year': random.randint(1990, 2000),
                    'height': random.randint(160, 170),
                    'marriage': 1,
                    'place_city_code': '440300',
                    'version': '2.2.1'
                })
                if r.json()['result'] == True:
                    logger.info('完善资料ok')
                else:
                    logger.error('完善资料报错啦')
                # 标签审核通过
                if user_id is not None:
                    try:
                        sql = 'UPDATE js_user_tag_log SET STATUS = 2 WHERE user_id = %s'
                        mysql_path(auto_config,sql,user_id,'2')
                        sql = "insert into js_user_tag_mapping(tag_id,user_id,sex,create_time,ctime) values('60',%s,2,%s,%s);"
                        ctime = int(time.time() * 1000)
                        datetime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                        mysql_path(auto_config,sql,[user_id,datetime,ctime],'3')
                        sql = '''UPDATE js_user_detail SET tag_ids = '[60]' WHERE user_id = %s'''
                        mysql_path(auto_config, sql, user_id, '2')
                        r = requests.post(url + '/index/sign?sign=2')
                        if r.status_code == 200:
                            logger.info('标签审核通过')
                    except Exception as e:
                        logger.error('标签审核报错了'+str(e))
                # 头像审核
                if user_id is not None:
                    try:
                        sql = 'UPDATE js_user_avatar_audit SET STATUS = 1 WHERE user_id = %s'
                        mysql_path(auto_config,sql,user_id,'2')
                        sql = 'UPDATE js_user SET avatar = %s WHERE id = %s'
                        mysql_path(auto_config,sql,[image_url,user_id],'2')
                        logger.info('头像审核通过')
                    except Exception as e:
                        logger.info('头像审核失败')
        except Exception as e:
            logger.error(str(e))
            continue
        else:
            list_id.append(int(auto_phone)+i)
    logger.info('注册完成')
    return HttpResponse(json.dumps({'status': 200,
                                'msg': '成功的手机号：{}'.format(list_id)}))

def income_calculator(request):
    rewarder = request.POST.get('rewarder', None)
    recipient = request.POST.get('recipient', None)
    coin_money = request.POST.get('coin_money', None)
    income_config = request.POST.get('income_config', None)
    isbeibao = request.POST.get('is_beibao', None)
    if rewarder == '' or recipient == '' or coin_money == '':
        return HttpResponse(json.dumps({'status': 500,
                                        'msg': '必填项不能为空'}))
    try:
        rewarder_sql = '''
                    SELECT
                    agent_ratio,
                    superior_ratio,
                    user_ratio,
                    user_parent_ratio 
                FROM
                    js_user u LEFT JOIN js_user_agent a on u.agent_user_id = a.user_id 
                WHERE
                    u.id = %s
		            '''
        recipient_sql = '''
                    SELECT
                    agent_ratio,
                    superior_ratio,
                    user_ratio,
                    user_parent_ratio 
                FROM
                    js_user u LEFT JOIN js_user_agent a on u.agent_user_id = a.user_id 
                WHERE
                    u.id = %s
		            '''
        inbites_sql = '''
                        select * from js_system_config where name = 'invite_contacts_config'
                        '''
        inbites = mysql_path(income_config, inbites_sql)
        inbites = eval(inbites[0][5])
        recipient_user = int(inbites['gift']) / 100#上级礼物流水
        result = mysql_path(income_config,recipient_sql,recipient)
        result = result[0]
        recipient_agent,recipient_its_superior = result[0]/100,result[2]/100
        logger.info('受赏者代理商的分成比例 {} 受赏者上级的分成比例 {} 受赏者代理商用户分成比例 {}'
                    .format(recipient_agent,recipient_user,recipient_its_superior))
        x = float(coin_money) * recipient_agent
        rewarded_income = x * recipient_its_superior  # 受赏者收益
        reward_income = x * recipient_user # 受赏者上级收益
        agent_income = x - rewarded_income - reward_income # 受赏者代理商收益
        logger.info('受赏者收益  {} 受赏者上级收益 {} 受赏者代理商收益 {}'
                    .format(rewarded_income/10,reward_income/10/10,agent_income/10))
        if isbeibao == '1':
            sql = '''
            select * from js_system_config where name = 'pack_config'
            '''
            result = mysql_path(income_config,sql)
            beibao = int(result[0][5]) / 100
            rewarded_income = int(coin_money) * beibao
            return HttpResponse(json.dumps({'status': 200,
                                'msg': '受赏者收益{}元'
                    .format(rewarded_income/10)}))

    except Exception as e:
        return HttpResponse(json.dumps({'status': 500,
                                        'msg': '异常:{}'.format(str(e))}))
    else:
        logger.info('完成')
        return HttpResponse(json.dumps({'status': 200,
                                'msg': '受赏者收益 {} 受赏者上级收益 {} 受赏者代理商收益 {}'
                    .format(rewarded_income/10,reward_income/10,round(agent_income/10,3))}))

def charge_vip(request):
    vip_phone = request.POST.get('vip_phone', None)
    combo = request.POST.get('combo', None)
    vip_config = request.POST.get('vip_config', None)
    if vip_phone == '' or combo == '' or vip_config == '':
        return HttpResponse(json.dumps({'status': 500,
                                        'msg': '缺少必填'}))

    url = url_config(vip_config)
    if combo == '1' or combo == '2' or combo == '3':
        try:
            r1 = requests.post(url + '/user/auth/smsLogin', data={
                'phone': vip_phone,
                'code': '80008',
                'version': '1.7.1'
            })

            token = r1.json()['info']['access_token']
            r2 = requests.post(url + '/user/member/renew', data={
                'access_token': token,
                'pay_type': '1',
                'member_id': combo,
                'order_src': '1'
            })

            id = r2.json()['info']['id']
            r3 = requests.post(url + '/pay/test', data={
                'access_token': token,
                'order_id': id
            })

        except Exception as e:
            return HttpResponse(json.dumps({'status': 500,
                                            'msg': '接口报错 {}'.format(str(e))}))
        else:
            return HttpResponse(json.dumps({'status': 200,
                                            'msg': 'ok'}))
    else:
        return HttpResponse(json.dumps({'status': 500,
                                        'msg': '会员套餐id只能是1，2，3'}))
def diary_login(request):

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

def checkApp(request):
    appPro = request.POST.get('appPro',None)
    appXt = request.POST.get('appXt',None)
    version = request.POST.get('version',None)
    env = request.POST.get('env',None)
    if appPro is None or appXt is None or version is None or env is None:
        return HttpResponse(json.dumps({'status': 400, 'msg': '缺少参数'}))
    querys = models.app_date.objects.filter(appPro__icontains=appPro,appxt__icontains=appXt,appVersion__icontains=version,app_env__icontains=env).order_by('-create_time')
    datas = []
    if not querys.exists():
        return HttpResponse(json.dumps({'status': 300, 'msg': '查询结果为空'}))
    for query in querys:
        if query.id is not None:
            datas.append(
                {
                    'id':query.id,
                    'create_time':query.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'app_build': query.app_build,
                    'app_name': query.app_name,
                    'appVersion': query.appVersion,
                    'app_env': query.app_env,
                    'appVersionNo': query.appVersionNo,
                    'app_url': query.app_url,
                    'appbuildVersion': query.appbuildVersion,
                    'appPro': query.appPro,
                    'appxt':query.appxt
                }
            )
        else:
            print(query.id)
    return HttpResponse(json.dumps({'status': 200, 'msg': '操作成功','data':datas}))



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
import json, time, os



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
    if data is None:
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
    if data is None:
        gift_uid = '7619766383'
        print('收礼人上级是等Ta自营代理商')
    else:
        gift_uid = data[0]
    if_sql = 'select * from js_user_agent where user_id = %s'
    if_data = sql_excute(if_sql, gift_uid)
    if if_data is None:
        daili_sql = 'select agent_user_id from js_user where id = %s'
        datas = sql_excute(daili_sql, gift_uid)
        daili_uid = datas[0]
    else:
        daili_uid = gift_uid
    return gift_uid, daili_uid

def im_history(request):
    fromUser = request.POST.get('fromUser',None)
    touser = request.POST.get('toUser','')
    startTime = request.POST.get('startTime',None)
    endTime = request.POST.get('endTime',None)
    if fromUser == None:
        fromUser = ''
    if touser == None:
        touser = ''
    if startTime == None or startTime == '':
        startTime = int(time.time()) - 864000
    if startTime != None and startTime != '':
        startTime = int(time.mktime(time.strptime(startTime, "%Y-%m-%d %H:%M:%S"))) * 1000
    if endTime != None and endTime != '':
        endTime = int(time.mktime(time.strptime(endTime, "%Y-%m-%d %H:%M:%S"))) * 1000
    if fromUser == None:
        fromUser = ''
    if touser == None:
        touser = ''
    url = 'http://8.129.1.206:15601/api/console/proxy?path=_search&method=POST'
    datas = []
    headers = {
        'Accept': 'text/plain, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Authorization': 'Basic a2liYW5hOkZGREVXZGs4MjA5bCpvZWFh',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Length': '0',
        'Host': '8.129.1.206:15601',
        'kbn-version': '6.8.1',
        'Origin': 'http://8.129.1.206:15601',
        'Pragma': 'no-cache',
        'Referer': 'http://8.129.1.206:15601/app/kibana',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
    }
    data = {"version": True, "size": 500, "sort": [{"@timestamp": {"order": "desc", "unmapped_type": "boolean"}}],
            "_source": {"excludes": []}, "aggs": {"2": {
            "date_histogram": {"field": "@timestamp", "interval": "1m", "time_zone": "Asia/Shanghai",
                               "min_doc_count": 1}}}, "stored_fields": ["*"], "script_fields": {},
            "docvalue_fields": [{"field": "@timestamp", "format": "date_time"}], "query": {"bool": {
            "must": [{"range": {"@timestamp": {"gte": int(startTime), "lte": int(endTime), "format": "epoch_millis"}}}],
            "filter": [{"bool": {
                "filter": [{"multi_match": {"type": "best_fields", "query": "00push00", "lenient": True}}, {"bool": {
                    "filter": [
                        {"multi_match": {"type": "phrase", "query": "'fromAccount' => '{}'".format(fromUser), "lenient": True}},
                        {"multi_match": {"type": "phrase", "query": "'to' => '{}',".format(touser), "lenient": True}}]}}]}}],
            "should": [], "must_not": []}},
            "highlight": {"pre_tags": ["@kibana-highlighted-field@"], "post_tags": ["@/kibana-highlighted-field@"],
                          "fields": {"*": {}}, "fragment_size": 2147483647}, "timeout": "30000ms"}
    r = requests.post(url, json=data, headers=headers)
    for i in r.json()['hits']['hits']:
        try:
            print(i['_source']['message'])
            from_nick = i['_source']['message'].split("'fromNick' => '")[1].split("',")[0]
            from_user = i['_source']['message'].split("'fromAccount' => '")[1].split("',")[0]
            to_user = i['_source']['message'].split("'to' => '")[1].split("',")[0]
            text = i['_source']['message'].split("'body' => '")[1].split("',")[0]
            times = time.strftime("%Y--%m--%d %H:%M:%S", time.localtime(int(i['sort'][0])/1000))

            datas.append({'from_nick':from_nick,'from_user':from_user,'to_user':to_user,'text':text,'time':times,})
        except Exception as e:
            print(str(e))
            continue
    return HttpResponse(json.dumps({'status': 200, 'msg': '操作成功','data':datas}))


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


from apscheduler.schedulers.background import BackgroundScheduler #定时任务在后台运行
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
try:
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    @register_job(scheduler, "interval", seconds=120)
    def test_job():
        work()
    @register_job(scheduler, "interval", seconds=600)
    def dingding_job():
        shenhe()
    register_events(scheduler)
    # 启动定时器
    scheduler.start()
except Exception as e:
    raise BaseException('定时任务异常：%s' % str(e))

def uplaod_app(type,xt,times,pro_name,filename):
    pyger = {'test': {'uKey': 'c3e8e43d6d9abf36f9ecd0ea8f9d6db6', '_api_key': '18a30c4f4ae04c3743c863aafe150992', 'name': '测试'},
             'master': {'uKey': '01b58cc2ad38a6dd650fa600ce51cc13', '_api_key': 'e87b4ef54b1d6a2205e71d258b1eae37', 'name': '正式'},
             'uat': {'uKey': '49243a7db33cbeaed834593a19d1540b', '_api_key': '8c4de0575589f2431a85a9a7ea13611c', 'name': '预发布'}}
    ukey = pyger[type]['uKey']
    _api_key = pyger[type]['_api_key']
    r =requests.post('https://upload.pgyer.com/apiv1/app/upload',data={
        'uKey':ukey,
        '_api_key':_api_key,
        'installType':'1',
    },files={'file':open(filename,'rb')})
    url = r.json()['data']['appQRCodeURL']
    build = r.json()['data']['appVersionNo']
    appVersion = r.json()['data']['appVersion']
    appVersionNo = r.json()['data']['appVersionNo']
    appbuildVersion = r.json()['data']['appBuildVersion']
    if xt == 'Android':
        Version = r.json()['data']['appVersion']
    else:
        Version = r.json()['data']['appVersionNo']
    # 调用钉钉机器人接口发送消息
    headers = {"Content-Type": "application/json"}
    data = {
        'msgtype': 'markdown',
        'markdown': {
            'title': '{}新安装包'.format(times),
            'text': r"#### ...下面是{}--{}--{}--{}环境最新{}安装包二维码... ![screenshot]({})".format(
                pro_name, times, Version, pyger[type]['name'], xt, url)
        },
        'at': {
            "atMobiles": ['15989510396', '13434435107'], 'isAtAll': True
        }
    }
    r2 = requests.post(
        'https://oapi.dingtalk.com/robot/send?access_token=afb093a2e7bc0c64947a2a46d193c21347e1ffc609fac83dcd9d940083a9cd6f',
        data=json.dumps(data), headers=headers)
    if r2.status_code != 200:
        raise LookupError('钉钉消息发送失败')
    print('发送消息成功......')
    dic = {'app_name':filename,
           'app_build': build,
           'app_url':url,
           'appVersion':appVersion,
           'appVersionNo':appVersionNo,
           'appbuildVersion':appbuildVersion,
           'app_env':type,
           'appPro':pro_name,
           'appxt':xt}
    models.app_date.objects.create(**dic)


def work():
    import platform
    if platform.system() == 'Linux':
        return
    file_path = 'Z:\测试部\\app\\'
    # file_path = '/smb/测试部/app/'
    times = time.strftime("%Y%m%d", time.localtime())
    for pro_name in ['等Ta','TaTaLive','纯净版']:
        type = ['test','uat','master','dev']
        for i in type:
            filenames = file_path+'{}\{}\{}'.format(pro_name,i,times)
            file_exist = os.path.isdir(filenames)
            exist = '是' if file_exist ==True else '否'
            # print('文件夹名称：{}'.format(filenames))
            # print('检测是否存在{}今日{}{}新文件夹:'.format(pro_name,times,i),exist)
            if file_exist:
                for dirpath, dirnames, files in os.walk(filenames):
                    for filename in files:
                        if filename == '.DS_Store':
                            continue
                        filename = file_path + '{}\{}\{}\{}'.format(pro_name, i, times, filename)
                        querys = models.app_date.objects.filter(app_name__contains=filename)
                        if querys.exists():
                            logger.info('所有安装包已上传')
                            continue
                        azb = filename[-3:]
                        xt = 'IOS' if azb == 'ipa' else 'Android'
                        logger.info('检测到有{}新{}环境{}安装包:{}'.format(pro_name,i,xt, filename))
                        # 上传蒲公英
                        try:
                            uplaod_app(i,xt,times,pro_name,filename)
                        except Exception as e:
                            logger.error('上传失败：{}'.format(str(e)))
                            continue

def auth_msg(request):
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    chrome_options = Options()
    chrome_options.add_argument('--window-size=1366,768')
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get('http://8.129.1.206:15601/app/kibana#/home?_g=()')
    print(driver.title)
    return HttpResponse(json.dumps({'status': 500, 'msg': '报错了哥'}))

import requests,time
def shenhe():
    times = time.strftime("%H", time.localtime())
    if int(times) >= 23 or int(times) <= 9:
        return
    r = requests.Session()
    r.headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    'cookie': settings.SHENHE_COOKIE,
               'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
                 'x-requested-with':'XMLHttpRequest'
                 }
    try:
        rt = r.post('https://manager.dengtayiduiyi.com/admin.php/app/user/avataraudit.html?page=1&limit=10', data={
            'status': 1
        })
        rt.json()
    except:
        get_houtai_cookie()
        logger.info('跳过dingding-job')
        return

    rd = r.post('https://manager.dengtayiduiyi.com/admin.php/app/content_audit/moments.html',data={
        'status':1
    })
    rx = r.post('https://manager.dengtayiduiyi.com/admin.php/app/photo/audit.html',data={
        'status':2
    })
    now_time = datetime.datetime.now()
    new_time = now_time.strftime('%Y-%m-%d %H:%M:%S')
    yes_time = now_time + datetime.timedelta(days=-1)
    old_time = yes_time.strftime('%Y-%m-%d %H:%M:%S')
    rb = r.post('https://manager.dengtayiduiyi.com/admin.php/app/content_audit/userrealauth.html', data={
            'datetime_start': old_time,
            'datetime_end': new_time
        })#真人认证
    rq = r.post('https://manager.dengtayiduiyi.com/admin.php/app/user/checktag.html',data={
        'pass_status':1
    })#标签
    rz = r.post('https://manager.dengtayiduiyi.com/admin.php/app/greet/index.html?page=1&limit=10&field=1&name=&status=-1&datetime_start=&datetime_end=&agent_user_id=0')

    # # 调用钉钉机器人接口发送消息
    text = '有{}个头像未审核  \n'.format(len(rt.json()['data'])) + \
               "有{}条动态未审核  \n".format(len(rd.json()['data'])) + \
               '有{}个相册未审核  \n'.format(len(rx.json()['data'])) + \
               '有{}个标签未审核  \n'.format(len(rq.json()['data'])) + \
               '有{}条招呼未审核  \n'.format(len(rz.json()['data'])) + \
                '最近24小时有{}条真人认证  \n'.format(len(rb.json()['data']))

    data = {
            'msgtype': 'markdown',
            'markdown': {
                'title': '审核来了，兄弟姐妹们',
                'text':"## 有新的审核哟 \n>" + "{}" "[其他审核]({})=====[真人认证审核]({})".format(text,'http://121.201.57.207:9001/shenhe','http://121.201.57.207:9001/zhenren')
            },
            'at': {
                "atMobiles": ['15989510396', '13434435107'], 'isAtAll': True
            }
        }
    if len(rt.json()['data']) == 0 and len(rd.json()['data']) == 0 and len(rx.json()['data']) == 0  and len(rq.json()['data']) == 0:
        data = {
            'msgtype': 'markdown',
            'markdown': {
                'title': '没有任何审核信息',
                'text': r"没有任何审核信息 耶~"
            },
            'at': {
                "atMobiles": ['15989510396', '13434435107'], 'isAtAll': True
            }
        }
    headers = {"Content-Type": "application/json"}
    r2 = requests.post(
        'https://oapi.dingtalk.com/robot/send?access_token=4040d62948003fe61428082409aee12723d35c9fd1296277fb10056c88230aa7',
        data=json.dumps(data), headers=headers)
    if r2.status_code != 200:
        raise LookupError('钉钉消息发送失败')

def get_houtai_cookie():
    from selenium.webdriver import Chrome
    from selenium.webdriver.chrome.options import Options

    DRIVER_PATH = '/usr/chromedriver/chromedriver'
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')  # 无头参数
    options.add_argument('--disable-gpu')
    # 启动浏览器
    if 'Linux' in platform.system():
        driver = Chrome(executable_path=DRIVER_PATH, options=options)
    else:
        driver = Chrome(options=options)
    # 访问目标URL
    driver.get('https://manager.dengtayiduiyi.com/admin.php/system/index/index.html')
    driver.find_element_by_xpath('//input[@placeholder="登录账号"]').send_keys('yunying09')
    driver.find_element_by_xpath('//input[@placeholder="登录密码"]').send_keys('Ysh@1234')
    driver.find_element_by_class_name('layui-btn.layui-btn-normal').click()
    cookie = driver.get_cookies()
    driver.close()
    driver.quit()
    for i in cookie:
        if len(i['value']) > 5:
            settings.PHPSESSID = i['value']