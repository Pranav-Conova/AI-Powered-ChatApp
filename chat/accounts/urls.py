from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("profile/", views.profile_detail, name="profile_detail"),
    path("couples/", views.couple_list, name="couple_list"),
]
