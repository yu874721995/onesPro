# Generated by Django 2.2.1 on 2020-11-25 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oneGo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_testcase_body',
            name='value',
            field=models.TextField(max_length=2000),
        ),
    ]
