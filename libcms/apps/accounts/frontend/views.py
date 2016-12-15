# -*- coding: utf-8 -*-
import urlparse

from django.conf import settings
from django.contrib.auth import (
    logout as auth_logout, )
from django.utils.translation import ugettext as _
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.utils.http import is_safe_url
from django.shortcuts import resolve_url
from django.db import transaction
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.messages.api import get_messages

from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.models import get_current_site

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
    ap_mac = request.GET.get('ap_mac', '')
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
                if ap_mac:
                    request.session['ap_mac'] = ap_mac
                    library = participants_models.get_org_by_ap_mac(ap_mac)
                    if library:
                        request.session['org_id'] = library.id
                if wifi:
                    username = form.cleaned_data['username']
                    suffix = '@tatar.ru'
                    if username.endswith(suffix):
                        username = username.replace(suffix, '')
                    username = u'EDU\\' + username
                    return render(request, 'accounts/frontend/to_wifi.html', {
                        'username': username,
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

    library = None
    if ap_mac:
        library = participants_models.get_org_by_ap_mac(ap_mac)
        if library:
            request.session['org_id'] = library.id
    context = {
        'form': form,
        'library': library,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)


    return render(request, template_name, context, current_app=current_app)


def logout(request, next_page=None,
           template_name='registration/logged_out.html',
           redirect_field_name=REDIRECT_FIELD_NAME,
           current_app=None, extra_context=None):
    """
    Logs out the user and displays 'You are logged out' message.
    """
    logout_idp_url = request.session.get('logout_idp_url')


    auth_logout(request)

    if next_page is not None:
        next_page = resolve_url(next_page)

    if (redirect_field_name in request.POST or
                redirect_field_name in request.GET):
        next_page = request.POST.get(redirect_field_name,
                                     request.GET.get(redirect_field_name))
        # Security check -- don't allow redirection to a different host.
        if not is_safe_url(url=next_page, host=request.get_host()):
            next_page = request.path

    if logout_idp_url:
        return redirect(logout_idp_url)

    if next_page:
        # Redirect to this page until the session has been cleared.
        return HttpResponseRedirect(next_page)

    current_site = get_current_site(request)
    context = {
        'site': current_site,
        'site_name': current_site.name,
        'title': _('Logged out')
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app


    return TemplateResponse(request, template_name, context)


def wifi(request):
    ap_mac = request.GET.get('ap_mac', '')
    if request.user.is_authenticated():
        if ap_mac:
            request.session['ap_mac'] = ap_mac
        orgs = participants_models.user_organizations(request.user)
        if orgs:
            return redirect('http://help.kitap.tatar.ru')
    return redirect('index:frontend:index')


@transaction.atomic()
def registration(request):
    return redirect('accounts:frontend:login')
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
