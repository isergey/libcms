# -*- coding: utf-8 -*-
import hashlib
import uuid
from django.shortcuts import redirect, render, HttpResponse, get_object_or_404
from django.core.urlresolvers import reverse

from common.pagination import get_page
from ..models import Poll, Choice, PolledUser


def index(request):
    polls_page = get_page(request, Poll.objects.filter(published=True).order_by('-id')[:100])
    return render(request, 'polls/frontend/index.html', {
        'polls_page': polls_page
    })


def vote(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id, published=True)

    if not poll.is_active():
        return redirect(reverse('polls:frontend:results', args=(poll.id,)))

    poller_id = get_poller_id(request)

    if not poll.multi_vote:
        votes_in_poll = PolledUser.objects.filter(poller_id=poller_id, poll=poll).count()

        if votes_in_poll:
            return results(request, poll_id, poll)

    if request.method == 'POST' and 'answer' in request.POST:
        if poll.poll_type == 'radio':
            # Голосуем за первый попавшийся id
            choices = Choice.objects.filter(poll=poll, pk__in=request.POST.getlist('answer'))[:1]
        elif poll.poll_type == 'checkboxes':
            choices = Choice.objects.filter(poll=poll, pk__in=request.POST.getlist('answer'))
        else:
            raise ValueError(u'Type of poll must be "radio" or "checkboxes"')

        for choice in choices:
            choice.votes += 1
            choice.save()

        polled_user = PolledUser(poller_id=poller_id, poll=poll)
        polled_user.save()

        response = results(request, poll_id, poll)
        set_cookies(response, poller_id)
        return response

    choices = Choice.objects.filter(poll=poll).order_by('-sort')

    response = render(request, 'polls/frontend/vote.html', {
        'poll': poll,
        'choices': choices,
    })
    set_cookies(response, poller_id)
    return response


def results(request, poll_id, poll=None):
    if not poll:
        poll = get_object_or_404(Poll, id=poll_id, published=True)

    choices = Choice.objects.filter(poll=poll).order_by('-sort')[:100]

    choices_dicts = []
    # суммарное число ответов
    summ_number_of_answers = 0

    # сортируем ответы по количеству голосов, начиная от большего к меньшему
    # и извлекаем максимальное значение
    max_choice_answers = 0
    if len(choices):
        max_choice_answers = sorted(choices, key=lambda x: x.votes, reverse=True)[0].votes
        if max_choice_answers == 0:
            max_choice_answers = 1

    for choice in choices:
        summ_number_of_answers += choice.votes
    if summ_number_of_answers == 0:
        summ_number_of_answers = 1
    for choice in choices:
        choices_dicts.append({
            'choice': choice,
            # Процент от макимального значения
            'percent_from_max': int(choice.votes * 100 / summ_number_of_answers),
        })
    if summ_number_of_answers == 0:
        summ_number_of_answers = 1;
    for choices_dict in choices_dicts:
        # Процент от суммарного значения голосов
        choices_dict['percent_from_sum_votes'] = '%0.2f' % \
                                                 (choices_dict['choice'].votes * 100.0 / summ_number_of_answers)

    show_results = False
    message = u"Спасибо за ответ. Ваше мнение очень важно для нас!"
    if request.method == 'GET':
        if poll.show_results_after_end_poll:
            message = u"Результаты будут доступны после завершения опроса."
        else:
            message = u"Результаты опроса не доступны."
    elif request.method == 'POST':
        if poll.show_results_after_end_poll:
            message = u"Спасибо за ответ! Результаты будут доступны после завершения опроса!"

    # если голосование активно и разрешено показывать результаты
    if poll.is_active() and poll.show_results_on_vote:
        show_results = True

    # если голосование НЕ активно и разрешено показывать результаты
    # после завершения голосования
    elif not poll.is_active() and poll.show_results_after_end_poll:
        show_results = True

    if request.is_ajax():
        return render(request, 'polls/tags/polls_ajax_results.html', {
            'poll': poll,
            'choices_dicts': choices_dicts,
            'show_results': show_results,
            'message': message
        })

    return render(request, 'polls/frontend/polls_results.html', {
        'poll': poll,
        'choices_dicts': choices_dicts,
        'show_results': show_results,
        'message': message,
    })


def set_cookies(response, poller_id):
    response.set_cookie('polls.id', poller_id, expires=(365 * 24 * 3600))


def get_poller_id(request):
    if request.user.is_authenticated():
        poller_id = hashlib.md5(request.user.username).hexdigest()
    else:
        poller_id = request.COOKIES.get('polls.id', uuid.uuid4().hex)
    return poller_id
