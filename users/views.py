from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from users.forms import RegisterForm, CustomRegForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def sign_up(request):
    
    form = CustomRegForm()
    
    if request.method == "POST":
        form = CustomRegForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Sign Up")
            return redirect('sign-up')

    return render(request, 'registration/register.html', {'form':form})


def sign_in(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        
    return render(request, 'registration/sign_in.html')


def logOut(request):

    if request.method == 'POST':
        logout(request)
        return redirect('sign-in')