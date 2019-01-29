from huey.contrib.djhuey import db_task, lock_task
from . import indexing


@db_task()
@lock_task('ssearch.indexing')
def indexing(slug, reset):
    indexing._indexing(slug, reset=reset)
