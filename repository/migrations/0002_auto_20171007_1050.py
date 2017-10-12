# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-07 02:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServerRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(null=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': '资产记录表',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='姓名')),
                ('email', models.EmailField(max_length=254, verbose_name='邮箱')),
                ('phone', models.CharField(max_length=32, verbose_name='座机')),
                ('mobile', models.CharField(max_length=32, verbose_name='手机')),
            ],
            options={
                'verbose_name_plural': '用户表',
            },
        ),
        migrations.AddField(
            model_name='serverrecord',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='repository.UserProfile'),
        ),
        migrations.AddField(
            model_name='serverrecord',
            name='server_obj',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ar', to='repository.Server'),
        ),
    ]
