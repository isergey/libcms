# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from django.contrib.admin.sites import site
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^', include('index.urls', namespace='index')),
    (r'^core/', include('core.urls', namespace='core')),
    (r'^accounts/', include('accounts.urls', namespace='accounts')),
    (r'^filebrowser/', include('filebrowser.urls', namespace='filebrowser')),
    (r'^menu/', include('menu.urls', namespace='menu')),
    (r'^pages/', include('pages.urls', namespace='pages')),
    (r'^news/', include('news.urls', namespace='news')),
    (r'^events/', include('events.urls', namespace='events')),
    (r'^participants/', include('participants.urls', namespace='participants')),
    (r'^forum/', include('forum.urls', namespace='forum')),

#    (r'^ask_librarian/', include('ask_librarian.urls', namespace='ask_librarian')),
    (r'^ssearch/', include('ssearch.urls', namespace='ssearch')),

    # Uncomment the next line to enable the admin:
    url(r'^radmin/', include(admin.site.urls)),
    url(r'^jsi18n/$', site.i18n_javascript, name='jsi18n'),
    url(r'^sauth/', include('social_auth.urls')),
)