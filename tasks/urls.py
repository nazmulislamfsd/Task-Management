from django.urls import path
from tasks.views import viewTask

urlpatterns = [
    path('view/', viewTask)
]