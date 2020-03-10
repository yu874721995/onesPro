from django.db import models

# Create your models here.
from django.db import models
from datetime import datetime
import django.utils.timezone as timezone


#django 暂时不支持字段注释
class UserInfo(models.Model):#用户表
    id = models.AutoField(primary_key=True,blank=False)
    status = models.CharField('是否禁用',max_length=20, default=1)#是否禁用
    usernikename = models.CharField('用户昵称',max_length=20)
    password = models.CharField('用户密码',max_length=20,default='123456')
    telphone = models.CharField('手机号码',max_length=20,default='')
    sex = models.CharField('性别',max_length=20, default=1)
    headimg = models.CharField('头像',max_length=100, default='/image/default/headimage.png')
    wxopenid = models.CharField('微信openid',max_length=100,default='')
    create_time = models.DateTimeField('创建时间',default=timezone.now)
    old_login_time = models.DateTimeField('最后登录时间',default=timezone.now)

class Comodity_type(models.Model):#商品类型表
    class Meta:
        verbose_name = '商品类型表'
    id = models.AutoField(primary_key=True,blank=False,verbose_name='商品类型id')
    status = models.CharField(max_length=20, default=1,verbose_name='是否禁用 1用 0禁')#是否禁用
    Comodity_type_name = models.CharField(max_length=20,verbose_name='商品类型名称')

class Comcp_mk(models.Model):
    id = models.AutoField(primary_key=True, blank=False)
    status = models.CharField(max_length=20, default=1)
    type = models.CharField(max_length=20, default=1)
    name = models.CharField(max_length=200, blank=False)
    subjection = models.CharField(max_length=20, default='')
    create_date = models.DateTimeField(default=timezone.now)



class Commodity(models.Model):#商品表
    class Meta:
        # 表备注
        verbose_name = "商品表"
    id = models.AutoField(primary_key=True,blank=False,verbose_name='商品id')
    status = models.CharField(max_length=20, default=1, verbose_name='是否禁用 1用 0禁')  # 是否禁用
    Commodity_name = models.CharField(max_length=20,verbose_name='商品名称')
    Comodity_type_id = models.ForeignKey('Comodity_type',on_delete=models.CASCADE,verbose_name='商品类型')
    Comodity_introduction = models.CharField(max_length=200,default='暂无介绍',verbose_name='商品简介')
    Comodity_Specifications = models.CharField(max_length=20,verbose_name='商品规格')
    Commodity_Company = models.CharField(max_length=20,verbose_name='商品计量单位')
    Commodity_money = models.CharField(max_length=20,verbose_name='商品价格')
    Commodity_details = models.TextField(max_length=2000,verbose_name='商品详情')
    create_time = models.DateTimeField(default=timezone.now)
    old_login_time = models.DateTimeField(default=timezone.now)


class Commodity_pic(models.Model):#商品图片表
    class Meta:
        # 表备注
        verbose_name = "商品图片表"
    id = models.AutoField(primary_key=True,blank=False,verbose_name='图片id')
    status = models.CharField(max_length=20, default=1, verbose_name='是否禁用 1用 0禁')  # 是否禁用
    Commodity_id = models.ForeignKey('Commodity',on_delete=models.CASCADE,verbose_name='商品id')
    pic_path = models.CharField(max_length=200,verbose_name='商品图片路径')
    create_time = models.DateTimeField(default=timezone.now)

class Commodity_banner(models.Model):
    id = models.AutoField(primary_key=True, blank=False, verbose_name='记录id')
    status = models.CharField(max_length=20, default=1, verbose_name='是否禁用 1用 0禁')  # 是否禁用
    banner_path = models.CharField(max_length=20, default=1)# banner位置
    banner_pic_path = models.CharField(max_length=200,verbose_name='banner图片路径')









class Diary(models.Model):#日记表
    id = models.AutoField(primary_key=True,blank=False)
    status = models.CharField('是否删除',max_length=20, default=1)
    uid = models.CharField('发布人userid',max_length=20)
    AssociatedPet = models.CharField('关联宠物ID',max_length=20)
    diarytitle = models.CharField('日记标题',max_length=30, default='无标题')
    diaryimage = models.CharField('日记封面',max_length=100, default='/image/default/diaryimage.png')
    diarydetail = models.TextField('日记详情',max_length=1000)
    type = models.CharField('关联用户ID',max_length=20)
    create_time = models.DateTimeField('发布时间',default=timezone.now)
    update_time = models.DateTimeField('最后登录时间',default=timezone.now)

