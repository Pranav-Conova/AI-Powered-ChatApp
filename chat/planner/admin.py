from django.contrib import admin

from .models import Itinerary, ItineraryEvent, Preference


@admin.register(Preference)
class PreferenceAdmin(admin.ModelAdmin):
    list_display = ("user", "activity_type", "vibe_score", "price_level")


class ItineraryEventInline(admin.TabularInline):
    model = ItineraryEvent
    extra = 0


@admin.register(Itinerary)
class ItineraryAdmin(admin.ModelAdmin):
    list_display = ("title", "couple", "start_date", "end_date", "is_public")
    inlines = [ItineraryEventInline]


@admin.register(ItineraryEvent)
class ItineraryEventAdmin(admin.ModelAdmin):
    list_display = ("venue", "itinerary", "start_time", "end_time", "order")
