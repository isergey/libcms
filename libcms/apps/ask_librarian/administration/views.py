# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import transaction
from django.utils.translation import ugettext as _
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, Http404, urlresolvers
from django.http import HttpResponseForbidden
from guardian.decorators import permission_required_or_403
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.sites.models import get_current_site
from common.pagination import get_page
from django.utils.translation import get_language
from common.pagination import get_page
from django.db.models import Q
from ..models import Category, CategoryTitle,  Question, QuestionManager, Recomendation
from forms import CategoryForm, CategoryTitleForm,  AnswerQuestionForm, ToManagerForm



#@permission_required_or_403('accounts.view_users')
@login_required
def index(request):
    manager = QuestionManager.get_manager(request.user)
    if not manager and not request.user.is_superuser:
        return HttpResponseForbidden()

    return render(request, 'ask_librarian/administration/index.html')



@login_required
def questions_list(request, my=None):
    manager = QuestionManager.get_manager(request.user)
    if not manager and not request.user.is_superuser and not request.user.has_module_perms('ask_librarian'):
        return HttpResponse(u'Вы не можете обрабатывать вопросы')

    if manager:
        manager.user = request.user

    status = request.GET.get('status', 0)

    if my:
        questions_page = get_page(request, Question.objects.filter(status=status, manager=manager).exclude(manager=None).order_by('-create_date'), 10)
        questions_page.object_list = list(questions_page.object_list)
        for question in questions_page.object_list:
            question.manager = manager
    else:
        questions_page = get_page(request, Question.objects.filter(status=status).order_by('-create_date'), 10)
        questions_page.object_list = list(questions_page.object_list)
        md = {}
        for question in questions_page.object_list:
            if question.manager_id:
                md[question.manager_id] = None

        managers = QuestionManager.objects.select_related('user').filter(id__in=md.keys())
        for manager_item in managers:
            if manager_item.id in md:
                md[manager_item.id] = manager_item

        for question in questions_page.object_list:
            if question.manager_id:
                question.manager = md[question.manager_id]


    return render(request, 'ask_librarian/administration/questions_list.html', {
            'questions_page': questions_page,
        })


@login_required
@transaction.atomic
def questions_to_process(request, id):
    manager = QuestionManager.get_manager(request.user)
    if not manager:
        return HttpResponse(u'Вы не можете обрабатывать вопросы')
    try:
        question = Question.objects.select_for_update().get(Q(id=id), ~Q(status=2))
    except Question.DoesNotExist:
        raise Http404()
    question.take_to_process(manager)
    return redirect('ask_librarian:administration:questions_list')


@login_required
@transaction.atomic
@permission_required_or_403('ask_librarian.assign_to_manager')
def assign_to_manager(request, question_id):
    if request.method == 'POST':
        to_manager_form = ToManagerForm(request.POST)
        if to_manager_form.is_valid():
            try:
                question = Question.objects.select_for_update().get(Q(id=question_id), ~Q(status=2))
            except Question.DoesNotExist:
                raise Http404(u'Вопрос не может быть присвоен менеджеру. Его не существует, либо он уже обрабатывается')

            question.take_to_process(to_manager_form.cleaned_data['manager'])
            return redirect('ask_librarian:administration:questions_list')
    else:
        return HttpResponse(u'Only POST request')


@login_required
def question_detail(request, id):
    manager = QuestionManager.get_manager(request.user)
    if not manager and not request.user.is_superuser:
        return HttpResponse(u'Вы не можете обрабатывать вопросы')

    question = get_object_or_404(Question, id=id)
#    recomendations = Recomendation.objects.filter(id=id)

    to_manager_form = ToManagerForm()
    return render(request, 'ask_librarian/administration/question_detail.html', {
        'question': question,
        'to_manager_form': to_manager_form
#        'recomendations': recomendations
    })

