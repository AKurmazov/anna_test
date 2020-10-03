# Generated by Django 3.1.1 on 2020-10-03 20:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=128)),
                ('description', models.TextField(blank=True)),
                ('status', models.CharField(blank=True, choices=[('New', 'New'), ('Scheduled', 'Scheduled'), ('In-Progress', 'In-Progress'), ('Completed', 'Completed')], default='New', max_length=32)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('scheduled_on', models.DateTimeField(blank=True, default=None, null=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
