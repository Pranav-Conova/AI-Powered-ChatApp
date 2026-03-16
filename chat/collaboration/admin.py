from django.contrib import admin

from .models import Vote


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("user", "event", "vote_type", "created_at")