@login_required
def question_answer(request, id):
    manager = QuestionManager.get_manager(request.user)
    if not manager:
        return HttpResponse(u'Вы не можете обрабатывать вопросы')

    question = get_object_or_404(Question, id=id)
    if question.is_ready():
        return HttpResponse(u'Ответ на вопрос уже дан.')
    if request.method == 'POST':
        form = AnswerQuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            if question.is_new():
                question.take_to_process(manager, commit=False)
            question.close_process()
            if question.email:
                domain = settings.SITE_DOMAIN
                from_mail = settings.DEFAULT_FROM_EMAIL
                send_mail(u"Спроси библиотекаря",
                    u'Ваш вопрос был обработан. Вы можете посмотреть ответ по адресу http://%s%s' %
                    (domain, urlresolvers.reverse('ask_librarian:frontend:detail', args=(question.id,))),
                    from_mail,
                    [question.email],
                    #                    fail_silently=True
                )
            return redirect('ask_librarian:administration:question_detail', id=id)
    else:
        form = AnswerQuestionForm(instance=question)

    return render(request, 'ask_librarian/administration/question_answer.html', {
        'question': question,
        'form': form
    })

@login_required
def question_edit(request, id):
    question = get_object_or_404(Question, id=id)
    if (question.manager and not question.manager.user_id == request.user.id) and not request.user.is_superuser:
        return HttpResponse(u'Вы не можете обрабатывать вопросы')


    if request.method == 'POST':
        form = AnswerQuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('ask_librarian:administration:question_detail', id=id)
    else:
        form = AnswerQuestionForm(instance=question)

    return render(request, 'ask_librarian/administration/question_edit.html', {
        'question': question,
        'form': form
    })


@login_required
@permission_required_or_403('ask_librarian.delete_question')
@transaction.atomic
def question_delete(request, id):
    manager = QuestionManager.get_manager(request.user)
    if not manager:
        return HttpResponse(u'Вы не можете обрабатывать вопросы')

    question = get_object_or_404(Question, id=id)
    question.delete()
    return redirect(request.META.get('HTTP_REFERER', 'ask_librarian:administration:questions_list'))


@login_required
def categories_list(request):
    if not request.user.has_module_perms('ask_librarian'):
        return HttpResponseForbidden()
    nodes = list(Category.objects.all())
    lang=get_language()[:2]
    category_titles = CategoryTitle.objects.filter(category__in=nodes, lang=lang)
    nd = {}
    for node in nodes:
        nd[node.id] = node

    for category_title in category_titles:
        nd[category_title.category_id].t_title = category_title

    return render(request, 'ask_librarian/administration/categories_list.html', {
        'nodes': nodes,
#        'menu': menu
    })


@login_required
@permission_required_or_403('ask_librarian.add_category')
@transaction.atomic
def category_create(request, parent=None):

    if  parent:
        parent = get_object_or_404(Category, id=parent)

    if request.method == 'POST':
        category_form = CategoryForm(request.POST,prefix='category_form')

        category_title_forms = []
        for lang in settings.LANGUAGES:
            category_title_forms.append({
                'form':CategoryTitleForm(request.POST,prefix='category_title_' + lang[0]),
                'lang':lang[0]
            })

        if category_form.is_valid():

            category = category_form.save(commit=False)
            category.parent = parent
            category.save()

            valid = False
            for category_title_form in category_title_forms:
                valid = category_title_form['form'].is_valid()
                if not valid:
                    break
            if valid:
                for category_title_form in category_title_forms:
                    category_title = category_title_form['form'].save(commit=False)
                    category_title.lang = category_title_form['lang']
                    category_title.category = category
                    category_title.save()
                return redirect('ask_librarian:administration:categories_list')
    else:
        category_form = CategoryForm(prefix="category_form")
        category_title_forms = []
        for lang in settings.LANGUAGES:
            category_title_forms.append({
                'form':CategoryTitleForm(prefix='category_title_' + lang[0]),
                'lang':lang[0]
            })

    return render(request, 'ask_librarian/administration/create_category.html', {
        'category_form': category_form,
        'category_title_forms': category_title_forms,
    })



