# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from common.pagination import get_page
from ..models import Feedback
from forms import FeedbackForm


def index(request):
    feedbacks_page = get_page(request, Feedback.objects.filter(publicated=True).order_by('-add_date'))
    return render(request, 'guestbook/frontend/index.html', {
        'feedbacks_page': feedbacks_page,
    })


def send_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'guestbook/frontend/thanks.html')
    else:
        form = FeedbackForm()

    return render(request, 'guestbook/frontend/send_feedback.html', {
        'form': form,
    })
