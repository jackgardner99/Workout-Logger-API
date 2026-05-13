from rest_framework.response import Response
from rest_framework.views import APIView

from workout_logger_api.models.exercise import Exercise


class ExerciseListView(APIView):
    def get(self, request):
        exercises = Exercise.objects.select_related("category").prefetch_related("muscle_exercises__muscle_group").order_by("name")
        data = [
            {
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
            for ex in exercises
        ]
        return Response(data)
