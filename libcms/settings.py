# -*- coding: utf-8 -*-

import os
import sys

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

sys.path.insert(0, os.path.join(PROJECT_PATH, "apps"))
sys.path.insert(0, os.path.join(PROJECT_PATH, "vendors"))
sys.path.insert(0, os.path.join(PROJECT_PATH, "libs"))

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True



# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'



# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'


# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)



# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    # ('django.template.loaders.cached.Loader', (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #    )),
    #     'django.template.loaders.eggs.Loader',
)


# TEMPLATE_LOADERS = (
#        ('django.template.loaders.cached.Loader', (
#    'django.template.loaders.filesystem.Loader',
#    'django.template.loaders.app_directories.Loader',
#        )),
#         'django.template.loaders.eggs.Loader',
#    )


TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'social_auth.context_processors.social_auth_by_type_backends',
    #'django.contrib.messages.context_processors.messages',
)



MIDDLEWARE_CLASSES = (
    'localeurl.middleware.LocaleURLMiddleware',
    'oauth2_provider.middleware.OauthSessionMiddleware',
    # 'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django_sorting.middleware.SortingMiddleware',
    'oauth2_provider.middleware.OauthUserMiddleware',
    # 'statistics.middleware.RequestLog',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'libcms.urls'
WSGI_APPLICATION = 'libcms.wsgi.application'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'sso.backend.SSOBackend',
    'sso_ruslan.backend.RuslanAuthBackend',
    'oauth2_provider.backend.OauthUserBackend',
    'guardian.backends.ObjectPermissionBackend',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    # 'django.contrib.admindocs',

    # vendor apps
    'localeurl',
    'mptt',
    'guardian',
    'captcha',
    # 'debug_toolbar',
    'django_sorting',
    # cms apps
    'core',
    'accounts',
    'profile',
    # 'social_auth',
    'filebrowser',
    'menu',
    'pages',
    'news',
    'events',
    'extsystems',
    'ldap_sync',
    'participants',
    'participant_news',
    'participant_events',
    'participant_pages',
    'participant_site',
    'participant_menu',
    'participant_photopolls',
    'participant_banners',
    'professionals_pages',
    'professionals_news',
    'professionals',
    'personal',
    'ruslan_users',
    'ask_librarian',
    'ssearch',
    'statistics',
    'rbooks',
    'forum',
    # 'urt',
    'orders',
    'polls',
    'ruslan_cabinet',
    'external_orders',
    'zgate',
    'mydocs',
    'guestbook',
    'newinlib',
    'attacher',
    'oauth2_provider',
    'sso',
    'sso_ruslan',
    'sso_esia',
    'sso_tatedu',
    'subscribe',
    'recommended_reading',
    'bootstrap3',
)

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


# префикс для системы кеширования
KEY_PREFIX = 'libcms'

# guardian settings
ANONYMOUS_USER_ID = -1

LOGIN_REDIRECT_URL = "/"

DEBUG_TOOLBAR_PANELS = [
    # 'debug_toolbar.panels.versions.VersionsPanel',
    # 'debug_toolbar.panels.timer.TimerPanel',
    # 'debug_toolbar.panels.settings.SettingsPanel',
    # 'debug_toolbar.panels.headers.HeadersPanel',
    # 'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    # 'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    # 'debug_toolbar.panels.templates.TemplatesPanel',
    # 'debug_toolbar.panels.cache.CachePanel',
    # 'debug_toolbar.panels.signals.SignalsPanel',
    # 'debug_toolbar.panels.logging.LoggingPanel',
    # 'debug_toolbar.panels.redirects.RedirectsPanel',
]

LOCALE_INDEPENDENT_PATHS = (
    r'^/esia_sso/redirect',
    r'^/statistics/api/',
    r'^/participants/api/',
    r'^/robots.txt/',
)

PARTICIPANTS_SHOW_ORG_TYPES = ['library', 'school']

from local_settings import *
