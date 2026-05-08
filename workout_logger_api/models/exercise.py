from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class MuscleGroup(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Exercise(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="exercises")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, max_length=3000)
    difficulty = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class MuscleExercise(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name="muscle_exercises")
    muscle_group = models.ForeignKey(MuscleGroup, on_delete=models.CASCADE, related_name="muscle_exercises")

    class Meta:
        unique_together = ("exercise", "muscle_group")
