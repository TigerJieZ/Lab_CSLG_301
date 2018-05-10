# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-05-10 08:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0002_suggest'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, verbose_name='组名')),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='姓名')),
                ('gender', models.CharField(max_length=10, verbose_name='性别')),
                ('birthday', models.DateField(auto_now_add=True, verbose_name='出生年月')),
                ('email', models.EmailField(max_length=254, verbose_name='邮箱')),
                ('password', models.CharField(max_length=10, verbose_name='密码')),
                ('profession', models.CharField(max_length=30, verbose_name='专业')),
                ('academy', models.CharField(max_length=30, verbose_name='学院')),
                ('permission', models.CharField(max_length=10, verbose_name='权限')),
                ('articles', models.ManyToManyField(to='lab.Article')),
            ],
        ),
        migrations.AddField(
            model_name='group',
            name='members',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lab.Member'),
        ),
    ]
