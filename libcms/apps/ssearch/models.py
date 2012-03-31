import datetime
from django.db import models


RECORD_SCHEMES = (
    ('rusmarc', u"Rusmarc"),
    ('usmarc', u"Usmarc"),
    ('unimarc', u"Unimarc"),
    )

RECORD_FORMATS = (
    ('iso2709', u"ISO 2709"),
    ('xml', u"XML"),
    )

RECORD_ENCODINGS = (
    ('utf-8', u"UTF-8"),
    ('cp1251', u"Windows 1251"),
    ('koi8-r', u"koi8-r"),
    ('latin-1', u"Unimarc"),
    ('marc8', u"Marc 8"),
    )


class Upload(models.Model):
    """Uploaded files."""
    file = models.FileField(upload_to='uploads', )
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    records_scheme = models.CharField(max_length=16, choices=RECORD_SCHEMES, default='rusmarc')
    records_format = models.CharField(max_length=16, choices=RECORD_FORMATS, default='iso2709')
    records_encodings = models.CharField(max_length=16, choices=RECORD_ENCODINGS, default='utf-8')

    notes = models.CharField(max_length=255, blank=True)
    processed = models.BooleanField(default=False, db_index=True)
    success = models.BooleanField(default=False, db_index=True)

    class Meta:
        ordering = ['-timestamp', ]

    def __unicode__(self):
        return unicode(self.file)

    @property
    def size(self):
        return filesizeformat(self.file.size)


class Source(models.Model):
    title = models.CharField(max_length=256, verbose_name=u"Source title")
    index_rule = models.TextField(verbose_name=u"Index rule")
    add_date = models.DateTimeField(auto_now_add=True, verbose_name=u"Add date")

    def __unicode__(self):
        return self.title

import zlib
class ZippedTextField(models.TextField):
    __metaclass__ = models.SubfieldBase

    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] == 'django.db.backends.postgresql_psycopg2' or connection.settings_dict['ENGINE'] == 'django.db.backends.postgresql':
            return 'bytea'
        else:
            return 'BLOB'

    def to_python(self, value):
        try:
            value = zlib.decompress(value,-15)
            value = value.decode('utf-8')
        except zlib.error:
            pass
        return value


    def get_db_prep_save(self, value, connection):
        if isinstance(value, unicode):
            value.encode('utf-8')
        value = zlib.compress(value)
        if value is None:
            return None
        if connection.settings_dict['ENGINE'] == 'django.db.backends.postgresql_psycopg2' or connection.settings_dict['ENGINE'] == 'django.db.backends.postgresql':
            return psycopg2.Binary(value)
        else:
            return value

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return value

class Record(models.Model):
    source = models.ForeignKey(Source, null=True, blank=True)
    gen_id = models.IntegerField(db_index=True)
    record_id = models.CharField(max_length=32, db_index=True)
    scheme = models.CharField(max_length=16, choices=RECORD_SCHEMES, default='rusmarc', verbose_name=u"Scheme")
    content = ZippedTextField(verbose_name=u'Xml content')
    add_date = models.DateTimeField(auto_now_add=True, db_index=True)
    update_date = models.DateTimeField(auto_now_add=True, db_index=True)
    deleted= models.BooleanField()
    hash = models.TextField(max_length=16)
    def __unicode__(self):
        return self.record_id
    class Meta:
        db_table = 'sc2'