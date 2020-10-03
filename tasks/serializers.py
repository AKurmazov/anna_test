from rest_framework import serializers
from accounts.serializers import UserSerializer

from tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = '__all__'

    def create(self, validated_data):
        task = Task.objects.create(name=validated_data['name'], description=validated_data['description'],
                                   creator=validated_data['creator'])
        return task
