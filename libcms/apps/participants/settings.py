from django.conf import settings

PARTICIPANTS_SHOW_ORG_TYPES = getattr(settings, 'PARTICIPANTS_SHOW_ORG_TYPES', [])
