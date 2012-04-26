# -*- coding: utf-8 -*-
import datetime
from django.shortcuts import render, Http404, HttpResponse,redirect, get_object_or_404
from forms import QuestionForm
from models import Question, Category, AnswerManager, ManagerNonActivePeriod, Answer


def index(request):
    #categories = Category.tree.root_nodes()
    #Category.tree.rebuild()
    categories = Category.objects.all()

#    print categories
    return render(request, 'ask_librarian/frontend/index.html', {'categories':categories})



def available_managers(request):
#    not_active_managers = ManagerNonActivePeriod.get_not_active_periods()
#    active_managers = AnswerManager.objects.all().exclude(id__in=not_active_managers)
#    for manager in  not_active_managers:
#        print unicode(manager)
#    print 'active managers'
#    for manager in  active_managers:
#        print unicode(manager)

    not_active_managers = AnswerManager.get_active_managers()
    for manager in  not_active_managers:
        print unicode(manager)

    return render(request, 'base.html')



def by_category(request, id):
    categories = Category.objects.all()
    category = get_object_or_404(Category, id=id)
    filter_categories = [category]
    if not category.is_leaf_node():
        filter_categories = category.get_descendants(include_self=True)
    questions = Question.objects.filter(category__in=filter_categories)
    return render(request, 'ask_librarian/frontend/index.html', {
        'categories':categories,
        'category':category,
        'questions': questions
        })



def ask_question(request):
    if request.method=='POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            form.save_m2m()
            return redirect(question)
    else:
        form = QuestionForm()
    return render(request, 'ask_librarian/frontend/create_question.html', {'form':form})



def question_detail(request, id):
    question = get_object_or_404(Question, id=id)
    try:
        answer = Answer.objects.get(question=question)
    except Answer.DoesNotExist:
        answer = None
    return render(request, 'ask_librarian/frontend/question_detail.html', {
        'question':question,
        'answer': answer
    })


