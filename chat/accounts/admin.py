from django.contrib import admin

from .models import Couple, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "date_of_birth")


@admin.register(Couple)
class CoupleAdmin(admin.ModelAdmin):
    list_display = ("id", "shared_vibe", "anniversary", "created_at")
