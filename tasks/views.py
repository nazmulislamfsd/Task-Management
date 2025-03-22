from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    return HttpResponse("This is Home Page")

def contact(request):
    return HttpResponse("This is contact Page")

def viewTask(request):
    return HttpResponse("Hello, This is ViewTask Page")

def show_specific_task(request, id):
    print('id:' ,id)
    print('type:', type(id))
    return HttpResponse("This is specific task")