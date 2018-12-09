# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils import translation
from django.utils.translation import get_language
from common.pagination import get_page
from participants.models import Library
from .. import models
import forms


def index(request, library_code):
    library = get_object_or_404(Library, code=library_code)
    polls_page = get_page(
        request, models.Poll.objects.filter(
            publicated=True,
            library=library
        ).order_by('-create_date')
    )

    poll_contents = list(
        models.PollContent.objects.filter(
            poll__in=list(polls_page.object_list),
            lang=get_language()[:2]
        ))

    t_dict = {}
    for poll in polls_page.object_list:
        t_dict[poll.id] = {'poll': poll}

    for poll_content in poll_contents:
        t_dict[poll_content.poll_id]['poll'].poll_content = poll_content

    return render(request, 'participant_photopolls/frontend/list.html', {
        'library': library,
        'polls_list': polls_page.object_list,
        'polls_page': polls_page,
    })


def show(request, library_code, id):
    library = get_object_or_404(Library, code=library_code)
    cur_language = translation.get_language()
    poll = get_object_or_404(models.Poll, id=id, library=library)
    try:
        content = models.PollContent.objects.get(poll=poll, lang=cur_language[:2])
    except models.PollContent.DoesNotExist:
        content = None

    images_contents_dict = {}
    images = models.PollImage.objects.filter(poll=poll)
    images_contents = models.PollImageContent.objects.filter(poll_image__in=images)
    for images_content in images_contents:
        images_contents_dict[images_content.poll_image_id] = images_content

    images_list = []
    for image in images:
        images_list.append({
            'image': image,
            'content': images_contents_dict.get(image.id, {})
        })
    return render(request, 'participant_photopolls/frontend/show.html', {
        'library': library,
        'poll': poll,
        'content': content,
        'images_list': images_list
    })


def vote(request, library_code, poll_id, image_id):
    library = get_object_or_404(Library, code=library_code)
    poll = get_object_or_404(models.Poll, id=poll_id, library=library)
    image = get_object_or_404(models.PollImage, poll=poll, id=image_id)

    user = None
    if request.user.is_authenticated():
        user = request.user

    can_vote = True
    ip = get_client_ip(request)
    if not poll.multi_vote:
        if models.Vote.objects.filter(poll_image=image, user=user).exists():
            can_vote = False

        if models.Vote.objects.filter(poll_image=image, ip=ip).exists():
            can_vote = False

    if can_vote:
        models.Vote(user=user, poll_image=image, ip=ip).save()
    return HttpResponse('Спасибо за голос')
    return redirect('participant_photopolls:frontend:show', library_code=library_code, id=poll.id)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip