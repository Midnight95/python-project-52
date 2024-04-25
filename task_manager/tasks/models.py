from django.db import models
from task_manager.users.models import User
from task_manager.statuses.models import Status
from task_manager.labels.models import Label


class Task(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        )

    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='author'
        )

    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='executor'
        )

    labels = models.ManyToManyField(
        Label,
        through='TaskLabels',
        through_fields=('task', 'label'),
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class TaskLabels(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.PROTECT)