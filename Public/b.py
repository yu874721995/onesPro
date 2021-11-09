#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@Time    : 2019/8/8 10:37
@Author  : Careslten
@Site    : 
@File    : b.py
@Software: PyCharm
'''

def checkPhone(phone,array_name):
    if phone == '' or phone == None:
        raise ValueError('缺少参数{}'.format(array_name))
    if len(phone) != 11:
        raise ValueError('手机号码长度不正确')
    return

def checkArray(request,**kwargs):
    for array in kwargs.items():
        Array = request.get(array[0],None)
        arrayName = array[0]
        print(Array,arrayName,array[1])
        if array[1] == 'phone':
            checkPhone(Array,arrayName)
        elif array[1] == 'dict':
            if not isinstance(Array,dict):
                raise ValueError('{}参数类型不正确'.format(arrayName))
        elif Array == '' or Array ==None:
            raise ValueError('{}参数不能为空'.format(arrayName))