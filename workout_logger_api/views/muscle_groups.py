from rest_framework.response import Response
from rest_framework.views import APIView

from workout_logger_api.models.exercise import MuscleGroup


class MuscleGroupListView(APIView):
    def get(self, request):
        groups = MuscleGroup.objects.order_by("name")
        return Response([{"id": g.id, "name": g.name} for g in groups])
