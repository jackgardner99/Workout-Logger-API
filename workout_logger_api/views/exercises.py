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
    }


class ExerciseListView(APIView):
    def get(self, request):
        exercises = (
            Exercise.objects
            .select_related("category")
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
        )

        muscle_group_ids = request.data.get("muscle_group_ids", [])
        for mg_id in muscle_group_ids:
            if MuscleGroup.objects.filter(pk=mg_id).exists():
                MuscleExercise.objects.create(exercise=exercise, muscle_group_id=mg_id)

        exercise = (
            Exercise.objects
            .select_related("category")
            .prefetch_related("muscle_exercises__muscle_group")
            .get(pk=exercise.pk)
        )
        return Response(serialize_exercise(exercise), status=status.HTTP_201_CREATED)
