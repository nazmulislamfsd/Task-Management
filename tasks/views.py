from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm
from tasks.models import Employee, Task

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


def create_task(request):
    employees = Employee.objects.all()
    form = TaskModelForm()

    if request.method=='POST':
        form = TaskModelForm(request.POST)
        if form.is_valid():

            '''For django Model Form'''
            form.save()
            context = {"form":form, "message":'Task Added Successfully'}
            return render(request, "taskForm.html",context)



            '''For django Form'''
            # data = form.cleaned_data
            # title = data.get('title')
            # description = data.get('description')
            # due_date = data.get('due_date')
            # assigned_to = data.get('assigned_to')
            
            # task = Task.objects.create(title=title,description=description,due_date=due_date)

            # # assigne employee to task

            # for emp_id in assigned_to:
            #     employee = Employee.objects.get(id=emp_id)
            #     task.assigned_to_employee.add(employee)

            # return HttpResponse("Task added Successfully")


    context = {"form":form}
    return render(request, "taskForm.html",context)

def view_task(request):
    tasks = Task.objects.all()
    
    return render(request,"view_task.html",{"tasks":tasks})