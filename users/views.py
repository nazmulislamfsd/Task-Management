from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from users.forms import RegisterForm, CustomRegForm, LoginForm, AssignRoleForm, CreateGroupForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Prefetch
# Create your views here.

# Test for users
def is_admin(user):
    return user.groups.filter(name='Admin').exists()


def sign_up(request):
    
    form = CustomRegForm()
    
    if request.method == "POST":
        form = CustomRegForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.set_password(form.cleaned_data.get('password1'))
            user.save()
            messages.success(request, "A confirmation mail. please check your email")
            return redirect('sign-in')

    return render(request, 'registration/register.html', {'form':form})


def sign_in(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        
    return render(request, 'registration/sign_in.html', {'form':form})

@login_required
def logOut(request):

    if request.method == 'POST':
        logout(request)
        return redirect('sign-in')
    
    

def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('sign-in')
        else:
            return HttpResponse('Invalid id or token')
    except User.DoesNotExist:
        return HttpResponse('user not found!!')
    

@user_passes_test(is_admin, login_url='no-permission')
def admin_dashboard(request):
    users = User.objects.prefetch_related(
        Prefetch('groups', queryset=Group.objects.all(), to_attr='all_groups')
    )

    for user in users:
        if user.all_groups:
            user.group_name = user.all_groups[0].name
        else:
            user.group_name = "No groups assign"

    return render(request, 'admin/dashboard.html', {'users':users})


@user_passes_test(is_admin, login_url='no-permission')
def assign_role(request, user_id):
    form = AssignRoleForm()
    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear() # remove all roles
            user.groups.add(role)
            messages.success(request, f"User {user.username} has been assign to the {role} role.")
            return redirect('admin-dashboard')
        
    return render(request, 'admin/assign_role.html', {"form":form})


@user_passes_test(is_admin, login_url='no-permission')
def create_group(request):

    form = CreateGroupForm()

    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request, f"Group {group.name} has been created Successfully.")
            return redirect('create-group')

    return render(request, 'admin/create_group.html', {"form":form})


@user_passes_test(is_admin, login_url='no-permission')
def group_list(request):

    groups = Group.objects.prefetch_related('permissions')
    return render(request, 'admin/group_list.html', {"groups":groups})