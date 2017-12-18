# -*- coding: utf-8 -*-
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
#from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from guardian.decorators import permission_required_or_403
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from ..models import Poll, Choice
from forms import PollForm, ChoiceForm
from django.forms.models import model_to_dict
from django.forms.formsets import formset_factory
from django.forms.models import BaseInlineFormSet, inlineformset_factory


@permission_required_or_403('polls.add_poll')
def index(request):
    polls = Poll.objects.all().order_by('-id')
    paginator = Paginator(polls, 20)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        polls_list = paginator.page(page)
    except (EmptyPage, InvalidPage):
        polls_list = paginator.page(paginator.num_pages)

    return render(request, 'polls/administration/list.html',
            {'polls_list': polls_list,
             'active_module': 'polls'})


@permission_required_or_403('polls.add_poll')
def create(request):
    if request.method == 'POST':
        form = PollForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('polls:administration:index'))
    else:
        form = PollForm()
    return render(request, 'polls/administration/create.html',
            {'form': form,
             'active_module': 'polls'})


@permission_required_or_403('polls.change_poll')
def edit(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    if request.method == 'POST':
        form = PollForm(request.POST, instance=poll)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('polls:administration:index'))
    else:

        form = PollForm(model_to_dict(poll),instance=poll)
    return render(request, 'polls/administration/edit.html',
            {'form': form,
             'poll':poll,
             'active_module': 'polls'})


@permission_required_or_403('polls.delete_poll')
def delete(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    poll.delete()
    return HttpResponseRedirect(reverse('polls:administration:index'))


@permission_required_or_403('polls.add_choice')
def view(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    choices = Choice.objects.filter(poll=poll).order_by('-sort')

    return render(request, 'polls/administration/view.html',
            {'poll': poll,
             'choices':choices,
             'active_module': 'polls'})


@permission_required_or_403('polls.add_choice')
def create_choice(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    choice = Choice(poll=poll)
    if request.method == 'POST':
        form = ChoiceForm(request.POST, request.FILES, instance=choice)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('polls:administration:view', args=[poll.id]))
    else:
        form = ChoiceForm(initial={'poll':poll})
    return render(request, 'polls/administration/create_choice.html',
            {'form': form,
             'poll': poll,
             'active_module': 'polls'})


@permission_required_or_403('polls.change_choice')
def edit_choice(request, choice_id):
    choice = get_object_or_404(Choice, id=choice_id)
    if request.method == 'POST':
        form = ChoiceForm(request.POST, request.FILES, instance=choice)
        if form.is_valid():
            form.save()
            #            choice.choice = form.cleaned_data['choice']
            #            choice.votes = form.cleaned_data['votes']
            #            choice.save()
            return HttpResponseRedirect(reverse('polls:administration:view', args=[choice.poll.id]))
    else:

        form = ChoiceForm(instance=choice)
    return render(request, 'polls/administration/edit_choice.html',
            {'form': form,
             'choice': choice,
             'active_module': 'polls'})


@permission_required_or_403('polls.delete_choice')
def delete_choice(request, choice_id):
    choice = get_object_or_404(Choice, id=choice_id)
    poll_id = choice.poll.id
    choice.delete()
    return HttpResponseRedirect(reverse('polls:administration:view', args=[poll_id]))
