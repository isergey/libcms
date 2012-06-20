# -*- coding: utf-8 -*-
from django.core.cache import cache
from django import template
from django.utils.translation import get_language
from ..models import Category, CategoryTitle, Question, QuestionManager

register = template.Library()
@register.inclusion_tag('ask_librarian/tags/drow_categories_tree.html', takes_context=True)
def drow_categories_tree(context):
    path = context['request'].META['PATH_INFO']

    nodes = list(Category.objects.all())
    lang=get_language()[:2]
    nodes_titles = CategoryTitle.objects.filter(category__in=nodes, lang=lang)
    nd = {}
    for node in nodes:
        nd[node.id] = node

    for node_title in nodes_titles:
        nd[node_title.category_id].node_title = node_title

    if not nodes_titles:
        nodes = []
    return ({
        'nodes': nodes,
        'path': path
    })
@register.simple_tag
def get_question_status_count(status, user=None):
    if user:
        try:
            manager = QuestionManager.objects.get(user=user)
            return  Question.objects.filter(status=status, manager=manager).count()
        except QuestionManager.DoesNotExist:
            return 0
    return  Question.objects.filter(status=status).count()

@register.simple_tag
def get_question_category_count(category):
    category_count = cache.get('ask_librarian_frontend_category_count'+str(category.id), None)
    if category_count == None:
        categories  = []
        categories.append(category.id)
        descendants = category.get_descendants()
        for descendant in descendants:
            categories.append(descendant.id)
        category_count =   Question.objects.filter(category__in=categories, status=1).count()
        cache.set('ask_librarian_frontend_category_count'+str(category.id), category_count)
    return category_count