@login_required
@permission_required_or_403('ask_librarian.change_category')
@transaction.atomic
def category_edit(request, id):

    category = get_object_or_404(Category, id=id)
    category_titles = CategoryTitle.objects.filter(category=category)

    category_titles_langs = {}
    for lang in settings.LANGUAGES:
        category_titles_langs[lang] = None


    for category_title in category_titles:
        category_titles_langs[category_title.lang] = category_title

    if request.method == 'POST':
        category_form = CategoryForm(request.POST,prefix='category_form', instance=category)

        category_title_forms = []
        for lang in settings.LANGUAGES:
            category_title_forms.append({
                'form':CategoryTitleForm(request.POST,prefix='category_title_' + lang[0]),
                'lang':lang[0]
            })

        if category_form.is_valid():

            category = category_form.save(commit=False)
            category.parent = parent
            category.save()

            valid = False
            for category_title_form in category_title_forms:
                valid = category_title_form['form'].is_valid()
                if not valid:
                    break
                #            print 'valid', valid
            if valid:
                for category_title_form in category_title_forms:
                    category_title = category_title_form['form'].save(commit=False)
                    category_title.lang = category_title_form['lang']
                    category_title.category = category
                    category_title.save()
                return redirect('ask_librarian:administration:categories_list')
    else:
        category_form = CategoryForm(prefix="category_form")
        category_title_forms = []
        for lang in settings.LANGUAGES:
            category_title_forms.append({
                'form':CategoryTitleForm(prefix='category_title_' + lang[0]),
                'lang':lang[0]
            })

    return render(request, 'ask_librarian/administration/create_category.html', {
        'category_form': category_form,
        'category_title_forms': category_title_forms,
        })




@login_required
@permission_required_or_403('ask_librarian.change_category')
@transaction.atomic
def category_edit(request, id,):
    category = get_object_or_404(Category, id=id)
    category_titles = CategoryTitle.objects.filter(category=category)

    category_titles_langs = {}
    for lang in settings.LANGUAGES:
        category_titles_langs[lang] = None


    for category_title in category_titles:
        category_titles_langs[category_title.lang] = category_title



    if request.method == 'POST':
        category_form = CategoryForm(request.POST, prefix='category_form', instance=category)
        category_title_forms = []
        for lang in settings.LANGUAGES:
            if lang in category_titles_langs:
                lang = lang[0]
                if lang in category_titles_langs:
                    category_title_forms.append({
                        'form':CategoryTitleForm(request.POST,prefix='category_title_' + lang, instance=category_titles_langs[lang]),
                        'lang':lang
                    })
                else:
                    category_title_forms.append({
                        'form':CategoryTitleForm(request.POST,prefix='category_title_' + lang),
                        'lang':lang
                    })

        valid = False
        for category_title_form in category_title_forms:
            valid = category_title_form['form'].is_valid()
            if not valid:
                break


        if not category_form.is_valid():
            valid = False

        if valid:
            category = category_form.save()
            for category_title_form in category_title_forms:
                category_title = category_title_form['form'].save(commit=False)
                category_title.category = category
                category_title.lang = category_title_form['lang']
                category_title.save()

            if not category.is_leaf_node():
                dcategorys = category.get_descendants()
                for dcategory in dcategorys:
                    dcategory.save()

            return redirect('ask_librarian:administration:categories_list')


    else:
        category_form = CategoryForm(prefix="category_form", instance=category)
        category_title_forms = []
        for lang in settings.LANGUAGES:
            lang = lang[0]
            if lang in category_titles_langs:
                category_title_forms.append({
                    'form':CategoryTitleForm(prefix='category_title_' + lang, instance=category_titles_langs[lang]),
                    'lang':lang
                })
            else:
                category_title_forms.append({
                    'form':CategoryTitleForm(prefix='category_title_' + lang),
                    'lang':lang
                })

    return render(request, 'ask_librarian/administration/edit_category.html', {
        'category_form': category_form,
        'category_title_forms': category_title_forms,
        'category': category
    })



#
@login_required
@permission_required_or_403('ask_librarian.delete_category')
def category_delete(request, id):
    category = get_object_or_404(Category, id=id)
    category.delete()
    return redirect('ask_librarian:administration:categories_list')


def category_up(request, id):
    category = get_object_or_404(Category, id=id)
    category.up()
    return redirect('ask_librarian:administration:categories_list')

def category_down(request, id):
    category = get_object_or_404(Category, id=id)
    category.down()
    return redirect('ask_librarian:administration:categories_list')


