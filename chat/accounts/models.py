from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    """Extended profile storing dating-specific preferences."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    bio = models.TextField(blank=True, default="")
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Profile({self.user.username})"


class Couple(models.Model):
    """
    Represents a pairing of users for shared itinerary planning.

    Uses ManyToManyField so that neither partner is arbitrarily
    designated as "partner one" or "partner two".
    """

    partners = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="couples",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    shared_vibe = models.CharField(max_length=100, default="Adventurous")
    anniversary = models.DateField(null=True, blank=True)

    def __str__(self):
        names = ", ".join(u.username for u in self.partners.all())
        return f"Couple({names})"
