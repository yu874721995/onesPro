from django.db import models
from datetime import datetime
import django.utils.timezone as timezone
from django.db import models
from datetime import datetime
from django.conf import settings

class UserInfo(models.Model):
    id = models.AutoField(primary_key=True,blank=False)
    status = models.CharField(max_length=20, default=1)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    sex = models.CharField(max_length=20, default=1)
    create_time = models.DateTimeField(default=timezone.now)
    old_login_time = models.DateTimeField(default=timezone.now)
    useing = models.CharField(max_length=20, default=1)
# Create your models here.
class user_host(models.Model):
    id = models.AutoField(primary_key=True,blank=False)
    status = models.CharField(max_length=20,default=1)
    host = models.CharField(max_length=200,blank=False)
    create_date = models.DateTimeField(default=timezone.now)
    response_body = models.TextField(max_length=2000,default='ZZZ')
    userid = models.IntegerField()
    method = models.CharField(max_length=20,default='post')
    json_body = models.CharField(max_length=200, blank=False, default='')
    json_header = models.CharField(max_length=200, blank=False, default='')
    casename = models.CharField(max_length=100,default='暂无名称')

class user_body(models.Model):
    id = models.AutoField(primary_key=True,blank=False)
    status = models.CharField(max_length=20, default=1)
    key = models.CharField(max_length=200,blank=False)
    value = models.TextField(max_length=2000,blank=False)
    host_id = models.ForeignKey('user_host',on_delete=models.CASCADE)
    type = models.CharField(max_length=10,default=1)

class user_TestCase_host(models.Model):
    id = models.AutoField(primary_key=True, blank=False)
    status = models.CharField(max_length=20, default=1)
    caseName = models.CharField(max_length=200, blank=False)
    host = models.CharField(max_length=200, blank=False)
    create_date = models.DateTimeField(default=timezone.now)
    userid = models.IntegerField()
    method = models.CharField(max_length=20, default='post')
    subjectionId = models.CharField(max_length=200, blank=False,default='')

class casecp_mk(models.Model):
    id = models.AutoField(primary_key=True, blank=False)
    status = models.CharField(max_length=20, default=1)
    type = models.CharField(max_length=20, default=1)
    name = models.CharField(max_length=200, blank=False)
    subjection = models.CharField(max_length=20, default='')
    create_date = models.DateTimeField(default=timezone.now)

class user_TestCase_body(models.Model):
    id = models.AutoField(primary_key=True, blank=False)
    status = models.CharField(max_length=20, default=1)
    key = models.CharField(max_length=200, blank=False)
    value = models.TextField(max_length=2000, blank=False)
    host_id = models.ForeignKey('user_TestCase_host', on_delete=models.CASCADE)
    type = models.CharField(max_length=10,default=1)

class user_Case_Assert(models.Model):
    id = models.AutoField(primary_key=True, blank=False)
    status = models.CharField(max_length=20, default=1)
    Assert_name = models.CharField(max_length=200, blank=False,default='')
    Assert_text = models.CharField(max_length=200, blank=False,default='')
    host_id = models.ForeignKey('user_TestCase_host', on_delete=models.CASCADE)

class Case_report(models.Model):
    id = models.AutoField(primary_key=True, blank=False)
    create_date = models.DateTimeField(default=timezone.now)
    report_name = models.CharField(max_length=200, blank=False, default='')
    becuxe_id = models.CharField(max_length=200, blank=False, default='')
    type = models.CharField(max_length=10, blank=False, default=1)

class app_date(models.Model):
    id = models.AutoField(primary_key=True, blank=False)
    create_time = models.DateTimeField(default=timezone.now)
    app_name = models.CharField(max_length=200, blank=False, default='')
    app_build = models.CharField(max_length=200, blank=False, default='')
    app_url = models.CharField(max_length=200, blank=False, default=1)
    appVersion = models.CharField(max_length=200, blank=False, default=1)
    appVersionNo = models.CharField(max_length=200, blank=False, default=1)
    appbuildVersion = models.CharField(max_length=200, blank=False, default=1)
    app_env = models.CharField(max_length=10, blank=False, default=1)
    appPro = models.CharField(max_length=10, blank=False, default=1)
    appxt = models.CharField(max_length=10, blank=False, default=1)

class UploadImage(models.Model):
    class Meta:
        db_table = "upload_image"

    id = models.AutoField(primary_key=True)
    filename = models.CharField(max_length=252, default="")
    file_md5 = models.CharField(max_length=128)
    file_type = models.CharField(max_length=32)
    file_size = models.IntegerField()
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(default=datetime.now)

    # 我们还定义了通过文件md5值获取模型对象的类方法
    @classmethod
    def getImageByMd5(cls, md5):
        try:
            return UploadImage.objects.filter(file_md5=md5).first()
        except Exception as e:
            return None

    # 获取本图片的url，我们可以通过这个url在浏览器访问到这个图片
    # 其中settings.WEB_HOST_NAME 是常量配置，指你的服务器的域名
    # settings.WEB_IMAGE_SERVER_PATH 也是常量配置，指你的静态图片资源访问路径
    # 这些配置项我在Django项目的settings.py文件中进行配置
    def getImageUrl(self):
        filename = self.file_md5 + "." + self.file_type
        url = settings.WEB_HOST_NAME + settings.WEB_IMAGE_SERVER_PATH + filename
        return url
    def getImageBgUrl(self):
        filename = self.file_md5 + "new." + self.file_type
        url = settings.WEB_HOST_NAME + settings.WEB_IMAGE_SERVER_PATH + filename
        return url

    # 获取本图片在本地的位置，即你的文件系统的路径，图片会保存在这个路径下
    def getImagePath(self):
        filename = self.file_md5 + "." + self.file_type
        path = settings.IMAGE_SAVING_PATH + filename
        return path
    def getImagePaths(self):
        filename = self.file_md5 + "new." + self.file_type
        path = settings.IMAGE_SAVING_PATH + filename
        return path

    def __str__(self):
        s = "filename:" + str(self.filename) + " - " + "filetype:" + str(self.file_type) \
            + " - " + "filesize:" + str(self.file_size) + " - " + "filemd5:" + str(self.file_md5)
        return s


