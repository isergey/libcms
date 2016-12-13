import json
from django.shortcuts import HttpResponse


def response(content, status=200):
    return HttpResponse(json.dumps(content, ensure_ascii=False), content_type='application/json', status=status)


def error_response(error, status=400):
    return response(error.to_dict(), status=status)


def errors_response(message='', code='', status=400, explain=None):
    response_dict = {
        'code': code,
        'message': message
    }
    if explain:
        response_dict['explain'] = explain
    return response(response_dict, status=status)