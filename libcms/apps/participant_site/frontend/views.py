from django.shortcuts import render, redirect, get_object_or_404
from participants.models import Library


def index(request, library_code):
    library = get_object_or_404(Library, code=library_code)
    ancestors = library.get_ancestors()
    return render(request, 'participant_site/frontend/index.html', {
        'library': library,
        'ancestors': ancestors
    })

def site_page(request):
    return render(request, 'index/frontend/org_page.html')

def site_news_list(request):
    return render(request, 'index/frontend/org_news_list.html')

def site_news_detail(request, id):
    return render(request, 'index/frontend/org_news_detail.html')