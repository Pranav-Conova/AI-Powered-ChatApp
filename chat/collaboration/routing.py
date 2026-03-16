from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(
        r"ws/itinerary/(?P<room_name>\w+)/$",
        consumers.ItineraryConsumer.as_asgi(),
    ),
]
