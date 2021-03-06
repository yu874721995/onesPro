# Generated by Django 2.2.1 on 2020-08-31 10:15

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Adoption_information',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(default=1, max_length=20, verbose_name='是否删除')),
                ('uid', models.CharField(max_length=20, verbose_name='发布人userid')),
                ('type', models.CharField(default=1, max_length=20, verbose_name='是否官方发布')),
                ('Adoptionimage', models.CharField(default='/image/default/adoptionimage.png', max_length=50, verbose_name='宠物领养封面图片')),
                ('petname', models.CharField(max_length=20, verbose_name='宠物名称')),
                ('Adoptionpet', models.CharField(default=1, max_length=20, verbose_name='宠物类别')),
                ('petage', models.CharField(max_length=20, verbose_name='宠物年龄')),
                ('petsex', models.CharField(default=1, max_length=20, verbose_name='宠物性别')),
                ('petVarieties', models.CharField(max_length=20, verbose_name='宠物品种')),
                ('petcharacter', models.CharField(max_length=20, verbose_name='宠物性格')),
                ('Health', models.CharField(max_length=20, verbose_name='健康情况')),
                ('sterilization', models.CharField(default=1, max_length=20, verbose_name='是否绝育')),
                ('Insectrepellent', models.CharField(default=1, max_length=20, verbose_name='是否驱虫')),
                ('vaccine', models.CharField(default=1, max_length=20, verbose_name='是否接种疫苗')),
                ('petdetail', models.CharField(default=1, max_length=200, verbose_name='宠物描述')),
                ('petimage', models.TextField(default='null', max_length=1000, verbose_name='宠物图片')),
                ('Adoptionarea', models.CharField(default=1, max_length=200, verbose_name='领养地区')),
                ('AdoptionRequirement', models.CharField(default=1, max_length=200, verbose_name='领养要求')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='发布时间')),
            ],
        ),
        migrations.CreateModel(
            name='Adoption_intention',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('AdoptionPetId', models.CharField(default=1, max_length=20, verbose_name='领养宠物ID')),
                ('uid', models.CharField(max_length=20, verbose_name='意向领养人userid')),
                ('AdoptionMsg', models.CharField(max_length=500, verbose_name='领养说明')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='提交时间')),
            ],
        ),
        migrations.CreateModel(
            name='Comcp_mk',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(default=1, max_length=20)),
                ('type', models.CharField(default=1, max_length=20)),
                ('name', models.CharField(max_length=200)),
                ('subjection', models.CharField(default='', max_length=20)),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Commodity',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='商品id')),
                ('status', models.CharField(default=1, max_length=20, verbose_name='是否禁用 1用 0禁')),
                ('Commodity_name', models.CharField(max_length=20, verbose_name='商品名称')),
                ('Comodity_introduction', models.CharField(default='暂无介绍', max_length=200, verbose_name='商品简介')),
                ('Comodity_Specifications', models.CharField(max_length=20, verbose_name='商品规格')),
                ('Commodity_Company', models.CharField(max_length=20, verbose_name='商品计量单位')),
                ('Commodity_money', models.CharField(max_length=20, verbose_name='商品价格')),
                ('Commodity_details', models.TextField(max_length=2000, verbose_name='商品详情')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('old_login_time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': '商品表',
            },
        ),
        migrations.CreateModel(
            name='Commodity_banner',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='记录id')),
                ('status', models.CharField(default=1, max_length=20, verbose_name='是否禁用 1用 0禁')),
                ('banner_path', models.CharField(default=1, max_length=20)),
                ('banner_pic_path', models.CharField(max_length=200, verbose_name='banner图片路径')),
            ],
        ),
        migrations.CreateModel(
            name='Comodity_type',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='商品类型id')),
                ('status', models.CharField(default=1, max_length=20, verbose_name='是否禁用 1用 0禁')),
                ('Comodity_type_name', models.CharField(max_length=20, verbose_name='商品类型名称')),
            ],
            options={
                'verbose_name': '商品类型表',
            },
        ),
        migrations.CreateModel(
            name='Diary',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(default=1, max_length=20, verbose_name='是否删除')),
                ('uid', models.CharField(max_length=20, verbose_name='发布人userid')),
                ('AssociatedPet', models.CharField(max_length=20, verbose_name='关联宠物ID')),
                ('diarytitle', models.CharField(default='无标题', max_length=30, verbose_name='日记标题')),
                ('diaryimage', models.CharField(default='/image/default/diaryimage.png', max_length=100, verbose_name='日记封面')),
                ('diarydetail', models.TextField(max_length=1000, verbose_name='日记详情')),
                ('type', models.CharField(max_length=20, verbose_name='关联用户ID')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='发布时间')),
                ('update_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='最后登录时间')),
            ],
        ),
        migrations.CreateModel(
            name='Health_records',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('PetId', models.CharField(max_length=20, verbose_name='宠物ID')),
                ('Symptoms', models.CharField(max_length=200, verbose_name='病状')),
                ('HealthTime', models.CharField(max_length=200, verbose_name='病症周期')),
                ('diseaseName', models.CharField(max_length=200, verbose_name='疾病名称')),
                ('MedicalScheme', models.CharField(max_length=200, verbose_name='医疗方案')),
                ('MedicalLocation', models.CharField(max_length=20, verbose_name='医疗地点')),
                ('doctor', models.CharField(max_length=20, verbose_name='医生名称')),
                ('TreatmentCost', models.CharField(max_length=20, verbose_name='治疗花费')),
                ('SymptomsImage', models.TextField(default='', max_length=1000, verbose_name='关联照片')),
                ('type', models.CharField(default=0, max_length=200, verbose_name='是否公开')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='提交时间')),
                ('update_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='最后更新时间')),
            ],
        ),
        migrations.CreateModel(
            name='PetFiles',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ShitOfficer', models.CharField(max_length=20, verbose_name='铲屎官ID')),
                ('PetName', models.CharField(max_length=20, verbose_name='宠物名称')),
                ('PetSex', models.CharField(default=1, max_length=20, verbose_name='宠物性别')),
                ('PetType', models.CharField(default=1, max_length=20, verbose_name='宠物类型')),
                ('sterilization', models.CharField(default=1, max_length=20, verbose_name='是否绝育')),
                ('sterilizationTime', models.CharField(default='null', max_length=20, verbose_name='绝育时间')),
                ('Petbirth', models.CharField(max_length=20, verbose_name='生日')),
                ('PetToHome', models.CharField(default='', max_length=50, verbose_name='宠物到家日期')),
                ('PetHeadimg', models.CharField(default='/image/default/petheadimage.png', max_length=20, verbose_name='宠物头像')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='提交时间')),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(default=1, max_length=20, verbose_name='是否禁用')),
                ('usernikename', models.CharField(max_length=20, verbose_name='用户昵称')),
                ('password', models.CharField(default='123456', max_length=20, verbose_name='用户密码')),
                ('telphone', models.CharField(default='', max_length=20, verbose_name='手机号码')),
                ('sex', models.CharField(default=1, max_length=20, verbose_name='性别')),
                ('headimg', models.CharField(default='/image/default/headimage.png', max_length=100, verbose_name='头像')),
                ('wxopenid', models.CharField(default='', max_length=100, verbose_name='微信openid')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('old_login_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='最后登录时间')),
            ],
        ),
        migrations.CreateModel(
            name='Vaccine_situation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('PetId', models.CharField(max_length=20, verbose_name='宠物ID')),
                ('InoculationSite', models.CharField(max_length=20, verbose_name='接种地点')),
                ('Inoculation_time', models.CharField(max_length=20, verbose_name='接种时间')),
                ('InoculationPeople', models.CharField(max_length=20, verbose_name='接种人')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='提交时间')),
            ],
        ),
        migrations.CreateModel(
            name='Commodity_pic',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='图片id')),
                ('status', models.CharField(default=1, max_length=20, verbose_name='是否禁用 1用 0禁')),
                ('pic_path', models.CharField(max_length=200, verbose_name='商品图片路径')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('Commodity_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='xcx.Commodity', verbose_name='商品id')),
            ],
            options={
                'verbose_name': '商品图片表',
            },
        ),
        migrations.AddField(
            model_name='commodity',
            name='Comodity_type_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='xcx.Comodity_type', verbose_name='商品类型'),
        ),
    ]
