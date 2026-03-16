from django.db import models


class Venue(models.Model):
    """A discoverable location (restaurant, hotel, activity spot, etc.)."""

    CATEGORY_CHOICES = [
        ("restaurant", "Restaurant"),
        ("hotel", "Hotel"),
        ("activity", "Activity"),
        ("hangout", "Hangout Spot"),
        ("leisure", "Leisure"),
    ]

    name = models.CharField(max_length=255)
    place_id = models.CharField(max_length=255, blank=True, default="")
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default="restaurant",
    )
    address = models.TextField(blank=True, default="")
    description = models.TextField(blank=True, default="")
    price_level = models.PositiveIntegerField(default=0)
    rating = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"
