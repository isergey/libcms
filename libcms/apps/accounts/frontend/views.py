# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.messages.api import get_messages

from social_auth import __version__ as version
from forms import RegistrationForm
from accounts.models import RegConfirm

from participants import models as participants_models


def index(request):
    return render(request, 'accounts/frontend/index.html')


# def login(request):
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


import urlparse
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.models import get_current_site


@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request, template_name='registration/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          current_app=None, extra_context=None):
    """
    Displays the login form and handles the login action.
    """
    wifi = request.GET.get('wifi', '')
    remote_addr = request.META.get('REMOTE_ADDR', '')
    redirect_to = request.REQUEST.get(redirect_field_name, '')

    if request.method == "POST":
        form = authentication_form(data=request.POST)
        if form.is_valid():
            netloc = urlparse.urlparse(redirect_to)[1]

            # Use default setting if redirect_to is empty
            if not redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL

            # Heavier security check -- don't allow redirection to a different
            # host.
            elif netloc and netloc != request.get_host():
                redirect_to = settings.LOGIN_REDIRECT_URL

            # Okay, security checks complete. Log the user in.
            auth_login(request, form.get_user())

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            else:
                return HttpResponse(
                    u'У вас не работают cookies. Пожалуйста, включите их в браузере или очистите кеш браузера.')

            if request.user.is_authenticated():
                if wifi:
                    return render(request, 'accounts/frontend/to_wifi.html', {
                        'username': form.cleaned_data['username'],
                        'password': form.cleaned_data['password']
                    })

                orgs = participants_models.user_organizations(request.user)
                if orgs:
                    return redirect('http://help.kitap.tatar.ru')

            return redirect(redirect_to)
    else:
        form = authentication_form(request)

    request.session.set_test_cookie()

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template_name, context, current_app=current_app)


def from_wifi(request):
    if request.user.is_authenticated():
        orgs = participants_models.user_organizations(request.user)
        if orgs:
            return redirect('http://help.kitap.tatar.ru')
    else:
        return redirect('index:frontend:index')


@transaction.atomic()
def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                is_active=True,
            )
            user.set_password(form.cleaned_data['password'])
            user.save()
            group = Group.objects.get(name='users')
            user.groups.add(group)
            #            hash = md5_constructor(str(user.id) + form.cleaned_data['username']).hexdigest()
            #            confirm = RegConfirm(hash=hash, user_id=user.id)
            #            confirm.save()
            #            current_site = Site.objects.get(id=1)
            #            message = u'Поздравляем! Вы зарегистрировались на %s . Пожалуйста, пройдите по адресу %s для активации учетной записи.' % \
            #                      (current_site.domain, "http://" + current_site.domain + "/accounts/confirm/" + hash, )
            #
            #
            #            send_mail(u'Активация учетной записи ' + current_site.domain, message, 'system@'+current_site.domain,
            #                [form.cleaned_data['email']])

            return render(request, 'accounts/frontend/registration_done.html')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/frontend/registration.html', {
        'form': form
    })


@transaction.atomic
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
        # тут надо создать пользователя в лдапе
        user.is_active = True
        group = Group.objects.get(name='users')
        user.groups.add(group)
        user.save()
        confirm.delete()
    return render(request, 'accounts/frontend/registration_confirm.html')