class Adoption_information(models.Model):#领养信息
    id = models.AutoField(primary_key=True,blank=False)
    status = models.CharField('是否删除',max_length=20, default=1)
    uid = models.CharField('发布人userid', max_length=20)
    type = models.CharField('是否官方发布',max_length=20,default=1)
    Adoptionimage = models.CharField('宠物领养封面图片', max_length=50, default='/image/default/adoptionimage.png')
    petname = models.CharField('宠物名称',max_length=20)
    Adoptionpet = models.CharField('宠物类别', max_length=20,default=1)#1狗，2猫
    petage = models.CharField('宠物年龄',max_length=20)
    petsex = models.CharField('宠物性别',max_length=20,default=1)
    petVarieties = models.CharField('宠物品种',max_length=20)
    petcharacter = models.CharField('宠物性格',max_length=20)
    Health = models.CharField('健康情况',max_length=20)
    sterilization = models.CharField('是否绝育',max_length=20,default=1)
    Insectrepellent = models.CharField('是否驱虫',max_length=20,default=1)
    vaccine = models.CharField('是否接种疫苗',max_length=20,default=1)
    petdetail = models.CharField('宠物描述',max_length=200,default=1)
    petimage = models.TextField('宠物图片',max_length=1000,default='null')
    Adoptionarea = models.CharField('领养地区',max_length=200,default=1)
    AdoptionRequirement =  models.CharField('领养要求',max_length=200,default=1)
    create_time = models.DateTimeField('发布时间', default=timezone.now)

class Adoption_intention(models.Model):
    id = models.AutoField(primary_key=True,blank=False)
    AdoptionPetId =  models.CharField('领养宠物ID',max_length=20, default=1)
    uid = models.CharField('意向领养人userid', max_length=20)
    AdoptionMsg = models.CharField('领养说明', max_length=500)
    create_time = models.DateTimeField('提交时间', default=timezone.now)

class PetFiles(models.Model):#宠物档案
    id = models.AutoField(primary_key=True, blank=False)
    ShitOfficer = models.CharField('铲屎官ID', max_length=20)
    PetName = models.CharField('宠物名称', max_length=20)
    PetSex = models.CharField('宠物性别', max_length=20,default=1)
    PetType = models.CharField('宠物类型', max_length=20,default=1)#1狗2猫
    sterilization = models.CharField('是否绝育', max_length=20, default=1)
    sterilizationTime = models.CharField('绝育时间', max_length=20,default='null')
    Petbirth = models.CharField('生日', max_length=20)
    PetToHome = models.CharField('宠物到家日期', max_length=50,default='')
    PetHeadimg = models.CharField('宠物头像', max_length=20,default='/image/default/petheadimage.png')
    create_time = models.DateTimeField('提交时间', default=timezone.now)

class Vaccine_situation(models.Model):
    id = models.AutoField(primary_key=True, blank=False)
    PetId = models.CharField('宠物ID', max_length=20)
    InoculationSite = models.CharField('接种地点', max_length=20)
    Inoculation_time = models.CharField('接种时间', max_length=20)
    InoculationPeople = models.CharField('接种人', max_length=20)
    create_time = models.DateTimeField('提交时间', default=timezone.now)

class Health_records(models.Model):
    id = models.AutoField(primary_key=True, blank=False)
    PetId = models.CharField('宠物ID', max_length=20)
    Symptoms = models.CharField('病状', max_length=200)
    HealthTime = models.CharField('病症周期', max_length=200)
    diseaseName = models.CharField('疾病名称', max_length=200)
    MedicalScheme = models.CharField('医疗方案', max_length=200)
    MedicalLocation = models.CharField('医疗地点', max_length=20)
    doctor = models.CharField('医生名称', max_length=20)
    TreatmentCost = models.CharField('治疗花费', max_length=20)
    SymptomsImage = models.TextField('关联照片',max_length=1000,default='')
    type = models.CharField('是否公开', max_length=200,default=0)
    create_time = models.DateTimeField('提交时间', default=timezone.now)
    update_time = models.DateTimeField('最后更新时间', default=timezone.now)







































