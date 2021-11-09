# -*- coding : utf-8 -*-
# @Auther    : Careslten
# @time      : 2021/1/14 17:59
# @File      : tapd.py
# @SoftWare  : onesPro
import time
import datetime
import calendar

import requests
from lxml import etree
from django.http import HttpResponse
from oneGo import models
import json

cookie = '1997160845_35715961_/bugtrace/bugreports/my_view_remember_view=1135715961001002597; ' \
         'is_filter_close=false; ' \
         'tui_filter_fields=%5B%22title%22%2C%22iteration_' \
         'id%22%2C%22priority%22%2C%22status%22%2C%22current_owner%22%5D; ' \
         'bugtrace_reports_myview_35715961_filter_fields=' \
         '%5B%22version_report%22%2C%22module%22%5D; ' \
         'tapdsession=16105058576043263be9301301ca3042b5e6419b0dc3d62e224130334b22c4d7024aa0c0f5; __' \
         'root_domain_v=.tapd.cn; ' \
         '_qddaz=QD.479smn.3d2dr4.kjutm8ch; ' \
         't_u=608927bb4a83e2442d865362931124f66bc36b51b7529d1ea17f0ecf15421a0340a0492f9277259bc4142364429eba28157e49be73731c6c1aa3b507453a52fb72043c06bcf48e5f%7C1; ' \
         't_cloud_login=qc04%40jingshukj.com.cn; _' \
         't_uid=1997160845; _t_crop=38902580; ' \
         'tapd_div=101_4; ' \
         '35715961bug_create_template=1135715961001000063; ' \
         '61770148bug_create_template=0; ' \
         'c_link=0; _' \
         'wt=eyJ1aWQiOiIxOTk3MTYwODQ1IiwiY29tcGFueV9pZCI6IjM4OTAyNTgwIiwiZXhwIjoxNjEwNjE3MjQ1fQ%3D%3D.87b26059e084acfc4cecb4a5f43b52664401e9964dc25956189ee87003323a72; ' \
         'dsc-token=d1sjNclCfGbg3qpL'

