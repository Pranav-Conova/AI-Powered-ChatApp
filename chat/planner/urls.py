from django.urls import path

from . import views

app_name = "planner"

urlpatterns = [
    path("itineraries/", views.itinerary_list, name="itinerary_list"),
    path(
        "itineraries/<int:itinerary_id>/",
        views.itinerary_detail,
        name="itinerary_detail",
    ),
]
