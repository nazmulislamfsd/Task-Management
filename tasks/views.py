from django.shortcuts import render, redirect
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm, Task_detailModelform
from tasks.models import Employee, Task, Task_detail, Project
from datetime import date
from django.db.models import Q, Count, Max, Min, Sum, Avg
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required

# Create your views here.
# -------------------------

def is_manager(user):
    return user.groups.filter(name='Manager').exists()

def is_employee(user):
    return user.groups.filter(name='Employee').exists()

# -------------------------
@user_passes_test(is_employee, login_url='no-permission')
def employee_dashboard(request):
    return render(request, "dashboard/employee_dashboard.html")

@user_passes_test(is_manager, login_url='no-permission')
def manager_dashboard(request):
    
    # getting task count
    # total_task = tasks.count()
    # completed_task = Task.objects.filter(status="COMPLETED").count()
    # in_progress_task = Task.objects.filter(status="IN_PROGRESS").count()
    # pending_task = Task.objects.filter(status="PENDING").count()

    # counts = {
    #     "total":total_task,
    #     "completed":completed_task,
    #     "progress":in_progress_task,
    #     "pending":pending_task
    # }
    type = request.GET.get('type','all')
    
    base_query = Task.objects.select_related('details').prefetch_related('assigned_to')
    
    if type=='complete':
        tasks = base_query.filter(status="COMPLETED")
    elif type == 'in_progress':
        tasks = base_query.filter(status="IN_PROGRESS")
    elif type == 'pending':
        tasks = base_query.filter(status="PENDING")
    elif type == 'all':
        tasks = base_query.all()
    

    counts = Task.objects.aggregate(
        total = Count('id'),
        completed = Count('id', filter=Q(status="COMPLETED")),
        in_progress = Count('id', filter=Q(status="IN_PROGRESS")),
        pending = Count('id', filter=Q(status="PENDING"))
    )

    context = {
        "tasks":tasks,
        "counts":counts
    }

    return render(request, "dashboard/manager_dashboard.html",context)


@login_required
@permission_required("tasks.add_task", login_url='no-permission')
def create_task(request):

    task_form = TaskModelForm()
    task_detail_form = Task_detailModelform()

    if request.method=='POST':
        task_form = TaskModelForm(request.POST)
        task_detail_form = Task_detailModelform(request.POST)

        if task_form.is_valid() and task_detail_form.is_valid():

            '''For django Model Form'''

            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, "Created Task Successfully")
            return redirect("create-task")


    context = {"task_form":task_form, "task_detail_form":task_detail_form}
    return render(request, "taskForm.html",context)



@login_required
@permission_required("tasks.change_task", login_url='no-permission')
def update_task(request, id):

    task = Task.objects.get(id=id)

    task_form = TaskModelForm(instance=task)
    if task.details:
        task_detail_form = Task_detailModelform(instance=task.details)

    if request.method=='POST':
        task_form = TaskModelForm(request.POST, instance=task)
        task_detail_form = Task_detailModelform(request.POST, instance=task.details)

        if task_form.is_valid() and task_detail_form.is_valid():

            '''For django Model Form'''

            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()

            messages.success(request, "Task Update Successfully")
            return redirect("update-task", id)


    context = {"task_form":task_form, "task_detail_form":task_detail_form}
    return render(request, "taskForm.html",context)


@login_required
@permission_required("tasks.delete_task", login_url='no-permission')
def delete_task(request, id):
    if request.method == 'POST':
        task = Task.objects.get(id=id)
        task.delete()
        messages.success(request, 'Task Deleted Successfully')
        return redirect('manager-dashboard')
    else:
        messages.error(request, 'Something went wrong')
        return redirect('manager-dashboard')

@login_required
@permission_required("tasks.view_task", login_url='no-permission')
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

    # projects = Project.objects.annotate(num_task = Count("allTask")).order_by("id")
    # emps = Employee.objects.prefetch_related("tasks").all()

    # projects = Project.objects.prefetch_related("allTask").all()
    # tasks = Task.objects.filter(due_date = date.today()).all()
    # emps = Employee.objects.prefetch_related("tasks").all()
    tasks = Task.objects.select_related("details").all()
    # recent_task = Task.objects.order_by('-created_at').first()
    

    return render(request,"view_task.html",{"tasks":tasks})