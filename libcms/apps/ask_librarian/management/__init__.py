#encoding: utf-8
from django.contrib.auth.models import Group
from django.db.models.signals import post_syncdb
import ask_librarian.models


def init_app(sender, **kwargs):
    print 'Init ask_librarian module'
    pass

post_syncdb.connect(init_app, sender=ask_librarian.models)



def init_groups(sender, **kwargs):
    librarians, created = Group.objects.get_or_create(name='librarians')
    if librarians:
        print '\tGroup librarians was created'

post_syncdb.connect(init_groups, sender=ask_librarian.models)