def get_yanzhong(cookie,start_time,end_time,project_id):
    r1 = requests.post(
        'https://www.tapd.cn/{}/bugtrace/bugreports/stat_general/general/systemreport-1000000000000000002'.format(project_id),
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
            'Referer': 'https://www.tapd.cn/{}/bugtrace/bugreports/stat_general/general/systemreport-1000000000000000002'.format(project_id),
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


def get_nianling(name,cookie,start_time,end_time,project_id):
    r1 = requests.post(
        'https://www.tapd.cn/{}/bugtrace/bugreports/stat_age/age/systemreport-1000000000000000015'.format(project_id),
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
            'Referer': 'https://www.tapd.cn/{}/bugtrace/bugreports/stat_general/general/systemreport-1000000000000000002'.format(project_id),
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


def get_huigui(cookie,start_time,end_time,project_id):
    r1 = requests.post(
        'https://www.tapd.cn/{}/bugtrace/bugreports/stat_other/regression'.format(project_id),
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
            'Referer': 'https://www.tapd.cn/{}/bugtrace/bugreports/stat_general/general/systemreport-1000000000000000002'.format(project_id),
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

def get_name(cookie,start_time,end_time,project_id):

    url = "https://www.tapd.cn/{}/bugtrace/bugreports/stat_general/general/systemreport-1000000000000000001".format(project_id)
    data = {
        'data[Bugreport][filetype]': 'excel',
        'data[Bugreport][disxAxis]': 'fixer',
        'data[Bugreport][aggregation]': 'user',
        'data[Bugreport][disyAxis]': 'status',
        'data[Bugreport][time_type]': 5,
        'data[Bugreport][time_setting][from]':start_time,
        'data[Bugreport][time_setting][to]': end_time,
        'data[Bugreport][before_value]': 1,
        'data[Bugreport][before_unit]': 'month_before',
        'data[Bugreport][after_unit]': 'today',
        'data[Bugreport][create]': '生成报表',
        'data[Bugreport][title]': '缺陷状态分布图',
        'data[Bugreport][visible_type]': 0,
        'data[Bugreport][id]':'',
        'data[Bugreport][issaveas]':'',
        'data[Bugreport][params0]': 'general',
        'data[Bugreport][params1]': 'systemreport - 1000000000000000001',
        'data[Bugreport][charttype]': 'Column',
        'data[Bugreport][order_type]': 'order_default',
        'data[is_ajax]':'',
        'advanced_condition': {"optionType": "and", "data": [{"fieldLabel": "-+请选择规则+-"}, {"fieldLabel": "-+请选择规则+-"}]},
        'dsc_token': 'GXaIVIFiFsX2K4Nc'
    }
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'sec-ch-ua-mobile': '?0',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'https://www.tapd.cn',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://www.tapd.cn/{}/bugtrace/bugreports/stat_general/general/systemreport-1000000000000000001'.format(project_id),
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': cookie}

    response = requests.request("POST", url, headers=headers, data=data)

    soup = etree.HTML(response.text, etree.HTMLParser())
    # # tr = soup.xpath('//tbody/tr/td[contains(@class,"first-block")]/text()')
    tr = soup.xpath('//*[@id="page-content"]/div[2]/div/div/table/tbody/tr')
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

def get_project(request):
    url = "https://www.tapd.cn/company/my_take_part_in_projects_list?project_id=47855105&t=1629083568127&from=left_tree"
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'sec-ch-ua-mobile': '?0',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'https://www.tapd.cn',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://www.tapd.cn/35715961/bugtrace/bugreports/stat_general/general/systemreport-1000000000000000001',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': cookie}

    response = requests.request("GET", url, headers=headers)
    soup = etree.HTML(response.text, etree.HTMLParser())
    names = soup.xpath('//*[@class="project-name"]')
    ids = soup.xpath('//*[@class="font-public font-public-star  mr-7"]')
    sum = []
    for n,i in zip(names,ids):
        data = {}
        data['name'] = n.text
        data['id'] = i.attrib.get('object-id')
        sum.append(data)
    return HttpResponse(json.dumps({'status': 200,
                                    'data':sum}))


def split_list_by_n(list_collection, n):
    for i in range(0, len(list_collection), n):
        yield list_collection[i: i + n]

def get_last_month_start(month_str=None):
    # 获取上一个月的第一天
    '''
    param: month_str 月份，2021-04
    '''
    # return: 格式 %Y-%m-%d
    if not month_str:
        month_str = datetime.datetime.now().strftime('%Y-%m')
    year, month = int(month_str.split('-')[0]), int(month_str.split('-')[1])
    if month == 1:
        year -= 1
        month = 12
    else:
        month -= 1
    sj = ' 00:00:00'
    return '{}-{}-01{}'.format(year, month,sj)

def get_last_month_end(month_str=None):
    # 获取上一个月的最后一天
    '''
    param: month_str 月份，2021-04
    '''
    # return: 格式 %Y-%m-%d
    if not month_str:
        month_str = datetime.datetime.now().strftime('%Y-%m')
    year, month = int(month_str.split('-')[0]), int(month_str.split('-')[1])
    if month == 1:
        year -= 1
        month = 12
    else:
        month -= 1
    end = calendar.monthrange(year, month)[1]
    sj = ' 00:00:00'
    return '{}-{}-{}{}'.format(year, month, end,sj)

def main(request):
    '''
    :param request: 接口请求内容
    :start_time:搜索开始时间
    :end_time:搜索结束时间
    :name:人名搜索
    :last_month:是否查询近一个月
    :project_id:项目ID
    :return:
    '''
    start_time = request.POST.get('start','')
    end_time = request.POST.get('end','')
    seach_name = request.POST.get('name','')
    last_month = request.POST.get('last_month',False)
    temp_date = datetime.datetime.now()
    project_id = request.POST.get('project_id','35715961')
    now_time = temp_date.strftime("%Y-%m-%d %H:%M:%S")
    if last_month == 'true' or (start_time == '' and end_time == ''):
        start_time = get_last_month_start()
        end_time = get_last_month_end()
    yanzhong = split_list_by_n(get_yanzhong(cookie,start_time,end_time,project_id),7) #按严重程度排列修复人
    huigui = split_list_by_n(get_huigui(cookie,start_time,end_time,project_id), 7)#回归次数，按修复人排列
    all_name = split_list_by_n(get_name(cookie, start_time, end_time, project_id), 10)  # 缺陷状态，修复人攻击
    names = []
    sums = 0
    for i in all_name:
        names.append(i[0])
    datas = []
    yanzhongs = []
    for yan in yanzhong:
        yanzhongs.append(yan)
    huiguis = []
    for hui in huigui:
        huiguis.append(hui)
    for name in names:
        data = {}
        query = split_list_by_n(get_nianling(name,cookie, start_time, end_time, project_id),12)
        lins = []
        for que in query:
            for q in que:
                try:
                    q = int(q)
                    lins.append(q)
                except:continue
        if name in ['空','刘燕芬','余孛','骆小姣','邓小龙']:
            continue
        data['name'] = name
        for y in yanzhongs:
            if y[0] == name:
                data['zongshu'] = y[1]
                data['yiban'] = y[4]
                data['yanzhong'] = y[3]
        for h in huiguis:
            if h[0] == name:
                data['tongguolv'] = h[6]
        data['dayu2tian'] = sum(lins[1:])-lins[5]
        sums += sum(lins[1:])-lins[5]
        if name == '总计':
            data['dayu2tian'] = sums
        datas.append(data)
    seach_data = []
    if seach_name != '':
        for i in datas:
            if i['name'] == seach_name:
                seach_data = [i]
                return HttpResponse(json.dumps({'code': 0, 'count': len(seach_data), 'data': seach_data, 'msg': '操作成功'}))
        return HttpResponse(json.dumps({'code': 0, 'count': 0, 'data': [], 'msg': '操作成功'}))
    return HttpResponse(json.dumps({'code':0,'count':len(datas),'data':datas,'msg':'操作成功'}))
