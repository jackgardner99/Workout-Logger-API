from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from workout_logger_api.models.workout_log import WorkoutLog
from workout_logger_api.models.workout_log_like import WorkoutLogLike


class WorkoutLogLikeView(APIView):
    def post(self, request, pk):
        log = get_object_or_404(WorkoutLog, pk=pk)
        like, created = WorkoutLogLike.objects.get_or_create(user=request.user, log=log)
        if not created:
            like.delete()
        return Response({"liked": created, "like_count": log.likes.count()})
