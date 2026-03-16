from django.urls import path

from . import views

app_name = "collaboration"

urlpatterns = [
    path("events/<int:event_id>/votes/", views.vote_list, name="vote_list"),
]
