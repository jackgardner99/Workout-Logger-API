from rest_framework.response import Response
from rest_framework.views import APIView

from workout_logger_api.models.exercise import Category


class CategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.order_by("name")
        return Response([{"id": c.id, "name": c.name} for c in categories])
