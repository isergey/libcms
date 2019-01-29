import traceback
from django.conf import settings
from huey.contrib.djhuey import db_task, lock_task
from . indexing import _indexing


@db_task()
@settings.HUEY.lock_task('ssearch.indexing')
def indexing(slug, reset):
    print 'start indexing', slug, 'reset', reset
    try:
        _indexing(slug, reset=reset)
    except Exception as e:
        print(e)
        traceback.print_exc()
