# -*- coding: utf-8 -*-
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404, Http404
from common.pagination import get_page

from ..models import Question,  Category, Recomendation
from forms import QuestionForm, RecomendationForm

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
    if category:
        try:
            category = Category.objects.get(id=category)
        except Category.DoesNotExist:
            pass

        if category:
            categories.append(category)
            descendants = category.get_descendants()
            for descendant in descendants:
                categories.append(descendant)
    else:
        categories = list(Category.objects.all())

    if categories:
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
        'category': category,
        'categories': categories
    })


def detail(request, id):
    question = get_object_or_404(Question, id=id)
    if request.method == 'POST':
        recomendation_form = RecomendationForm(request.POST, prefix='recomendation_form')
        if recomendation_form.is_valid():
            with transaction.commit_on_success():
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

@transaction.commit_on_success
def ask(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            if request.user.is_authenticated():
                question.user = request.user
            question.save()
            return render(request, 'ask_librarian/frontend/thanks.html', {
                'question': question,
            })
    else:
        form = QuestionForm()

    return render(request, 'ask_librarian/frontend/ask.html', {
        'form': form
    })

