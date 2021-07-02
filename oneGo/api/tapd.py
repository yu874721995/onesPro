# -*- coding : utf-8 -*-
# @Auther    : Careslten
# @time      : 2021/1/14 17:59
# @File      : tapd.py
# @SoftWare  : onesPro

import requests
from lxml import etree
from django.http import HttpResponse
from oneGo import models
import json

def get_yanzhong(cookie,start_time,end_time):
    r1 = requests.post(
        'https://www.tapd.cn/35715961/bugtrace/bugreports/stat_general/general/systemreport-1000000000000000002',
        data={

            'data[Bugreport][disxAxis]': ' fixer',
            'data[Bugreport][disyAxis]': ' severity',
            'data[Bugreport][time_type]': ' 0',
            'data[Bugreport][time_setting][from]': start_time,
            'data[Bugreport][time_setting][to]': end_time,
            'data[Bugreport][time_setting][count]': ' 1',
            'data[Bugreport][time_setting][type]': ' month',
            'data[Bugreport][create]': ' 生成报表',
            'data[Bugreport][title]': ' 缺陷严重级别分布图',
            'data[Bugreport][id]': '',
            'data[Bugreport][issaveas]': '',
            'data[Bugreport][params0]': ' general',
            'data[Bugreport][params1]': ' systemreport-1000000000000000002',
            'data[Bugreport][charttype]': ' Column',
            'data[Bugreport][order_type]': ' order_default',
            'data[is_ajax]': '',
            'dsc_token': ' bs49C8xbcZKmRliG',
        },
        headers={
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip,deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Length': '847',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': cookie,
            'Host': 'www.tapd.cn',
            'Origin': 'https://www.tapd.cn',
            'Referer': 'https://www.tapd.cn/35715961/bugtrace/bugreports/stat_general/general/systemreport-1000000000000000002',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
        })

    soup = etree.HTML(r1.text, etree.HTMLParser())
    # tr = soup.xpath('//tbody/tr/td[contains(@class,"first-block")]/text()')
    tr = soup.xpath('//tbody/tr')
    our = []
    sum = []
    for i in tr:
        for td in i:
            if td.text != '                                                0                                            ' and len(
                    td.xpath('./a/text()')) != 0:
                our.append(td.xpath('./a/text()')[0].replace(' ', ''))
            else:
                our.append(td.text.replace(' ', ''))
    for i in our:
        sum.append(i.replace('\n', '').replace('\r', ''))
    return sum


def get_nianling(name,cookie,start_time,end_time):
    r1 = requests.post(
        'https://www.tapd.cn/35715961/bugtrace/bugreports/stat_age/age/systemreport-1000000000000000015',
        data={
            'data[Bugreport][status][]': ['new', 'in_progress'],
            # 'data[Bugreport][status][]': 'new',
            'data[Bugreport][time_type]': '0',
            'data[Bugreport][time_setting][from]': start_time,
            'data[Bugreport][time_setting][to]': end_time,
            'data[Bugreport][time_setting][count]': '1',
            'data[Bugreport][time_setting][type]': 'month',
            'data[Bugreport][create_time_type]': '0',
            'data[Bugreport][create_time_setting][from]': start_time,
            'data[Bugreport][create_time_setting][to]': end_time,
            'data[Bugreport][create_time_setting][count]': '1',
            'data[Bugreport][create_time_setting][type]': 'month',
            'data[Bugreport][AgeIntervalNum]': '5',
            'data[Bugreport][AgeTimeInterval]': 'day',
            'fixer_mode_age': '~',
            'fixer_age': name,
            'data[Bugreport][create]': '生成报表',
            'data[Bugreport][title]': '缺陷年龄统计',
            'data[Bugreport][id]': '',
            'data[Bugreport][issaveas]': '',
            'data[Bugreport][params0]': 'age',
            'data[Bugreport][params1]': 'systemreport-1000000000000000015',
            'data[Bugreport][charttype]': 'Column',
            'data[Bugreport][order_type]': 'order_default',
            'data[is_ajax]': '',
            'dsc_token': ' NdAS4gCmBPcbzpZG',
        },
        headers={
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip,deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Length': '847',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': cookie,
            'Host': 'www.tapd.cn',
            'Origin': 'https://www.tapd.cn',
            'Referer': 'https://www.tapd.cn/35715961/bugtrace/bugreports/stat_general/general/systemreport-1000000000000000002',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
        })
    soup = etree.HTML(r1.text, etree.HTMLParser())
    # # tr = soup.xpath('//tbody/tr/td[contains(@class,"first-block")]/text()')
    tr = soup.xpath('//tbody/tr')
    our = []
    sum = []
    for i in tr:
        for td in i:
            if td.text != '                                                0                                            ' and len(
                    td.xpath('./a/text()')) != 0:
                our.append(td.xpath('./a/text()')[0].replace(' ', ''))
            else:
                our.append(td.text.replace(' ', ''))
    for i in our:
        sum.append(i.replace('\n', '').replace('\r', ''))
    return sum


