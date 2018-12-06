import json
from django.shortcuts import HttpResponse
from django.forms.models import model_to_dict
from django.core import serializers
from django.contrib.auth.models import User

from api import decorators as api_decorators


# @api_decorators.login_required
def user(request):
    data = serializers.serialize("json", [request.user])
    return HttpResponse(data, content_type='application/json')


def get_user(request):
    username = request.GET.get('username')
    try:
        user = User.objects.get(username=username)
        data = serializers.serialize("json", [user], fields=['username', 'first_name', 'last_name', 'is_active', 'is_superuser', 'is_staff', 'groups', 'user_permissions', 'email'])
        return HttpResponse(data, content_type='application/json')
    except User.DoesNotExist:
        pass
    return HttpResponse(json.dumps({
        'status': 'error',
    }), status=400, content_type='application/json')


def check_password(request):
    username = request.GET.get('username')
    password = request.GET.get('password')
    try:
        user = User.objects.get(username=username)
        if user.check_password(password):
            return HttpResponse(json.dumps({
                'status': 'ok',
            }), content_type='application/json')

    except User.DoesNotExist:
        pass
    return HttpResponse(json.dumps({
        'status': 'error',
    }), status=400, content_type='application/json')
