# encoding: utf-8
import simplejson
from django.http import HttpResponse



def response(data={}):
    if not isinstance(data, dict):
        raise TypeError(u'data must be dict type object')
    return HttpResponse(simplejson.dumps(data, ensure_ascii=False), mimetype='application/json; charset=utf8')


