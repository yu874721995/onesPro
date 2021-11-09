# Generated by Django 2.2.1 on 2021-09-09 18:28

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='app_date',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('app_name', models.CharField(default='', max_length=200)),
                ('app_build', models.CharField(default='', max_length=200)),
                ('app_url', models.CharField(default=1, max_length=200)),
                ('appVersion', models.CharField(default=1, max_length=200)),
                ('appVersionNo', models.CharField(default=1, max_length=200)),
                ('appbuildVersion', models.CharField(default=1, max_length=200)),
                ('app_env', models.CharField(default=1, max_length=10)),
                ('appPro', models.CharField(default=1, max_length=10)),
                ('appxt', models.CharField(default=1, max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Case_report',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('report_name', models.CharField(default='', max_length=200)),
                ('becuxe_id', models.CharField(default='', max_length=200)),
                ('type', models.CharField(default=1, max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='casecp_mk',
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
            name='UploadImage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('filename', models.CharField(default='', max_length=252)),
                ('file_md5', models.CharField(max_length=128)),
                ('file_type', models.CharField(max_length=32)),
                ('file_size', models.IntegerField()),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('updated_at', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'db_table': 'upload_image',
            },
        ),
        migrations.CreateModel(
            name='user_host',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(default=1, max_length=20)),
                ('host', models.CharField(max_length=200)),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('response_body', models.TextField(default='ZZZ', max_length=2000)),
                ('userid', models.IntegerField()),
                ('method', models.CharField(default='post', max_length=20)),
                ('json_body', models.CharField(default='', max_length=200)),
                ('json_header', models.CharField(default='', max_length=200)),
                ('casename', models.CharField(default='暂无名称', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='user_TestCase_host',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(default=1, max_length=20)),
                ('caseName', models.CharField(max_length=200)),
                ('host', models.CharField(max_length=200)),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('userid', models.IntegerField()),
                ('method', models.CharField(default='post', max_length=20)),
                ('subjectionId', models.CharField(default='', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(default=1, max_length=20)),
                ('username', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
                ('sex', models.CharField(default=1, max_length=20)),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('old_login_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('useing', models.CharField(default=1, max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='user_TestCase_body',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(default=1, max_length=20)),
                ('key', models.CharField(max_length=200)),
                ('value', models.TextField(max_length=2000)),
                ('type', models.CharField(default=1, max_length=10)),
                ('host_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='oneGo.user_TestCase_host')),
            ],
        ),
        migrations.CreateModel(
            name='user_Case_Assert',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(default=1, max_length=20)),
                ('Assert_name', models.CharField(default='', max_length=200)),
                ('Assert_text', models.CharField(default='', max_length=200)),
                ('host_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='oneGo.user_TestCase_host')),
            ],
        ),
        migrations.CreateModel(
            name='user_body',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(default=1, max_length=20)),
                ('key', models.CharField(max_length=200)),
                ('value', models.TextField(max_length=2000)),
                ('type', models.CharField(default=1, max_length=10)),
                ('host_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='oneGo.user_host')),
            ],
        ),
    ]
