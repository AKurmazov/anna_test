from django.db import models
from django.contrib.auth.models import User


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
