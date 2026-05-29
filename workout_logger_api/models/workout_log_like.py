from django.contrib.auth.models import User
from django.db import models

from workout_logger_api.models.workout_log import WorkoutLog


class WorkoutLogLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="log_likes")
    log = models.ForeignKey(WorkoutLog, on_delete=models.CASCADE, related_name="likes")

    class Meta:
        unique_together = ("user", "log")
