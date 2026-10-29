from django.urls import path
from . import views

urlpatterns = [
 path("candidates/", views.candidates), path("candidates/<int:candidate_id>/", views.candidate_detail),
 path("messages/send/", views.send_messages), path("messages/<int:message_id>/retry/", views.retry), path("provider/status/", views.provider_webhook),
 path("templates/", views.templates), path("health/", views.health),
]
