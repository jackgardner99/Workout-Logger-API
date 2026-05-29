from django.contrib.auth.models import User
from django.db import models

from workout_logger_api.models.workout_log import WorkoutLog


class WorkoutLogComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="log_comments")
    log = models.ForeignKey(WorkoutLog, on_delete=models.CASCADE, related_name="comments")
    body = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
