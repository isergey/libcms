# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404, redirect
from guardian.decorators import permission_required_or_403
from common.pagination import get_page
from django.contrib.auth.models import User, Group
from forms import UserForm, GroupForm


from django.contrib.auth import login, REDIRECT_FIELD_NAME

#@permission_required_or_403('accounts.view_users')
def index(request):
    print REDIRECT_FIELD_NAME
    return render(request, 'accounts/administration/index.html')






@permission_required_or_403('accounts.view_users')
def users_list(request):
    users_qs = User.objects.all().exclude(id=-1).order_by('-date_joined')
    users_page = get_page(request,  users_qs)

    return render(request, 'accounts/administration/user_list.html', {
        'users_page': users_page,
        'users': users_qs
    })




@permission_required_or_403('auth.add_user')
def create_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if form.cleaned_data['password']:
                user.set_password(form.cleaned_data['password'])
            user.save()
            if form.cleaned_data['groups']:
                user.groups = form.cleaned_data['groups']

            if form.cleaned_data['user_permissions']:
                user.user_permissions = form.cleaned_data['user_permissions']

            return redirect('accounts:administration:users_list')

    else:
        form = UserForm()
    return render(request, 'accounts/administration/create_user.html', {
        'form': form
    })





@permission_required_or_403('auth.change_user')
def edit_user(request, id):
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            if form.cleaned_data['password']:
                user.set_password(form.cleaned_data['password'])

            if form.cleaned_data['groups']:
                user.groups = form.cleaned_data['groups']
            else:
                user.groups.clear()

            if form.cleaned_data['user_permissions']:
                user.user_permissions = form.cleaned_data['user_permissions']
            else:
                user.user_permissions.clear()

            user.save()
            return redirect('accounts:administration:users_list')

    else:
        form = UserForm(instance=user)

    return render(request, 'accounts/administration/edit_user.html', {
        'form': form
    })





@permission_required_or_403('accounts.view_groups')
def groups_list(request):
    groups_page = get_page(request,  Group.objects.all())
    return render(request, 'accounts/administration/groups_list.html', {
        'groups_page': groups_page
    })





@permission_required_or_403('auth.add_group')
def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:administration:groups_list')
    else:
        form = GroupForm()
    return render(request, 'accounts/administration/create_group.html', {
        'form': form
    })





@permission_required_or_403('auth.change_group')
def edit_group(request, id):
    group = get_object_or_404(Group, id=id)
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            group = form.save(commit=False)

            if form.cleaned_data['permissions']:
                group.permissions = form.cleaned_data['permissions']
            else:
                group.permissions.clear()

            group.save()
            return redirect('accounts:administration:groups_list')
    else:
        form = GroupForm(instance=group)

    return render(request, 'accounts/administration/edit_group.html', {
        'form': form
    })


@permission_required_or_403('auth.delete_group')
def delete_group(request, id):
    group = get_object_or_404(Group, id=id)
    group.delete()
    return redirect('accounts:administration:groups_list')

