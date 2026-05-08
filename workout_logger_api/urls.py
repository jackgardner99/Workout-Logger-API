from django.urls import path

from workout_logger_api.views.auth import LoginView, LogoutView, RegisterView
from workout_logger_api.views.workout_logs import WorkoutLogDetailView, WorkoutLogListCreateView

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("logs/", WorkoutLogListCreateView.as_view(), name="workout-logs"),
    path("logs/<int:pk>/", WorkoutLogDetailView.as_view(), name="workout-log-detail"),
]
