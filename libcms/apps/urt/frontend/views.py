# -*- coding: utf-8 -*-
from django.core.mail import send_mail
from django.db import transaction
from django.contrib.sites.models import Site
from django.contrib.auth.models import User, Group
from django.utils.hashcompat import md5_constructor
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.messages.api import get_messages

from social_auth import __version__ as version
from forms import RegistrationForm
from accounts.models import RegConfirm

def index(request):
    return render(request, 'accounts/frontend/index.html')


#def login(request):
#    if request
#    return render(request, 'frontend/login.html')

def logout(request):
    pass

def register(request):
    pass

def home(request):
    """Home view, displays login mechanism"""
    if request.user.is_authenticated():
        return redirect('accounts:frontend:done')
    else:
        return render(request, 'accounts/frontend/oauth/home.html', {
            'version': version
        })

@login_required
def done(request):
    """Login complete view, displays user data"""
    ctx = {
        'version': version,
        'last_login': request.session.get('social_auth_last_login_backend')
    }
    return render(request, 'accounts/frontend/oauth/done.html', ctx)


def error(request):
    """Error view"""
    messages = get_messages(request)
    return render(request, 'accounts/frontend/oauth/error.html', {
        'version': version,
        'messages': messages
    })

@transaction.commit_on_success
def registration(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                is_active=False,
            )
            user.set_password(form.cleaned_data['password'])
            user.save()
            hash = md5_constructor(str(user.id) + form.cleaned_data['username']).hexdigest()
            confirm = RegConfirm(hash=hash, user_id=user.id)
            confirm.save()
            current_site = Site.objects.get(id=1)
            message = u'Поздравляем! Вы зарегистрировались на %s . Пожалуйста, пройдите по адресу %s для активации учетной записи.' % \
                      (current_site.domain, "http://" + current_site.domain + "/accounts/confirm/" + hash, )


            send_mail(u'Активация аккаунта ' + current_site.domain, message, 'system@'+current_site.domain,
                [form.cleaned_data['email']])

            return render(request, 'accounts/frontend/registration_done.html')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/frontend/registration.html', {
        'form':form
    })
@transaction.commit_on_success
def confirm_registration(request, hash):
    try:
        confirm = RegConfirm.objects.get(hash=hash)
    except RegConfirm.DoesNotExist:
        return HttpResponse(u'Код подтверждения не верен')
    try:
        user = User.objects.get(id=confirm.user_id)
    except User.DoesNotExist:
        return HttpResponse(u'Код подтверждения не верен')

    if user.is_active == False:
        #тут надо создать пользователя в лдапе
        user.is_active = True
        group = Group.objects.get(name='users')
        user.groups.add(group)
        user.save()
        confirm.delete()
    return render(request,  'accounts/frontend/registration_confirm.html')

