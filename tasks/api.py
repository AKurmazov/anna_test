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


# ToDo: Move update method to the serializer, and create put method here
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

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.name = request.data.get('name', instance.name)
        instance.description = request.data.get('description', instance.description)
        status = request.data.get('status', instance.status)

        if status == 'Scheduled':
            scheduled_on = request.data.get('scheduled_on', instance.scheduled_on)
            if not scheduled_on:
                return Response({
                    'detail': 'Deadline date is not provided'
                }, status=rf_status.HTTP_400_BAD_REQUEST)
            instance.status = status
            instance.scheduled_on = scheduled_on

        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=rf_status.HTTP_200_OK)
