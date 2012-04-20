# -*- coding: utf-8 -*-
import datetime
from django.shortcuts import render, Http404, HttpResponse, redirect, get_object_or_404
from forms import QuestionForm
from models import Question, Category, AnswerManager, ManagerNonActivePeriod, Answer


def index(request):
    return render(request, 'ask_librarian/administration/module.html')


def questions(request):
    questions = None #Question.objects.all()
    return render(request, 'ask_librarian/administration/questions_stats.html', {
        #'questions'
    })


def questions_list(request):
    questions = Question.objects.all()
    return render(request, 'ask_librarian/administration/questions_list.html', {
        'questions': questions,
    })


def questions_detail(request, id):
    question = get_object_or_404(Question, id=id)
    #question = Question.objects.filter(id=id).prefetch_related('answer_language')[0]
    #print question.answer_language.all()
    try:
        answer = Answer.objects.get(question=question)
    except Answer.DoesNotExist:
        answer = None

    return render(request, 'ask_librarian/administration/questions_detail.html', {
        'question': question,
        'answer': answer
    })


def managers(request):
    return render(request, 'ask_librarian/administration/managers.html')