from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def user_dashboard(request):
    return render(request, "dashboard/user_dashboard.html")

def manager_dashboard(request):
    return render(request, "dashboard/manager_dashboard.html")

def test(request):
    names = ["mahmud","ahmed","jhon","mahin"]
    count = 0
    for name in names:
        count+=1
    context = {
        "names":names,
        "age":18,
        "count":count
    }
    return render(request, "test.html", context)