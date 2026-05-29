from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from workout_logger_api.models.exercise import Exercise, MuscleExercise, MuscleGroup


def serialize_exercise(ex):
    return {
        "id": ex.id,
        "name": ex.name,
        "description": ex.description,
        "difficulty": ex.difficulty,
        "category": {"id": ex.category.id, "name": ex.category.name} if ex.category else None,
        "muscle_groups": [
            {"id": me.muscle_group.id, "name": me.muscle_group.name}
            for me in ex.muscle_exercises.all()
        ],
        "created_by": {"username": ex.created_by.username} if ex.created_by else None,
    }


def _fetch_exercise(pk):
    return (
        Exercise.objects
        .select_related("category", "created_by")
        .prefetch_related("muscle_exercises__muscle_group")
        .get(pk=pk)
    )


def _sync_muscle_groups(exercise, muscle_group_ids):
    exercise.muscle_exercises.all().delete()
    for mg_id in muscle_group_ids:
        if MuscleGroup.objects.filter(pk=mg_id).exists():
            MuscleExercise.objects.create(exercise=exercise, muscle_group_id=mg_id)


class ExerciseListView(APIView):
    def get(self, request):
        exercises = (
            Exercise.objects
            .select_related("category", "created_by")
            .prefetch_related("muscle_exercises__muscle_group")
            .order_by("name")
        )
        return Response([serialize_exercise(ex) for ex in exercises])

    def post(self, request):
        name = request.data.get("name", "").strip()
        if not name:
            return Response({"error": "name is required"}, status=status.HTTP_400_BAD_REQUEST)

        exercise = Exercise.objects.create(
            name=name,
            description=request.data.get("description", "").strip(),
            difficulty=request.data.get("difficulty", "").strip(),
            category_id=request.data.get("category_id") or None,
            created_by=request.user,
        )

        _sync_muscle_groups(exercise, request.data.get("muscle_group_ids", []))

        return Response(serialize_exercise(_fetch_exercise(exercise.pk)), status=status.HTTP_201_CREATED)


class ExerciseDetailView(APIView):
    def _get_owned(self, pk, user):
        return get_object_or_404(Exercise, pk=pk, created_by=user)

    def put(self, request, pk):
        exercise = self._get_owned(pk, request.user)
        name = request.data.get("name", "").strip()
        if not name:
            return Response({"error": "name is required"}, status=status.HTTP_400_BAD_REQUEST)

        exercise.name = name
        exercise.description = request.data.get("description", "").strip()
        exercise.difficulty = request.data.get("difficulty", "").strip()
        exercise.category_id = request.data.get("category_id") or None
        exercise.save()

        _sync_muscle_groups(exercise, request.data.get("muscle_group_ids", []))

        return Response(serialize_exercise(_fetch_exercise(exercise.pk)))

    def delete(self, request, pk):
        self._get_owned(pk, request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
