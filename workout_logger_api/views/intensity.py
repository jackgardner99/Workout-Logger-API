from rest_framework.response import Response
from rest_framework.views import APIView

from workout_logger_api.models.intensity import Intensity


class IntensityListView(APIView):
    def get(self, request):
        intensities = Intensity.objects.order_by("id")
        return Response([{"id": i.id, "name": i.name} for i in intensities])
