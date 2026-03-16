from django.http import JsonResponse

from .models import Vote


def vote_list(request, event_id):
    """Return all votes for a given itinerary event."""
    votes = Vote.objects.filter(event_id=event_id)
    data = [
        {
            "id": v.id,
            "user": v.user.username,
            "vote_type": v.vote_type,
        }
        for v in votes
    ]
    return JsonResponse({"votes": data})
