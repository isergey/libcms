from django.conf.urls import patterns, include, url
from django.contrib.admin.sites import site
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    (r'^', include('apps.index.urls', namespace='index')),
    (r'^core/', include('apps.core.urls', namespace='core')),
    (r'^accounts/', include('apps.accounts.urls', namespace='accounts')),
    (r'^filebrowser/', include('apps.filebrowser.urls', namespace='filebrowser')),
    (r'^menu/', include('apps.menu.urls', namespace='menu')),
    (r'^pages/', include('apps.pages.urls', namespace='pages')),
    (r'^news/', include('apps.news.urls', namespace='news')),
    (r'^ssearch/', include('apps.search.urls', namespace='search')),
    (r'^newinlib/', include('apps.newinlib.urls', namespace='newinlib')),
    (r'^gallery/', include('apps.gallery.urls', namespace='gallery')),
    (r'^polls/', include('apps.polls.urls', namespace='polls')),
    (r'^events/', include('apps.events.urls', namespace='events')),
    (r'^consultation/', include('apps.ask_librarian.urls', namespace='ask_librarian')),
    (r'^mydocs/', include('apps.mydocs.urls', namespace='mydocs')),
    (r'^personal/', include('apps.personal.urls', namespace='personal')),
    (r'^subscribe/', include('apps.subscribe.urls', namespace='subscribe')),
    url(r'^testapp/', include('apps.testapp.urls', namespace='testapp')),
    url(r'^radmin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^radmin/', include(admin.site.urls)),
    url(r'^jsi18n/$', site.i18n_javascript, name='jsi18n'),
    url(r'^captcha/', include('captcha.urls')),
)



from django.conf import settings

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
            }),
    )