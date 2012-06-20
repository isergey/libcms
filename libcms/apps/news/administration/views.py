# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import transaction
from django.utils.translation import ugettext as _
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from guardian.decorators import permission_required_or_403
from django.contrib.auth.decorators import login_required
from common.pagination import get_page
from django.contrib.auth import login, REDIRECT_FIELD_NAME
from django.utils.translation import to_locale, get_language

from core.forms import LanguageForm
from news.models import News, NewsContent
from forms import NewsForm, NewsContentForm

@login_required
@permission_required_or_403('news.add_news')
def index(request):
    return redirect('news:administration:news_list')


@login_required
@permission_required_or_403('news.add_news')
def news_list(request):
    type = request.GET.get('type', u'public')
    if type ==  u'prof':
        news_page = get_page(request, News.objects.filter(type=1).order_by('-create_date'))
    elif type == u'public':
        news_page = get_page(request, News.objects.filter(type=0).order_by('-create_date'))
    else:
        news_page = get_page(request, News.objects.filter(type=2).order_by('-create_date'))

    news_contents = list(NewsContent.objects.filter(news__in=list(news_page.object_list), lang=get_language()[:2]))

    t_dict = {}
    for news in news_page.object_list:
        t_dict[news.id] = {'news': news}

    for news_content in news_contents:
        t_dict[news_content.news_id]['news'].news_content = news_content

    return render(request, 'news/administration/news_list.html', {
        'news_list': news_page.object_list,
        'news_page': news_page,
        })



@login_required
@permission_required_or_403('news.add_news')
@transaction.commit_on_success
def create_news(request):

    if request.method == 'POST':
        news_form = NewsForm(request.POST,prefix='news_form')

        news_content_forms = []
        for lang in settings.LANGUAGES:
            news_content_forms.append({
                'form':NewsContentForm(request.POST,prefix='news_content' + lang[0]),
                'lang':lang[0]
            })

        if news_form.is_valid():



            valid = False
            for news_content_form in news_content_forms:
                valid = news_content_form['form'].is_valid()
                print valid
                if not valid:
                    break

            if valid:
                news = news_form.save(commit=False)
                news.save()
                for news_content_form in news_content_forms:
                    news_content = news_content_form['form'].save(commit=False)
                    news_content.lang = news_content_form['lang']
                    news_content.news = news
                    news_content.save()
                return redirect('news:administration:news_list')
    else:
        news_form = NewsForm(prefix="news_form")
        news_content_forms = []
        for lang in settings.LANGUAGES:
            news_content_forms.append({
                'form':NewsContentForm(prefix='news_content' + lang[0]),
                'lang':lang[0]
            })

    return render(request, 'news/administration/create_news.html', {
        'news_form': news_form,
        'news_content_forms': news_content_forms,
    })

@login_required
@permission_required_or_403('news.change_news')
@transaction.commit_on_success
def edit_news(request, id):
    news = get_object_or_404(News, id=id)
    news_contents = NewsContent.objects.filter(news=news)
    news_contents_langs = {}

    for lang in settings.LANGUAGES:
        news_contents_langs[lang] = None

    for news_content in news_contents:
        news_contents_langs[news_content.lang] = news_content

    if request.method == 'POST':
        news_form = NewsForm(request.POST,prefix='news_form', instance=news)

        if news_form.is_valid():
            news_form.save()
            news_content_forms = []
            for lang in settings.LANGUAGES:
                lang = lang[0]
                if lang in news_contents_langs:
                    news_content_forms.append({
                        'form':NewsContentForm(request.POST,prefix='news_content_' + lang, instance=news_contents_langs[lang]),
                        'lang':lang
                    })
                else:
                    news_content_forms.append({
                        'form':NewsContentForm(request.POST, prefix='news_content_' + lang),
                        'lang':lang
                    })


            valid = False
            for news_content_form in news_content_forms:
                valid = news_content_form['form'].is_valid()
                if not valid:
                    break

            if valid:
                for news_content_form in news_content_forms:
                    news_content = news_content_form['form'].save(commit=False)
                    news_content.news = news
                    news_content.lang = news_content_form['lang']
                    news_content.save()
                return redirect('news:administration:news_list')
    else:
        news_form = NewsForm(prefix="news_form", instance=news)
        news_content_forms = []
        for lang in settings.LANGUAGES:
            lang = lang[0]
            if lang in news_contents_langs:
                news_content_forms.append({
                    'form':NewsContentForm(prefix='news_content_' + lang, instance=news_contents_langs[lang]),
                    'lang':lang
                })
            else:
                news_content_forms.append({
                    'form':NewsContentForm(prefix='news_content_' + lang),
                    'lang':lang
                })
    return render(request, 'news/administration/edit_news.html', {
        'news_form': news_form,
        'news_content_forms': news_content_forms,
        })


@login_required
@permission_required_or_403('news.delete_news')
@transaction.commit_on_success
def delete_news(request, id):
    news = get_object_or_404(News, id=id)
    news.delete()
    return redirect('news:administration:news_list')


