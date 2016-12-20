# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('extsystems', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationTime',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hours', models.IntegerField(default=0, verbose_name='\u0427\u0430\u0441\u044b', validators=[django.core.validators.MinValueValidator(limit_value=0), django.core.validators.MaxValueValidator(limit_value=23)])),
                ('minutes', models.IntegerField(default=0, verbose_name='\u041c\u0438\u043d\u0443\u0442\u044b', validators=[django.core.validators.MinValueValidator(limit_value=0), django.core.validators.MaxValueValidator(limit_value=59)])),
                ('party', models.ForeignKey(to='extsystems.Party')),
            ],
            options={
                'verbose_name': '\u0412\u0440\u0435\u043c\u044f \u043d\u0430\u043f\u043e\u043c\u0438\u043d\u0430\u043d\u0438\u044f',
                'verbose_name_plural': '\u0412\u0440\u0435\u043c\u044f \u043d\u0430\u043f\u043e\u043c\u0438\u043d\u0430\u043d\u0438\u044f',
            },
        ),
    ]
