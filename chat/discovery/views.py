from django.http import JsonResponse

from .models import Venue


def venue_list(request):
    """Return all venues, optionally filtered by category."""
    category = request.GET.get("category")
    qs = Venue.objects.all()
    if category:
        qs = qs.filter(category=category)
    data = [
        {
            "id": v.id,
            "name": v.name,
            "category": v.category,
            "latitude": v.latitude,
            "longitude": v.longitude,
            "price_level": v.price_level,
            "rating": v.rating,
            "description": v.description,
        }
        for v in qs
    ]
    return JsonResponse({"venues": data})


def venue_detail(request, venue_id):
    """Return details for a single venue."""
    try:
        v = Venue.objects.get(pk=venue_id)
    except Venue.DoesNotExist:
        return JsonResponse({"error": "Venue not found"}, status=404)
    return JsonResponse(
        {
            "id": v.id,
            "name": v.name,
            "place_id": v.place_id,
            "category": v.category,
            "latitude": v.latitude,
            "longitude": v.longitude,
            "address": v.address,
            "description": v.description,
            "price_level": v.price_level,
            "rating": v.rating,
        }
    )
