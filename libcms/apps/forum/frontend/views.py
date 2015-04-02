# -*- coding: utf-8 -*-
import postmarkup
import json
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, Http404
from django.http import HttpResponseForbidden
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from guardian.core import ObjectPermissionChecker
from guardian.models import GroupObjectPermission
from guardian.forms import GroupObjectPermissionsForm
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from guardian.shortcuts import get_perms_for_model, get_perms, remove_perm, assign, get_groups_with_perms
from django.core.paginator import Paginator, InvalidPage
from core.forms import get_permissions_form
from forum.models import Forum, Topic, Article
from forms import ArticleForm, TopicForm, ForumForm


postmarkup_render = postmarkup.create()

@login_required
def forums(request):
    if not request.user.has_perms(['forum.can_views_forums']):
        return HttpResponseForbidden()

    forums = Forum.objects.all()
    if request.method == 'POST':
        if not request.user.has_perms(['forum.add_forum']):
            return HttpResponseForbidden()
        form = ForumForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('forum:frontend:forums')
    else:
        form = ForumForm()


    last_articles_dict = {}
    last_topics_dict = {}
    last_forums_dict = {}
    if request.user.has_perms(['forum.can_hide_articles']):
        last_articles = Article.objects.filter(deleted=False).order_by('-created')[:10]
    else:
        last_articles = Article.objects.filter(public=True, deleted=False).order_by('-created')[:10]

    for last_article in last_articles:
        last_articles_dict[last_article.id] = {'article': last_article}
        last_topics_dict[last_article.topic_id] = None

    topics = Topic.objects.filter(id__in=last_topics_dict.keys())

    for topic in topics:
        last_topics_dict[topic.id] = topic
        last_forums_dict[topic.forum_id] = None

    lforums = Forum.objects.filter(id__in=last_forums_dict.keys())

    for lforum in lforums:
        last_forums_dict[lforum.id] = lforum

    for last_article in last_articles:
        last_articles_dict[last_article.id]['topic']=last_topics_dict[last_article.topic_id]
        last_articles_dict[last_article.id]['forum'] = last_forums_dict[last_topics_dict[last_article.topic_id].forum_id]


    last_articles_list =  []
    for last_article in last_articles:
        last_articles_list.append(last_articles_dict[last_article.id])

    return render(request, 'forum/frontend/forums.html', {
        'forums': forums,
        'form': form,
        'last_articles': last_articles_list
    })



@login_required
@transaction.atomic
def forum_close(request, id):
    if not request.user.has_perms(['forum.can_close_forums']):
        return HttpResponseForbidden()

    forum = get_object_or_404(Forum, id=id)
    forum.closed = True
    forum.save()

    if request.is_ajax():
        return HttpResponse(u'{"status":"ok"}')
    else:
        return redirect('forum:frontend:forums', slug=forum.slug)

@login_required
@transaction.atomic
def forum_open(request, id):
    if not request.user.has_perms(['forum.can_close_forums']):
        return HttpResponseForbidden()

    forum = get_object_or_404(Forum, id=id)
    forum.closed = False
    forum.save()

    if request.is_ajax():
        return HttpResponse(u'{"status":"ok"}')
    else:
        return redirect('forum:frontend:forums', slug=forum.slug)


@login_required
@transaction.atomic
def forum_delete(request, id):
    if not request.user.has_perms(['forum.delete_forum']):
        return HttpResponseForbidden()

    forum = get_object_or_404(Forum, id=id)
    forum.delete()

    if request.is_ajax():
        return HttpResponse(u'{"status":"ok"}')
    else:
        return redirect('forum:frontend:forums')



@login_required
def forum_topics(request, slug):


    forum = get_object_or_404(Forum, slug=slug)



    if not request.user.has_perm("can_view_topics", forum):
        return HttpResponseForbidden()

    topics_qs = Topic.objects.filter(forum=forum)
    # пагинация сообщений в топике форума
    paginator = Paginator(topics_qs, 20)
    page_num = request.GET.get('page', '1')

    if page_num == 'last':
        page_num = paginator.num_pages
    try:
        page = paginator.page(int(page_num))
    except (InvalidPage, ValueError):
        raise Http404()

    #    topics = paginator.object_list
    if request.method == 'POST':

        if forum.closed:
            return HttpResponseForbidden()

        topic_form = TopicForm(request.POST, prefix='topic')
        article_form = ArticleForm(request.POST, prefix='article')

        if topic_form.is_valid() and article_form.is_valid():
            if not request.user.has_perm("can_create_topics", forum):
                return HttpResponseForbidden()

            topic = topic_form.save(commit=False)

            if request.user.has_perm('can_hide_topics', forum):
                topic.public = True
            else:
                topic.public = False

            topic.forum = forum
            topic.save()
            article = article_form.save(commit=False)

            article.public = True

            article.author = request.user
            article.topic = topic
            article.save()

            groups =  get_groups_with_perms(forum, attach_perms=True)
            for group in groups:
                if  u"can_create_topics" in  groups[group]:
                    assign(u"can_add_articles", group, topic)
                #                    assign(u"can_view_articles", group, topic)
                if  u"can_view_topics" in  groups[group]:
                    assign(u"can_view_articles", group, topic)

            if request.user.has_perm('can_hide_topics', forum):
                return redirect('forum:frontend:articles', slug=forum.slug, id=topic.id)
            else:
                return redirect('forum:frontend:topics', slug=forum.slug)
    else:
        topic_form = TopicForm(prefix='topic')
        article_form = ArticleForm(prefix='article')
    return render(request, 'forum/frontend/topics.html', {
        'forum': forum,
        #        'topics': topics,
        'topic_form': topic_form,
        'article_form': article_form,
        'page': page,
        })

