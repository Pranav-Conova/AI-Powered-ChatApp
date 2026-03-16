from django.urls import path

from . import views

app_name = "discovery"

urlpatterns = [
    path("venues/", views.venue_list, name="venue_list"),
    path("venues/<int:venue_id>/", views.venue_detail, name="venue_detail"),
]
