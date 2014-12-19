# encoding: utf-8
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.db import transaction

from .. import models
from forms import get_subscriber_form, EmailForm

@transaction.atomic()
def index(request):
    email = ''
    groups = models.Group.objects.all()
    user = None
    if request.user.is_authenticated():
        email = request.user.email
        user = request.user
    # subscribes = Subscribe.objects.filter(is_active=True)
    if request.method == 'POST':
        email_form = EmailForm(request.POST)
        forms = []
        for group in groups:
            SubscriberForm = get_subscriber_form(models.Subscribe.objects.filter(group=group, is_active=True))
            forms.append({
                'group': group,
                'form': SubscriberForm(request.POST, prefix=group.id)
            })
        subscribes = []
        is_valid = True
        for form in forms:
            subscriber_form = form['form']
            if not subscriber_form.is_valid():
                is_valid = False
            else:
                subscribes += subscriber_form.cleaned_data['subscribes']

        if not email_form.is_valid():
            is_valid = False

        if is_valid:
            subscribes = set(subscribes)
            try:
                subscriber = models.Subscriber.objects.get(email=email_form.cleaned_data['email'])
                exists_subscribes = list(subscriber.subscribe.all())
                for subscribe in subscribes:
                    if subscribe not in exists_subscribes:
                        subscriber.subscribe.add(subscribe)

                for exists_subscribe in exists_subscribes:
                    if exists_subscribe not in subscribes:
                        subscriber.subscribe.remove(exists_subscribe)

            except models.Subscriber.DoesNotExist:
                subscriber = models.Subscriber(user=user, email=email)
                subscriber.save()
                for subscribe in set(subscribes):
                    subscriber.subscribe.add(subscribe)
            return redirect('subscribe:frontend:index')
    else:
        email_form = EmailForm(initial={
            'email': email
        })
        forms = []
        for group in groups:
            initial_subscribes = []
            if email:
                try:
                    subscriber = models.Subscriber.objects.get(email=email)
                    initial_subscribes = subscriber.subscribe.all()
                except models.Subscriber.DoesNotExist:
                    pass
            SubscriberForm = get_subscriber_form(models.Subscribe.objects.filter(group=group, is_active=True))
            forms.append({
                'group': group,
                'form': SubscriberForm(prefix=group.id, initial={
                    'subscribes': initial_subscribes
                })
            })
    return render(request, 'subscribe/frontend/index.html', {
        'forms': forms,
        'email_form': email_form
    })


def subscription_detail(request, id):
    subscribe = get_object_or_404(models.Subscribe, id=id, is_active=True)
    user_subscribed = False
    key = ''
    email = ''
    if request.user.is_authenticated():
        try:
            subscriber = models.Subscriber.objects.get(email=request.user.email)
            user_subscribed = True
            key = models.generate_key(subscriber.id, subscriber.email)
            email = subscriber.email
        except models.Subscriber.DoesNotExist:
            pass


    return render(request, 'subscribe/frontend/subscribe_detail.html', {
        'subscribe': subscribe,
        'user_subscribed': user_subscribed,
        'key': key,
        'email': email
    })

@transaction.atomic()
def subscribe(request, id):
    subscribe = get_object_or_404(models.Subscribe, id=id, is_active=True)
    email = u''
    if request.user.is_authenticated():
        user = request.user
        email = user.email

    if request.method == 'POST':
        form = models.SubscribeForm(request.POST)
        if form.is_valid():
            subscriber = models.Subscriber(email=form.cleaned_data['email'], subscribe=subscribe)
            subscriber.save()
            return render(request, 'subscribe/frontend/to_subscribe_success.html', {
                'subscribe': subscribe,
                'email': subscriber.email
            })

    else:
        form = models.SubscribeForm(initial={
            'email': email,
            'subscribe': subscribe.id
        })
    return render(request, 'subscribe/frontend/to_subscribe.html', {
        'subscribe': subscribe,
        'form': form,
    })

@transaction.atomic()
def unsubscribe(request, id):
    subscribe = get_object_or_404(models.Subscribe, id=id)
    confirm = request.GET.get('confirm', None)
    email = request.GET.get('email', None)
    key = request.GET.get('key', None)
    if not email and request.user.is_authenticated():
        email = request.user.email

    if not email:
        return HttpResponse(u'Неправильные параметры запроса')

    subscriber = get_object_or_404(models.Subscriber, subscribe=subscribe, email=email)

    if key != models.generate_key(subscriber.id, email):
        return HttpResponse(u'Неправильная подпись заявки')
    if confirm:
        subscriber.delete()
        return render(request, 'subscribe/frontend/unsubscribe_success.html', {
            'subscribe': subscribe,
            'email': email
        })
    return render(request, 'subscribe/frontend/unsubscribe.html', {
        'subscribe': subscribe,
        'email': email
    })


def send_letters_req(request):
    models.send_letters()
    return HttpResponse('Ok')


def send_emails_req(request):
    models.send_to_email()
    return HttpResponse('Ok')