@login_required
def topic_delete(request, id):
    if not request.user.has_perms(['forum.can_delete_topics']):
        return HttpResponseForbidden()

    topic = get_object_or_404(Topic, id=id)
    topic.delete()

    if request.is_ajax():
        return HttpResponse(u'{"status":"ok"}')
    else:
        return redirect('forum:frontend:topics', slug=topic.forum.slug)

@login_required
def topic_close(request, id):
    if not request.user.has_perms(['forum.can_close_topics']) and not request.user.has_perms(['forum.can_close_own_topics']):
        return HttpResponseForbidden()

    topic = get_object_or_404(Topic, id=id)
    topic.closed = True
    topic.save()

    if request.is_ajax():
        return HttpResponse(u'{"status":"ok"}')
    else:
        return redirect('forum:frontend:topics', slug=topic.forum.slug)

@login_required
def topic_open(request, id):
    if not request.user.has_perms(['forum.can_close_topics']):
        return HttpResponseForbidden()

    topic = get_object_or_404(Topic, id=id)
    topic.closed = False
    topic.save()

    if request.is_ajax():
        return HttpResponse(u'{"status":"ok"}')
    else:
        return redirect('forum:frontend:topics', slug=topic.forum.slug)


@login_required
def topic_articles(request, slug, id, aid=None, eid=None):

    topic = get_object_or_404(Topic, id=id)
    if not request.user.has_perm("can_view_articles", topic):
        return HttpResponseForbidden()

    if request.user.has_perm("can_hide_articles", topic):
        articles_qs = Article.objects.select_related('author').filter(topic=topic)
    else:
        articles_qs = Article.objects.select_related('author').filter(topic=topic, public=True)

    # пагинация сообщений в топике форума
    paginator = Paginator(articles_qs, 20)
    page_num = request.GET.get('page', '1')

    if page_num == 'last':
        page_num = paginator.num_pages
    try:
        page = paginator.page(int(page_num))
    except (InvalidPage, ValueError):
        raise Http404()

    # отрисовка сообщений в bbcode в html
    articles = page.object_list
    for article in articles:
        article.text = postmarkup_render(article.text)

    # если пользователь нажал на цитирование
    if aid:
        if request.user.has_perm("can_hide_articles", topic):
            quote_article = get_object_or_404(Article, id=aid)
        else:
            quote_article = get_object_or_404(Article, id=aid, public=True)
    else:
        quote_article = None

    # если пользователь редактирует свое сообщение
    if eid:
        edit_article = get_object_or_404(Article, id=eid)
        if not request.user.has_perm("can_change_articles", topic):
            return  HttpResponseForbidden()
    else:
        edit_article = None

    if request.method == 'POST':
        if topic.closed:
            return HttpResponseForbidden()

        if edit_article:
            form = ArticleForm(request.POST, instance=edit_article)
        else:
            form = ArticleForm(request.POST)

        if form.is_valid():
            if edit_article:
                article = form.save(commit=False)
                if request.user.has_perm("can_hide_articles", topic) or request.user.has_perm("can_publish_own_articles", topic):
                    article.public = True
                else:
                    article.public = False
                article.save()
                return redirect('forum:frontend:articles', slug=topic.forum.slug, id=topic.id)

            article = form.save(commit=False)
            if request.user.has_perm("can_hide_articles", topic) or request.user.has_perm("can_publish_own_articles", topic) :
                article.public = True

            article.author = request.user
            article.topic = topic
            if quote_article:
                article.text = u"[quote][b]%s[/b]:\n%s[/quote] %s" % (
                    quote_article.author.username, quote_article.text, article.text)

            article.save()

            return redirect('forum:frontend:articles', slug=topic.forum.slug, id=topic.id)
    else:
        if edit_article:
            form = ArticleForm(instance=edit_article)
        else:
            form = ArticleForm()

    if quote_article:
        quote_article.text = postmarkup_render(quote_article.text)
    if edit_article:
        edit_article.text = postmarkup_render(edit_article.text)

    return render(request, 'forum/frontend/articles.html', {
        'topic': topic,
        'articles': articles,
        'quote_article': quote_article,
        'edit_article': edit_article,
        'form': form,
        'page': page

    })


