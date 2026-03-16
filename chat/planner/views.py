from django.http import JsonResponse

from .models import Itinerary, ItineraryEvent


def itinerary_list(request):
    """Return itineraries belonging to the current user's couples."""
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)
    itineraries = Itinerary.objects.filter(couple__partners=request.user)
    data = [
        {
            "id": it.id,
            "title": it.title,
            "start_date": str(it.start_date),
            "end_date": str(it.end_date),
            "is_public": it.is_public,
        }
        for it in itineraries
    ]
    return JsonResponse({"itineraries": data})


def itinerary_detail(request, itinerary_id):
    """Return a single itinerary with its events."""
    try:
        it = Itinerary.objects.get(pk=itinerary_id)
    except Itinerary.DoesNotExist:
        return JsonResponse({"error": "Itinerary not found"}, status=404)

    # Public itineraries are accessible to everyone; private ones require
    # the requesting user to be one of the couple's partners.
    if not it.is_public:
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Authentication required"}, status=401)
        if not it.couple.partners.filter(pk=request.user.pk).exists():
            return JsonResponse({"error": "Forbidden"}, status=403)

    events = ItineraryEvent.objects.filter(itinerary=it).select_related("venue")
    event_data = [
        {
            "id": e.id,
            "venue": e.venue.name,
            "start_time": str(e.start_time),
            "end_time": str(e.end_time),
            "notes": e.notes,
            "order": e.order,
        }
        for e in events
    ]
    return JsonResponse(
        {
            "id": it.id,
            "title": it.title,
            "start_date": str(it.start_date),
            "end_date": str(it.end_date),
            "is_public": it.is_public,
            "events": event_data,
        }
    )
