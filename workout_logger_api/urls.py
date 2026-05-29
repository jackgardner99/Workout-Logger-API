from django.urls import path

from workout_logger_api.views.auth import LoginView, LogoutView, RegisterView
from workout_logger_api.views.categories import CategoryListView
from workout_logger_api.views.exercises import ExerciseListView
from workout_logger_api.views.intensity import IntensityListView
from workout_logger_api.views.workout_logs import CommunityWorkoutLogListView, WorkoutLogDetailView, WorkoutLogListCreateView

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("categories/", CategoryListView.as_view(), name="categories"),
    path("exercises/", ExerciseListView.as_view(), name="exercises"),
    path("intensity/", IntensityListView.as_view(), name="intensity"),
    path("logs/", WorkoutLogListCreateView.as_view(), name="workout-logs"),
    path("logs/community/", CommunityWorkoutLogListView.as_view(), name="community-workout-logs"),
    path("logs/<int:pk>/", WorkoutLogDetailView.as_view(), name="workout-log-detail"),
]
