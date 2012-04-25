# -*- coding: utf-8 -*-
from datetime import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class Forum(models.Model):
    title = models.CharField(max_length=255, verbose_name=_(u'Title'), help_text=_(u'Maximum 255 simbols'))
    slug = models.SlugField(unique=True, verbose_name=_(u'Slug'), help_text=_(u'Small latin letter, "-" and "_"'))
    description = models.CharField(max_length=1024, verbose_name=_(u'Description'), help_text=_(u'Maximum 1024 simbols'))
    ordering = models.IntegerField(default=0, verbose_name=_(u'Ordering'), db_index=True, help_text=_(u'Order in forums list'))
    closed = models.BooleanField(verbose_name=_(u'Closed'), db_index=True, default=False, help_text=_(u'If forum is closed, users can not create topics'))
    deleted = models.BooleanField(verbose_name=_(u'Deleted'), db_index=True, default=False)

    class Meta:
        ordering = ['ordering',]
        permissions = (
            ("can_views_forums", "Can view forums"),
            ("can_close_forums", "Can close forum"),
            ("can_view_topics", "Can view topics in forum"),
            ("can_create_topics", "Can create topics in forum"),
            ("can_change_topics", "Can change topics in forum"),
            ("can_delete_topics", "Can delete topics in forum"),
            ("can_close_topics", "Can close all topics in forum"),
            ("can_close_own_topics", "Can close own topics in forum"),
            ("can_hide_topics", "Can hide topics in forum"),
            )

    def __unicode__(self):
        return self.title



class Topic(models.Model):
    forum = models.ForeignKey(Forum)
    subject = models.CharField(verbose_name=_(u'Subject'), max_length=255, help_text=_(u'Maximum 255 simbols'))
    created = models.DateTimeField(default=datetime.now, db_index=True, verbose_name=_(u'Created'))
    public = models.BooleanField(verbose_name=_(u'Publicated'), db_index=True, default=False)
    closed = models.BooleanField(verbose_name=_(u'Closed'), db_index=True, default=False, help_text=_(u'If topic is closed, users can not create messages'))
    deleted = models.BooleanField(verbose_name=_(u'Deleted'), db_index=True, default=False)
    class Meta:
        ordering = ['-id']
        permissions = (
            ("can_view_articles", "Can view topic articles"),
            ("can_add_articles", "Can add articles in topic"),
            ("can_change_articles", "Can change articles in topic"),
            ("can_delete_articles", "Can delete articles from topic"),
            ("can_hide_articles", "Can hide articles in topic"),
            ("can_publish_own_articles", "Can publish own articles in topic"),
            )


class Article(models.Model):
    topic = models.ForeignKey(Topic)
    author = models.ForeignKey(User, blank=True, null=True, verbose_name=_(u'Author'))
    text = models.TextField(verbose_name=_(u'Text of message'), max_length=10000, help_text=_(u'Maximum 10000 simbols'))
    created = models.DateTimeField(default=datetime.now, db_index=True, verbose_name=_(u'Created'))
    updated = models.DateTimeField(auto_now=True, db_index=True, verbose_name=_(u'Created'))
    public = models.BooleanField(verbose_name=u'Publicated', db_index=True, default=False)
    deleted = models.BooleanField(verbose_name=_(u'Deleted'), db_index=True, default=False)
    class Meta:
        ordering = ['created']

    def __unicode__(self):
        return u'(%s, %s)' % (self.topic, self.author)