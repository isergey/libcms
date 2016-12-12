# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Party',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contactemail', models.CharField(max_length=255, null=True, verbose_name='\u041a\u043e\u043d\u0442\u0430\u0442\u043d\u044b\u0439 email', blank=True)),
                ('contactperson', models.CharField(max_length=255, null=True, verbose_name='\u041a\u043e\u043d\u0442\u0430\u043a\u0442\u043d\u043e\u0435 \u043b\u0438\u0446\u043e', blank=True)),
                ('endpoint', models.CharField(max_length=255, null=True, verbose_name='\u0422\u043e\u0447\u043a\u0430 \u0434\u043e\u0441\u0442\u0443\u043f\u0430', blank=True)),
                ('hours', models.IntegerField(null=True, verbose_name='\u0427\u0430\u0441\u044b', blank=True)),
                ('minutes', models.IntegerField(null=True, verbose_name='\u041c\u0438\u043d\u0443\u0442\u044b', blank=True)),
                ('name', models.CharField(max_length=255, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435', blank=True)),
                ('notify', models.NullBooleanField()),
                ('status', models.NullBooleanField()),
                ('token', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
                'verbose_name': '\u0421\u0438\u0441\u0442\u0435\u043c\u0430',
                'managed': False,
                'verbose_name_plural': '\u0421\u0438\u0441\u0442\u0435\u043c\u044b',
            },
        ),
    ]
