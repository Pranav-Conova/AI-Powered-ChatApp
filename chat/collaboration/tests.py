import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from accounts.models import Couple
from discovery.models import Venue
from planner.models import Itinerary, ItineraryEvent

from .models import Vote


class VoteModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="jack", password="pass1234")
        couple = Couple.objects.create()
        couple.partners.add(self.user)
        venue = Venue.objects.create(name="Jazz Club", category="hangout")
        itinerary = Itinerary.objects.create(
            couple=couple,
            title="Evening Out",
            start_date=datetime.date(2026, 7, 1),
            end_date=datetime.date(2026, 7, 1),
        )
        now = timezone.now()
        self.event = ItineraryEvent.objects.create(
            itinerary=itinerary,
            venue=venue,
            start_time=now,
            end_time=now + datetime.timedelta(hours=2),
        )

    def test_create_vote(self):
        vote = Vote.objects.create(
            user=self.user, event=self.event, vote_type="up"
        )
        self.assertIn("up", str(vote))

    def test_unique_constraint(self):
        Vote.objects.create(user=self.user, event=self.event, vote_type="up")
        with self.assertRaises(Exception):
            Vote.objects.create(user=self.user, event=self.event, vote_type="down")


class VoteViewTest(TestCase):
    def test_vote_list(self):
        user = User.objects.create_user(username="kate", password="pass1234")
        couple = Couple.objects.create()
        couple.partners.add(user)
        venue = Venue.objects.create(name="Rooftop Bar", category="hangout")
        itinerary = Itinerary.objects.create(
            couple=couple,
            title="Night Plan",
            start_date=datetime.date(2026, 8, 1),
            end_date=datetime.date(2026, 8, 1),
        )
        now = timezone.now()
        event = ItineraryEvent.objects.create(
            itinerary=itinerary,
            venue=venue,
            start_time=now,
            end_time=now + datetime.timedelta(hours=1),
        )
        Vote.objects.create(user=user, event=event, vote_type="up")
        resp = self.client.get(f"/collaboration/events/{event.id}/votes/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()["votes"]), 1)
