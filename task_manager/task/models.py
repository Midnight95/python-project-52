from django.db import models
from task_manager.user.models import User
from task_manager.status.models import Status


class Task(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    status = models.ForeignKey(Status, on_delete=models.PROTECT)

    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name = 'author'
        )
    
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name = 'executor'
        )


    created_at = models.DateTimeField(auto_now_add=True)