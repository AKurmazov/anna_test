from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField


class Task(models.Model):
    STATUS_CHOICES = (
        ('New', 'New'),
        ('Scheduled', 'Scheduled'),
        ('In-Progress', 'In-Progress'),
        ('Completed', 'Completed')
    )

    name = models.CharField(max_length=128, blank=True, null=False)
    description = models.TextField(blank=True, null=False)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='New', blank=True, null=False)
    creator = models.ForeignKey(User, related_name='tasks', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    scheduled_on = models.DateTimeField(blank=True, null=True, default=None)

    def __str__(self):
        return f"Task#{self.pk} | Created by {self.creator}"


class ChangeLog(models.Model):
    log = JSONField()
    task = models.ForeignKey(Task, related_name='changes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Change log | Task#{self.task} at {self.created_at}"

