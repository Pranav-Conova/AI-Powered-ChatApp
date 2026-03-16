from django.test import TestCase

from .models import Venue


class VenueModelTest(TestCase):
    def test_create_venue(self):
        v = Venue.objects.create(
            name="Cafe Luna",
            category="restaurant",
            latitude=40.7128,
            longitude=-74.0060,
            price_level=2,
            rating=4.5,
        )
        self.assertEqual(str(v), "Cafe Luna (Restaurant)")

    def test_venue_defaults(self):
        v = Venue.objects.create(name="Test Spot")
        self.assertEqual(v.category, "restaurant")
        self.assertEqual(v.price_level, 0)
        self.assertEqual(v.rating, 0.0)


class DiscoveryViewTest(TestCase):
    def setUp(self):
        Venue.objects.create(name="Pizza Place", category="restaurant")
        Venue.objects.create(name="Art Gallery", category="activity")

    def test_venue_list(self):
        resp = self.client.get("/discovery/venues/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()["venues"]), 2)

    def test_venue_list_filter(self):
        resp = self.client.get("/discovery/venues/?category=activity")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()["venues"]), 1)
        self.assertEqual(resp.json()["venues"][0]["name"], "Art Gallery")

    def test_venue_detail(self):
        v = Venue.objects.first()
        resp = self.client.get(f"/discovery/venues/{v.id}/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["name"], v.name)

    def test_venue_detail_not_found(self):
        resp = self.client.get("/discovery/venues/9999/")
        self.assertEqual(resp.status_code, 404)
