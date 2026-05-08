from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from workout_logger_api.models.log_exercise import LogExercise
from workout_logger_api.models.workout_log import WorkoutLog


def serialize_log(log):
    return {
        "id": log.id,
        "title": log.title,
        "workout_date": log.workout_date,
        "intensity": {"id": log.intensity.id, "name": log.intensity.name} if log.intensity else None,
        "notes": log.notes,
        "created_at": log.created_at,
        "updated_at": log.updated_at,
        "exercises": [
            {
                "id": le.id,
                "exercise_id": le.exercise_id,
                "exercise_name": le.exercise.name,
                "sets": le.sets,
                "reps": le.reps,
                "weight_lbs": le.weight_lbs,
                "notes": le.notes,
            }
            for le in log.log_exercises.select_related("exercise")
        ],
    }


class WorkoutLogListCreateView(APIView):
    def get(self, request):
        logs = WorkoutLog.objects.filter(user=request.user).select_related("intensity")
        return Response([serialize_log(log) for log in logs])

    @transaction.atomic
    def post(self, request):
        title = request.data.get("title")
        workout_date = request.data.get("workout_date")
        intensity_id = request.data.get("intensity_id")
        notes = request.data.get("notes", "")
        exercises = request.data.get("exercises", [])

        if not title or not workout_date:
            return Response(
                {"error": "title and workout_date are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        log = WorkoutLog.objects.create(
            user=request.user,
            title=title,
            workout_date=workout_date,
            intensity_id=intensity_id,
            notes=notes,
        )

        for ex in exercises:
            exercise_id = ex.get("exercise_id")
            sets = ex.get("sets")
            reps = ex.get("reps")
            weight_lbs = ex.get("weight_lbs")

            if not all([exercise_id, sets is not None, reps is not None, weight_lbs is not None]):
                raise ValueError("each exercise requires exercise_id, sets, reps, and weight_lbs")

            LogExercise.objects.create(
                log=log,
                exercise_id=exercise_id,
                sets=sets,
                reps=reps,
                weight_lbs=weight_lbs,
                notes=ex.get("notes", ""),
            )

        return Response(serialize_log(log), status=status.HTTP_201_CREATED)


class WorkoutLogDetailView(APIView):
    def get_log(self, pk, user):
        return get_object_or_404(WorkoutLog, pk=pk, user=user)

    def get(self, request, pk):
        return Response(serialize_log(self.get_log(pk, request.user)))

    def patch(self, request, pk):
        log = self.get_log(pk, request.user)
        log.title = request.data.get("title", log.title)
        log.workout_date = request.data.get("workout_date", log.workout_date)
        log.intensity_id = request.data.get("intensity_id", log.intensity_id)
        log.notes = request.data.get("notes", log.notes)
        log.save()
        return Response(serialize_log(log))

    def delete(self, request, pk):
        self.get_log(pk, request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
