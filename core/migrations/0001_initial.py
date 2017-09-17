# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-17 19:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=200, unique=True)),
                ('is_alive', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='PDFFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
            ],
        ),
        migrations.AddField(
            model_name='link',
            name='pdf_file',
            field=models.ManyToManyField(to='core.PDFFile'),
        ),
    ]