@login_required
def article_delete(request, id):
    article = get_object_or_404(Article, id=id)
    topic =  article.topic

    if not request.user.has_perm("can_delete_articles", topic):
        return HttpResponseForbidden()

    article.delete()

    if request.is_ajax():
        return HttpResponse(u'{"status":"ok"}')
    else:
        return redirect('forum:frontend:articles', slug=topic.forum.slug, id=topic.id)

@login_required
def article_hide(request, id):
    article = get_object_or_404(Article, id=id)

    if not request.user.has_perm("can_hide_articles", article.topic):
        return HttpResponseForbidden()


    article.public = False
    article.save()

    if request.is_ajax():
        return HttpResponse(u'{"status":"ok"}')
    else:
        return redirect('forum:frontend:articles', slug=article.topic.forum.slug, id=article.topic.id)


@login_required
def article_show(request, id):
    article = get_object_or_404(Article, id=id)
    if not request.user.has_perm("can_hide_articles", article.topic):
        return HttpResponseForbidden()

    article = get_object_or_404(Article, id=id)
    article.public = True
    article.save()

    if request.is_ajax():
        return HttpResponse(u'{"status":"ok"}')
    else:
        return redirect('forum:frontend:articles', slug=article.topic.forum.slug, id=article.topic.id)



def article_preview(request):
    if request.method == 'POST':
        text = request.POST.get('text', u' ')
        result = {'text':postmarkup_render(text)}
        return HttpResponse(json.dumps(result, ensure_ascii=False))

    return HttpResponse(u'{}')





@login_required
def forum_permissions(request, id):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    forum = get_object_or_404(Forum, id=id)
    groups = Group.objects.all()


    return render(request, 'forum/frontend/permissions.html', {
        'forum': forum,
        'groups': groups,
        })




@login_required
@transaction.atomic
def assign_forum_permissions(request, id, gid):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    obj = get_object_or_404(Forum, id=id)
    group = get_object_or_404(Group, id=gid)
    obj_permissions  = get_perms_for_model(Forum).exclude(codename__in=['add_forum', 'can_views_forums'])

    ctype = ContentType.objects.get_for_model(obj)
    perms = []
    for group_perm in GroupObjectPermission.objects.filter(group=group,content_type=ctype, object_pk=obj.id):
        perms.append(group_perm.permission)
        #print perms
    PermissionsForm = get_permissions_form(obj_permissions.select_related(), initial=perms)
    if request.method == 'POST':
        form = PermissionsForm(request.POST)
        if form.is_valid():
            for perm in obj_permissions:
                remove_perm(perm.codename, group, obj)

            for perm in  form.cleaned_data['perms']:
                assign(perm.codename, group, obj )

    else:
        form = PermissionsForm()


    return render(request, 'forum/frontend/edit_permissions.html', {
        'forum': obj,
        'group': group,
        'form':form,
        })



@login_required
def topic_permissions(request, id):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    topic = get_object_or_404(Topic, id=id)
    groups = Group.objects.all()


    return render(request, 'forum/frontend/topic_permissions.html', {
        'topic': topic,
        'groups': groups,
        })



@login_required
@transaction.atomic
def assign_topic_permissions(request, id, gid):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    obj = get_object_or_404(Topic, id=id)
    group = get_object_or_404(Group, id=gid)
    obj_permissions  = get_perms_for_model(Topic).exclude(codename__in=['add_topic', ])

    ctype = ContentType.objects.get_for_model(obj)
    perms = []
    for group_perm in GroupObjectPermission.objects.filter(group=group,content_type=ctype, object_pk=obj.id):
        perms.append(group_perm.permission)

    PermissionsForm = get_permissions_form(obj_permissions.select_related(), initial=perms)

    if request.method == 'POST':
        form = PermissionsForm(request.POST)
        if form.is_valid():
            for perm in obj_permissions:
                remove_perm(perm.codename, group, obj)

            for perm in  form.cleaned_data['perms']:
                assign(perm.codename, group, obj )

    else:
        form = PermissionsForm()


    return render(request, 'forum/frontend/edit_topic_permissions.html', {
        'topic': obj,
        'group': group,
        'form':form,
        })