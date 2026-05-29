from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from workout_logger_api.models.workout_log import WorkoutLog
from workout_logger_api.models.workout_log_comment import WorkoutLogComment


class WorkoutLogCommentListCreateView(APIView):
    def post(self, request, pk):
        log = get_object_or_404(WorkoutLog, pk=pk)
        body = request.data.get("body", "").strip()
        if not body:
            return Response({"error": "body is required"}, status=status.HTTP_400_BAD_REQUEST)
        comment = WorkoutLogComment.objects.create(user=request.user, log=log, body=body)
        return Response({
            "id": comment.id,
            "user": {"id": request.user.id, "username": request.user.username},
            "body": comment.body,
            "created_at": comment.created_at,
        }, status=status.HTTP_201_CREATED)


class WorkoutLogCommentDetailView(APIView):
    def delete(self, request, pk, comment_pk):
        comment = get_object_or_404(WorkoutLogComment, pk=comment_pk, log_id=pk, user=request.user)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
