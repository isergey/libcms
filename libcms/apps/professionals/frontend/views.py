# coding: utf-8
from django.shortcuts import render
from guardian.decorators import permission_required_or_403
@permission_required_or_403('professionals.can_access_prof_page')
def index(request):

    return render(request, 'professionals/frontend/index.html')
