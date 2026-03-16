from django.conf import settings
from django.db import models

from accounts.models import Couple
from discovery.models import Venue


class Preference(models.Model):
    """Individual user preferences used by the recommendation engine."""

    ACTIVITY_CHOICES = [
        ("adventurous", "Adventurous"),
        ("cultural", "Cultural & Educational"),
        ("active", "Active Leisure"),
        ("lowcost", "Low-Cost / Niche"),
        ("dining", "Dining"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="preferences",
    )
    activity_type = models.CharField(
        max_length=50,
        choices=ACTIVITY_CHOICES,
        default="dining",
    )
    vibe_score = models.FloatField(default=0.5)
    price_level = models.PositiveIntegerField(default=2)

    def __str__(self):
        return f"Preference({self.user.username}, {self.activity_type})"


class Itinerary(models.Model):
    """Parent container for a series of scheduled events."""

    couple = models.ForeignKey(
        Couple,
        on_delete=models.CASCADE,
        related_name="itineraries",
    )
    title = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "itineraries"

    def __str__(self):
        return self.title


class ItineraryEvent(models.Model):
    """A single time-block event within an itinerary, linked to a venue."""

    itinerary = models.ForeignKey(
        Itinerary,
        on_delete=models.CASCADE,
        related_name="events",
    )
    venue = models.ForeignKey(
        Venue,
        on_delete=models.CASCADE,
        related_name="events",
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    notes = models.TextField(blank=True, default="")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "start_time"]

    def __str__(self):
        return f"{self.venue.name} @ {self.start_time:%H:%M}"
