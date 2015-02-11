import requests
from django.shortcuts import render
from .. import models
from . import forms
def index(request):

    period_form = forms.PeriodForm(request.GET, prefix='pf')
    results = []
    if period_form.is_valid():
        results = models.get_view_count_stats(
            period_form.cleaned_data['from_date'],
            period_form.cleaned_data['to_date'],
            period_form.cleaned_data['period'],
            #url_filter='/site/[0-9]+/?$'
        )

    return render(request, 'statistics/frontend/index.html', {
        'period_form': period_form,
        'results': results
    })

# METRIKA_URL = 'http://api-metrika.yandex.ru'
# # 444c680b612b47178114c8eef3811e5a
# def index(request):
#     response = requests.get(METRIKA_URL + '/counters', headers={
#         'Accept': 'application/x-yametrika+json',
#         'Content-type': 'application/x-yametrika+json',
#         'Authorization': 'OAuth 444c680b612b47178114c8eef3811e5a'
#     })
#
#     response = requests.get(METRIKA_URL + '/stat/content/popular', headers={
#         'Accept': 'application/x-yametrika+json',
#         'Content-type': 'application/x-yametrika+json',
#         'Authorization': 'OAuth 444c680b612b47178114c8eef3811e5a'
#     }, params={
#         'id': '3927343',
#         'table_mode': 'tree'
#     })
#
#     print response.text
#
#
#     return render(request, 'statistics/frontend/index.html')