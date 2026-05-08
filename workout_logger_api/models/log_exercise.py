from django.db import models

from workout_logger_api.models.exercise import Exercise
from workout_logger_api.models.workout_log import WorkoutLog


class LogExercise(models.Model):
    log = models.ForeignKey(WorkoutLog, on_delete=models.CASCADE, related_name="log_exercises")
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name="log_exercises")
    sets = models.IntegerField()
    reps = models.IntegerField()
    weight_lbs = models.FloatField()
    notes = models.TextField(blank=True)