def get_huigui(cookie,start_time,end_time):
    r1 = requests.post(
        'https://www.tapd.cn/35715961/bugtrace/bugreports/stat_other/regression',
        data={
            'data[Bugreport][time_type]': '0',
            'data[Bugreport][time_setting][from]': start_time,
            'data[Bugreport][time_setting][to]': end_time,
            'data[Bugreport][time_setting][count]': '1',
            'data[Bugreport][time_setting][type]': 'month',
            'data[Bugreport][xAxis]': 'fixer',
            'data[Bugreport][create]': '生成报表',
            'data[Bugreport][title]': '缺陷回归分布',
            'data[Bugreport][id]': '',
            'data[Bugreport][issaveas]': '',
            'data[Bugreport][params0]': 'regression',
            'data[Bugreport][params1]': '',
            'data[Bugreport][charttype]': 'Column',
            'data[Bugreport][order_type]': 'order_default',
            'data[is_ajax]': '',
            'dsc_token': 'd1sjNclCfGbg3qpL',
        },
        headers={
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip,deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Length': '847',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': cookie,
            'Host': 'www.tapd.cn',
            'Origin': 'https://www.tapd.cn',
            'Referer': 'https://www.tapd.cn/35715961/bugtrace/bugreports/stat_general/general/systemreport-1000000000000000002',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
        })
    soup = etree.HTML(r1.text, etree.HTMLParser())
    # # tr = soup.xpath('//tbody/tr/td[contains(@class,"first-block")]/text()')
    tr = soup.xpath('//tbody/tr')
    our = []
    sum = []
    for i in tr:
        for td in i:
            if td.text != '                                                0                                            ' and len(
                    td.xpath('./a/text()')) != 0:
                our.append(td.xpath('./a/text()')[0].replace(' ', ''))
            else:
                our.append(td.text.replace(' ', ''))
    for i in our:
        sum.append(i.replace('\n', '').replace('\r', ''))
    return sum


def split_list_by_n(list_collection, n):
    for i in range(0, len(list_collection), n):
        yield list_collection[i: i + n]

