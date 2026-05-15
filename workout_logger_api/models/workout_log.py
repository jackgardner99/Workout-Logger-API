from django.contrib.auth.models import User
from django.db import models

from workout_logger_api.models.intensity import Intensity


class WorkoutLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="workout_logs")
    intensity = models.ForeignKey(Intensity, on_delete=models.SET_NULL, null=True, related_name="workout_logs")
    title = models.CharField(max_length=255)
    workout_date = models.DateField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
