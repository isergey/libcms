# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404, Http404, urlresolvers
from django.contrib.auth.decorators import login_required
from common.pagination import get_page

from ..models import Question,  Category, Recomendation
from forms import get_question_form, RecomendationForm, DateFilterForm

def index(request):
    id =  request.GET.get('id', None)
    if id:
        try:
            id = int(id)
        except ValueError:
            raise Http404()
        return redirect('ask_librarian:frontend:detail', id=id)

    category = request.GET.get('category', None)
    categories = []
    category_m = None
    if category:
        try:
            category_m = Category.objects.get(id=category)
        except Category.DoesNotExist:
            raise Http404(u'Категория не найдена')

        if category_m:
            categories.append(category_m)
            descendants = category_m.get_descendants()
            for descendant in descendants:
                categories.append(descendant)
    else:
        categories = list(Category.objects.all())

    filtered_by_date = False

    if request.method == 'POST':
        date_filter_form = DateFilterForm(request.POST)
        if date_filter_form.is_valid():
            date =  date_filter_form.cleaned_data['date']
            questions_page = get_page(request, Question.objects.filter(create_date__year=date.year,create_date__month=date.month, create_date__day=date.day, status=1).order_by('-id'), 10)
            filtered_by_date = True
    else:
        date_filter_form = DateFilterForm()


    if not filtered_by_date:
    #        print categories
        if category and categories:
            questions_page = get_page(request, Question.objects.filter(category__in=categories, status=1).order_by('-create_date'), 10)
        else:
            questions_page = get_page(request, Question.objects.filter(status=1).order_by('-create_date'), 10)
    questions_page.object_list = list(questions_page.object_list)
    cd = {}

    for category_item in categories:
        cd[category_item.id] = category_item

    for question in questions_page.object_list:
        if question.category_id in cd:
            question.category = cd[question.category_id]



    return render(request, 'ask_librarian/frontend/questions_list.html', {
        'questions_page': questions_page,
        'category': category_m,
        'categories': categories,
        'date_filter_form': date_filter_form
    })


def detail(request, id):
    question = get_object_or_404(Question, id=id)
    if request.method == 'POST':
        recomendation_form = RecomendationForm(request.POST, prefix='recomendation_form')
        if recomendation_form.is_valid():
            with transaction.atomic():
                recomendation = recomendation_form.save(commit=False)
                if request.user.is_authenticated():
                    recomendation.user = request.user
                recomendation.question = question
                recomendation.save()
                return render(request, 'ask_librarian/frontend/recomended_thanks.html', {
                    'question': question,
                    })
    else:
        recomendation_form = RecomendationForm(prefix='recomendation_form')
    recomendations = Recomendation.objects.filter(question=question, public=True).order_by('-create_date')
    return render(request, 'ask_librarian/frontend/detail.html', {
        'question': question,
        'recomendation_form': recomendation_form,
        'recomendations': recomendations
    })

def printed_detail(request, id):
    question = get_object_or_404(Question, id=id)
    return render(request, 'ask_librarian/frontend/printed_detail.html', {
        'question': question,
        })

@transaction.atomic
def ask(request):
    QuestionForm = get_question_form(not request.user.is_authenticated())
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            if request.user.is_authenticated():
                question.user = request.user
            question.save()

            ask_librarian_settings = getattr(settings, 'ASK_LIBRARIAN', {})
            main_dispatcher = ask_librarian_settings.get('MAIN_DISPATCHER', None)
            if main_dispatcher:
                fail_silently = True
                if settings.DEBUG:
                    fail_silently = False

                domain = getattr(settings, 'SITE_DOMAIN', 'localhost')
                from_mail = settings.DEFAULT_FROM_EMAIL
                send_mail(u"Спроси библиографа. Новый вопрос.",
                    u'Поступил новый вопрос. Информация находится по адресу http://%s%s' %
                    (domain, urlresolvers.reverse('ask_librarian:administration:question_detail', args=(question.id,))),
                    from_mail,
                    [main_dispatcher],
                    fail_silently=fail_silently
                )
            return render(request, 'ask_librarian/frontend/thanks.html', {
                'question': question,
                })
    else:
        if request.user.is_authenticated():
            form = QuestionForm(
                initial={
                    'fio': request.user.last_name + u' ' + request.user.first_name,
                    'email': request.user.email,
                    }
            )
        else:
            form = QuestionForm()


    return render(request, 'ask_librarian/frontend/ask.html', {
        'form': form
    })

@login_required
def my_questions(request):
    questions_page = get_page(request, Question.objects.filter(user=request.user).order_by('-create_date'), 10)
    return render(request, 'ask_librarian/frontend/my_questions.html', {
        'questions_page': questions_page
    })