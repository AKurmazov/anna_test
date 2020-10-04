from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status as rf_status
from django.shortcuts import get_object_or_404
from django.http import Http404

from tasks.serializers import TaskSerializer
from tasks.models import Task


class TaskListAPI(generics.ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = TaskSerializer

    def get_queryset(self):
        return self.request.user.tasks


class TaskCreateAPI(generics.CreateAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = TaskSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        task = serializer.save(creator=request.user)
        return Response({
            'task': TaskSerializer(task, context=self.get_serializer_context()).data
        }, status=rf_status.HTTP_201_CREATED)


class TaskRetrieveUpdateAPI(generics.RetrieveUpdateAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = TaskSerializer

    def get_object(self, **kwargs):
        instance = get_object_or_404(Task, id=self.kwargs['pk'])
        if self.request.user.id != instance.creator.id:
            raise Http404
        return instance

    def put(self, request, *args, **kwargs):
        task = self.get_object()
        serializer = self.serializer_class(task, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=rf_status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=rf_status.HTTP_400_BAD_REQUEST)
