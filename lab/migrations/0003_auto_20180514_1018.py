# Generated by Django 2.0.5 on 2018-05-14 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0002_auto_20180514_1004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='article',
            name='last_modified_time',
            field=models.DateTimeField(auto_now=True, verbose_name='修改时间'),
        ),
    ]
