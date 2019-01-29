from huey.contrib.djhuey import db_task, lock_task
from . indexing import _indexing


@db_task()
@lock_task('ssearch.indexing')
def indexing(slug, reset):
    print 'start indexing', slug, 'reset', reset
    _indexing(slug, reset=reset)
