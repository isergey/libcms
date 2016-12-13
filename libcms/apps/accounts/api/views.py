import json
from django.shortcuts import HttpResponse
from django.forms.models import model_to_dict
from django.core import serializers

from api import decorators as api_decorators

@api_decorators.login_required
def user(request):
    data = serializers.serialize("json",[request.user])
    return HttpResponse(data, content_type='application/json')