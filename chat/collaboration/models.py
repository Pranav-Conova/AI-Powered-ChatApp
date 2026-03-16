from django.conf import settings
from django.db import models

from planner.models import Itinerary, ItineraryEvent


class Vote(models.Model):
    """A vote cast by a user on a proposed itinerary event."""

    VOTE_CHOICES = [
        ("up", "Up"),
        ("down", "Down"),
        ("veto", "Veto"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="votes",
    )
    event = models.ForeignKey(
        ItineraryEvent,
        on_delete=models.CASCADE,
        related_name="votes",
    )
    vote_type = models.CharField(max_length=10, choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "event")

    def __str__(self):
        return f"{self.user.username} -> {self.vote_type} on {self.event}"
