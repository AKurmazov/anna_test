from rest_framework import serializers
from accounts.serializers import UserSerializer

from tasks.models import Task, ChangeLog


class TaskSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = '__all__'

    def create(self, validated_data):
        name = validated_data.get('name')
        description = validated_data.get('description')
        creator = validated_data.get('creator')

        if not name or not description:
            raise serializers.ValidationError('Both name and description are required')

        task = Task.objects.create(name=name, description=description, creator=creator)

        # Make a change record
        log = {
            'name': 'null -> ' + validated_data['name'],
            'description': 'null -> ' + validated_data['description'],
            'status': 'null -> New',
        }
        change_log = ChangeLog.objects.create(log=log, task=task)

        return task

    def update(self, instance, validated_data):
        name = validated_data.get('name')
        description = validated_data.get('description')
        status = validated_data.get('status')
        scheduled_on = validated_data.get('scheduled_on')

        log = {}
        if name:
            log['name'] = f'{instance.name} -> {name}'
        if description:
            log['description'] = f'{instance.description} -> {description}'
        if status:
            log['status'] = f'{instance.status} -> {status}'
        if scheduled_on:
            log['scheduled_on'] = f'{instance.scheduled_on} -> {scheduled_on}'

        if not log:
            raise serializers.ValidationError('Data is not provided')

        instance.name = name or instance.name
        instance.description = description or instance.description
        status = status or instance.status

        if status == 'Scheduled':
            scheduled_on = scheduled_on or instance.scheduled_on
            if not scheduled_on:
                raise serializers.ValidationError('Deadline date should be provided')
            instance.scheduled_on = scheduled_on
        instance.status = status
        instance.save()

        change_log = ChangeLog.objects.create(log=log, task=instance)

        return instance


class ChangeLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChangeLog
        fields = ('id', 'log', 'created_at')
