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

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        status = validated_data.get('status', instance.status)

        if status == 'Scheduled':
            scheduled_on = validated_data.get('scheduled_on', instance.scheduled_on)
            if not scheduled_on:
                raise serializers.ValidationError('Deadline date should be provided')
            instance.scheduled_on = scheduled_on
        instance.status = status

        instance.save()
        return instance
