# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from guardian.decorators import permission_required_or_403
from common.pagination import get_page
from ..models import Feedback
from forms import FeedbackForm

@login_required
def index(request):
    if not request.user.has_module_perms('guestbook'):
        return HttpResponseForbidden()
    return redirect('guestbook:administration:feedbacks_list')

@login_required
def feedbacks_list(request):
    if not request.user.has_module_perms('guestbook'):
        return HttpResponseForbidden()

    feedbacks_page = get_page(request, Feedback.objects.all().order_by('-add_date'))

    return render(request, 'guestbook/administration/feedbacks_list.html', {
        'feedbacks_page': feedbacks_page,
    })


@login_required
@permission_required_or_403('guestbook.change_feedback')
def edit_feedback(request, id):
    feedback = get_object_or_404(Feedback, id=id)
    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=feedback)
        if form.is_valid():
            form.save()
            return redirect('guestbook:administration:feedbacks_list')
    else:
        form = FeedbackForm(instance=feedback)

    return render(request, 'guestbook/administration/edit_feedback.html', {
        'form': form,
    })


@login_required
@permission_required_or_403('guestbook.delete_feedback')
def delete_feedback(request, id=id):
    feedback = get_object_or_404(Feedback, id=id)
    feedback.delete()
    return redirect('guestbook:administration:feedbacks_list')