# def main(request):
#     start_time = request.POST.get('start',None)
#     end_time = request.POST.get('end',None)
#     if start_time == '' or end_time=='':
#         start_time = '2020-12-01'
#         end_time = '2021-01-10'
#     cookie = '1997160845_35715961_/bugtrace/bugreports/my_view_remember_view=1135715961001002597; is_filter_close=false; tui_filter_fields=%5B%22title%22%2C%22iteration_id%22%2C%22priority%22%2C%22status%22%2C%22current_owner%22%5D; bugtrace_reports_myview_35715961_filter_fields=%5B%22version_report%22%2C%22module%22%5D; tapdsession=16105058576043263be9301301ca3042b5e6419b0dc3d62e224130334b22c4d7024aa0c0f5; __root_domain_v=.tapd.cn; _qddaz=QD.479smn.3d2dr4.kjutm8ch; t_u=608927bb4a83e2442d865362931124f66bc36b51b7529d1ea17f0ecf15421a0340a0492f9277259bc4142364429eba28157e49be73731c6c1aa3b507453a52fb72043c06bcf48e5f%7C1; t_cloud_login=qc04%40jingshukj.com.cn; _t_uid=1997160845; _t_crop=38902580; tapd_div=101_4; 35715961bug_create_template=1135715961001000063; 61770148bug_create_template=0; c_link=0; _wt=eyJ1aWQiOiIxOTk3MTYwODQ1IiwiY29tcGFueV9pZCI6IjM4OTAyNTgwIiwiZXhwIjoxNjEwNjE3MjQ1fQ%3D%3D.87b26059e084acfc4cecb4a5f43b52664401e9964dc25956189ee87003323a72; dsc-token=d1sjNclCfGbg3qpL'
#     yanzhong = split_list_by_n(get_yanzhong(cookie,start_time,end_time),7)
#     huigui = split_list_by_n(get_huigui(cookie,start_time,end_time), 6)
#     # for i in yanzhong:
#     #     print(i)
#     # for i in huigui:
#     #     print(i)
#     # print(yanzhong)
#     yanzhongs = []
#     huiguis = []
#     nianling = {}
#     name = ['魏文彬','石文水','朱宇航','吴斯诺','邱杨琦','李胜锋','詹炼钢','桓成','肖旭辉','魏宏昌','李锡会1','李达文','张春窑']
#     for i in yanzhong:
#         if i[0] in name:
#             yanzhongs.append(i)
#     for i in huigui:
#         if i[0] in name:
#             huiguis.append(i)
#     for x in name:
#         lin = []
#         lin.append(get_nianling(x,cookie,start_time,end_time))
#         nianling[x] = lin
#     for i in nianling.keys():
#         for x in yanzhongs:
#             if i == x[0]:
#                 nianling[i].append(x)
#         for x in huiguis:
#             if i == x[0]:
#                 nianling[i].append(x)
#     datas = []
#     for i in nianling:
#         yanzhong_zhanbi_num = 0
#         dayu2tian_zhanbi_num = 0
#         data = {}
#         try:
#             zongshu = nianling[i][1][1]
#         except Exception as e:
#             print(e)
#             zongshu = '暂无数据'
#         try:
#             yanzhong_zhanbi_num = int(int(nianling[i][1][2]) + int(nianling[i][1][3])) / int(nianling[i][1][1])
#             yanzhong_zhanbi = '{}%'.format(round(yanzhong_zhanbi_num * 100,1))
#         except Exception as e:
#             print(e)
#             yanzhong_zhanbi = '暂无数据'
#
#         try:
#             dayu2tian_zhanbi_num = int(int(nianling[i][0][3])+int(nianling[i][0][4])+int(nianling[i][0][5])) / int(nianling[i][1][1])
#             dayu2tian_zhanbi = '{}%'.format(round(dayu2tian_zhanbi_num * 100, 1))
#         except Exception as e:
#             print(e)
#             dayu2tian_zhanbi = '暂无数据'
#
#         try:
#             tongguolv = nianling[i][2][5]
#         except Exception as e:
#             print(e)
#             tongguolv = '暂无数据'
#         data['name'] = i
#         data['zongshu'] = zongshu
#         data['yanzhong_zhanbi'] = yanzhong_zhanbi
#         data['dayu2tian_zhanbi'] = dayu2tian_zhanbi
#         data['tongguolv'] = tongguolv
#         # print((1-(int(zongshu)/100)) * 100*0.5,'22',(1-yanzhong_zhanbi_num)*100*0.05,'33',(1-dayu2tian_zhanbi_num)*100*0.2,'44',int(tongguolv[:-1])*100*0.25)
#         # print('11',(1-(int(zongshu)/100)) * 100*0.5,'22',(1-yanzhong_zhanbi_num)*100*0.05,'33',(1-dayu2tian_zhanbi_num)*100*0.2,'44',int(tongguolv[:-1])*100*0.25)
#         num1 = (1-(int(zongshu)/100)) * 100*0.5
#         num2 = (1-yanzhong_zhanbi_num)*100*0.05
#         num3 = (1-dayu2tian_zhanbi_num)*100*0.2
#         num4 = int(tongguolv[:-1])*0.25
#         print(num1,num2,num3,num4)
#         num = int(num1) + int(num2) + int(num3)+ int(num4)
#         data['zongfen'] = str(num)
#         datas.append(data)
#     return HttpResponse(json.dumps({'code':0,'count':13,'data':datas,'msg':'操作成功'}))

