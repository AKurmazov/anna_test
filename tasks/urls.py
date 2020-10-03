from django.urls import path

from tasks.api import TaskListAPI, TaskCreateAPI, TaskRetrieveUpdateAPI

urlpatterns = [
    path('api/tasks/all', TaskListAPI.as_view()),
    path('api/tasks/create', TaskCreateAPI.as_view()),
    path('api/tasks/<pk>/', TaskRetrieveUpdateAPI.as_view()),
]
