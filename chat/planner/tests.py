import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from accounts.models import Couple
from discovery.models import Venue

from .models import Itinerary, ItineraryEvent, Preference


class PreferenceModelTest(TestCase):
    def test_create_preference(self):
        user = User.objects.create_user(username="eve", password="pass1234")
        pref = Preference.objects.create(
            user=user, activity_type="cultural", vibe_score=0.8, price_level=3
        )
        self.assertEqual(str(pref), "Preference(eve, cultural)")


class ItineraryModelTest(TestCase):
    def setUp(self):
        self.u1 = User.objects.create_user(username="frank", password="pass1234")
        self.u2 = User.objects.create_user(username="grace", password="pass1234")
        self.couple = Couple.objects.create(shared_vibe="Chill")
        self.couple.partners.add(self.u1, self.u2)

    def test_create_itinerary(self):
        it = Itinerary.objects.create(
            couple=self.couple,
            title="Weekend Getaway",
            start_date=datetime.date(2026, 4, 1),
            end_date=datetime.date(2026, 4, 3),
        )
        self.assertEqual(str(it), "Weekend Getaway")
        self.assertFalse(it.is_public)


class ItineraryEventModelTest(TestCase):
    def setUp(self):
        u = User.objects.create_user(username="hank", password="pass1234")
        couple = Couple.objects.create()
        couple.partners.add(u)
        self.itinerary = Itinerary.objects.create(
            couple=couple,
            title="Day Trip",
            start_date=datetime.date(2026, 5, 1),
            end_date=datetime.date(2026, 5, 1),
        )
        self.venue = Venue.objects.create(name="Beach Bar", category="hangout")

    def test_create_event(self):
        now = timezone.now()
        event = ItineraryEvent.objects.create(
            itinerary=self.itinerary,
            venue=self.venue,
            start_time=now,
            end_time=now + datetime.timedelta(hours=2),
            notes="Sunset drinks",
        )
        self.assertIn("Beach Bar", str(event))

    def test_event_ordering(self):
        now = timezone.now()
        e2 = ItineraryEvent.objects.create(
            itinerary=self.itinerary,
            venue=self.venue,
            start_time=now + datetime.timedelta(hours=3),
            end_time=now + datetime.timedelta(hours=5),
            order=2,
        )
        e1 = ItineraryEvent.objects.create(
            itinerary=self.itinerary,
            venue=self.venue,
            start_time=now,
            end_time=now + datetime.timedelta(hours=2),
            order=1,
        )
        events = list(ItineraryEvent.objects.filter(itinerary=self.itinerary))
        self.assertEqual(events[0].id, e1.id)
        self.assertEqual(events[1].id, e2.id)


class PlannerViewTest(TestCase):
    def test_itinerary_list_unauthenticated(self):
        resp = self.client.get("/planner/itineraries/")
        self.assertEqual(resp.status_code, 401)

    def test_itinerary_detail_not_found(self):
        resp = self.client.get("/planner/itineraries/9999/")
        self.assertEqual(resp.status_code, 404)

    def test_itinerary_detail_found(self):
        u = User.objects.create_user(username="ivy", password="pass1234")
        couple = Couple.objects.create()
        couple.partners.add(u)
        it = Itinerary.objects.create(
            couple=couple,
            title="City Tour",
            start_date=datetime.date(2026, 6, 1),
            end_date=datetime.date(2026, 6, 2),
        )
        resp = self.client.get(f"/planner/itineraries/{it.id}/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["title"], "City Tour")
