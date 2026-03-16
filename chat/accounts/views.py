from django.http import JsonResponse

from .models import Couple, UserProfile


def profile_detail(request):
    """Return the current user's profile as JSON."""
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return JsonResponse(
        {
            "username": request.user.username,
            "bio": profile.bio,
            "date_of_birth": str(profile.date_of_birth) if profile.date_of_birth else None,
        }
    )


def couple_list(request):
    """Return couples the current user belongs to."""
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)
    couples = Couple.objects.filter(partners=request.user)
    data = [
        {
            "id": c.id,
            "shared_vibe": c.shared_vibe,
            "anniversary": str(c.anniversary) if c.anniversary else None,
            "partners": [u.username for u in c.partners.all()],
        }
        for c in couples
    ]
    return JsonResponse({"couples": data})