def main(request):
    start_time = request.POST.get('start',None)
    end_time = request.POST.get('end',None)
    if start_time == '' or end_time=='':
        start_time = '2020-12-18 00:00:00'
        end_time = '2021-01-15 00:00:00'
    cookie = '1997160845_35715961_/bugtrace/bugreports/my_view_remember_view=1135715961001002597; is_filter_close=false; tui_filter_fields=%5B%22title%22%2C%22iteration_id%22%2C%22priority%22%2C%22status%22%2C%22current_owner%22%5D; bugtrace_reports_myview_35715961_filter_fields=%5B%22version_report%22%2C%22module%22%5D; tapdsession=16105058576043263be9301301ca3042b5e6419b0dc3d62e224130334b22c4d7024aa0c0f5; __root_domain_v=.tapd.cn; _qddaz=QD.479smn.3d2dr4.kjutm8ch; t_u=608927bb4a83e2442d865362931124f66bc36b51b7529d1ea17f0ecf15421a0340a0492f9277259bc4142364429eba28157e49be73731c6c1aa3b507453a52fb72043c06bcf48e5f%7C1; t_cloud_login=qc04%40jingshukj.com.cn; _t_uid=1997160845; _t_crop=38902580; tapd_div=101_4; 35715961bug_create_template=1135715961001000063; 61770148bug_create_template=0; c_link=0; _wt=eyJ1aWQiOiIxOTk3MTYwODQ1IiwiY29tcGFueV9pZCI6IjM4OTAyNTgwIiwiZXhwIjoxNjEwNjE3MjQ1fQ%3D%3D.87b26059e084acfc4cecb4a5f43b52664401e9964dc25956189ee87003323a72; dsc-token=d1sjNclCfGbg3qpL'
    yanzhong = split_list_by_n(get_yanzhong(cookie,start_time,end_time),7)
    huigui = split_list_by_n(get_huigui(cookie,start_time,end_time), 6)
    yanzhongs = []
    huiguis = []
    nianling = {}
    name = ['魏文彬','石文水','朱宇航','吴斯诺','邱杨琦','李胜锋','詹炼钢','桓成','肖旭辉','魏宏昌','李锡会1','李达文','张春窑']
    for i in yanzhong:
        if i[0] in name:
            yanzhongs.append(i)
    for i in huigui:
        if i[0] in name:
            huiguis.append(i)
    for x in name:
        lin = []
        lin.append(get_nianling(x,cookie,start_time,end_time))
        nianling[x] = lin
    for i in nianling.keys():
        for x in yanzhongs:
            if i == x[0]:
                nianling[i].append(x)
        for x in huiguis:
            if i == x[0]:
                nianling[i].append(x)
    datas = []
    for i in nianling:
        print(i)
        print(nianling[i])
        data = {}
        zongshu = nianling[i][1][1]
        yiban_num = nianling[i][1][4]
        yanzhong_zhanbi_num = int(int(nianling[i][1][2]) + int(nianling[i][1][3]))
        dayu2tian_zhanbi_num = int(int(nianling[i][0][3])+int(nianling[i][0][4])+int(nianling[i][0][5]))
        tongguolv = nianling[i][2][5]

        data['name'] = i
        data['zongshu'] = zongshu
        data['yiban'] = yiban_num
        data['yanzhong'] = yanzhong_zhanbi_num
        data['dayu2tian'] = dayu2tian_zhanbi_num
        data['tongguolv'] = tongguolv

        datas.append(data)
    return HttpResponse(json.dumps({'code':0,'count':13,'data':datas,'msg':'操作成功'}))
