from django.urls import path
from tasks.views import viewTask, show_specific_task

urlpatterns = [
    path('view/', viewTask),
    path('show-task/<int:id>', show_specific_task)
]