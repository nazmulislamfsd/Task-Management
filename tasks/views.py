from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm
from tasks.models import Employee, Task, Task_detail, Project
from datetime import date
from django.db.models import Q, Count, Max, Min, Sum, Avg

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
    # tasks = Task.objects.all()
    # tasks = Task.objects.filter(status="PENDING")
    # tasks = Task.objects.filter(due_date=date.today())
    # tasks = Task_detail.objects.exclude(priority="L")
    # tasks = Task.objects.filter(id__gt=5)
    # tasks = Task.objects.filter(title__contains="paper")
    # tasks = Task_detail.objects.select_related('task').all()
    # tasks = Task.objects.filter(description__icontains = "c", status = "PENDING") '''AND Operation'''
    # tasks = Task.objects.filter(Q(status="PENDING") | Q(status="IN_PROGRESS"))
    # tasks = Task.objects.select_related('project').all()
    # tasks = Task.objects.select_related('details').all()
    # tasks = Task_detail.objects.select_related('task').all()
    # tasks = Task_detail.objects.select_related('task').all()
    # projects = Project.objects.prefetch_related('allTask').all()
    # countTask = Task.objects.aggregate(num_count= Count("id"))

    projects = Project.objects.annotate(num_task = Count("allTask")).order_by("id")
    

    return render(request,"view_task.html",{"projects":projects})