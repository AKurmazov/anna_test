from django.urls import path

from tasks.api import TaskListAPI, TaskCreateAPI, TaskRetrieveUpdateAPI, ChangeLogListAPI

urlpatterns = [
    path('api/tasks/all', TaskListAPI.as_view(), name='tasks-all'),
    path('api/tasks/create', TaskCreateAPI.as_view(), name='task-create'),
    path('api/tasks/<pk>/', TaskRetrieveUpdateAPI.as_view(), name='task-retrieve-update'),
    path('api/tasks/<pk>/changes', ChangeLogListAPI.as_view(), name='task-changes')
]
