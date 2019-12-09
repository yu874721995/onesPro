#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@Time    : 2019/11/13 14:53
@Author  : Careslten
@Site    : 
@File    : uploadimg.py
@Software: PyCharm
'''
from django.views.decorators.http import require_http_methods
import filetype, hashlib
from one.models import UploadImage
from django.conf import settings
from django.http import HttpResponse
import json

# 上传文件的视图
@require_http_methods(["POST"])
def uploadImage(request):
    # 从请求表单中获取文件对象
    file = request.FILES.get("img", None)
    if not file:  # 文件对象不存在， 返回400请求错误
        return HttpResponse(json.dumps({'msg':'没有文件'}))
    # 图片大小限制
    if not pIsAllowedFileSize(file.size):
        return HttpResponse(json.dumps({'msg':'文件太大'}))
    # 计算文件md5
    md5 = pCalculateMd5(file)
    uploadImg = UploadImage.getImageByMd5(md5)
    if uploadImg:   # 图片文件已存在， 直接返回
        return HttpResponse(json.dumps({'msg':'已存在','url': uploadImg.getImageUrl()}))
    # 获取扩展类型 并 判断
    ext = pGetFileExtension(file)
    if not pIsAllowedImageType(ext):
        return HttpResponse(json.dumps({'msg':'文件类型错误'}))
    # 检测通过 创建新的image对象
    # 文件对象即上一小节的UploadImage模型
    uploadImg = UploadImage()
    uploadImg.filename = file.name
    uploadImg.file_size = file.size
    uploadImg.file_md5 = md5
    uploadImg.file_type = ext
    print(3)
    uploadImg.save()  # 插入数据库
    print(4)
    # 保存 文件到磁盘
    with open(uploadImg.getImagePath(), "wb+") as f:
        # 分块写入
        for chunk in file.chunks():
            f.write(chunk)

    # 记录日志，这一步可有可无，可定制
    # FileLogger.log_info("upload_image", uploadImg, FileLogger.IMAGE_HANDLER)
    print(5)
    try:
        import requests

        response = requests.post(
            'https://api.remove.bg/v1.0/removebg',
            files={'image_file': open(uploadImg.getImagePath(), 'rb')},
            data={'size': 'auto'},
            headers={'X-Api-Key': 'JyA8RC9NpETgGdkmKv73JyyY'},
        )
        if response.status_code == requests.codes.ok:
            with open(uploadImg.getImagePaths(), 'wb') as out:
                out.write(response.content)
        else:
            print("Error:", response.status_code, response.text)
    except Exception as e:
        print(e)
        return HttpResponse(json.dumps({'status':1,"msg":'报错了'}))
    # 返回图片的url以供访问
    return HttpResponse(json.dumps({'status':1,"url": uploadImg.getImageUrl(),'g_url':uploadImg.getImageBgUrl()}))


# 检测文件类型
# 我们使用第三方的库filetype进行检测，而不是通过文件名进行判断
# pip install filetype 即可安装该库
def pGetFileExtension(file):
    rawData = bytearray()
    for c in file.chunks():
        rawData += c
    try:
        ext = filetype.guess_extension(rawData)
        return ext
    except Exception as e:
        # todo log
        return None

# 计算文件的md5
def pCalculateMd5(file):
    md5Obj = hashlib.md5()
    for chunk in file.chunks():
        md5Obj.update(chunk)
    return md5Obj.hexdigest()

# 文件类型过滤 我们只允许上传常用的图片文件
def pIsAllowedImageType(ext):
    if ext in ["png", "jpeg", "jpg","gif"]:
        return True
    return False

# 文件大小限制
# settings.IMAGE_SIZE_LIMIT是常量配置，我设置为10M
def pIsAllowedFileSize(size):
    limit = settings.IMAGE_SIZE_LIMIT
    if size < limit:
        return True
    return False