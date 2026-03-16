from django.contrib.auth.models import User
from django.test import TestCase

from .models import Couple, UserProfile


class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="pass1234")

    def test_create_profile(self):
        profile = UserProfile.objects.create(user=self.user, bio="Hello!")
        self.assertEqual(str(profile), "Profile(alice)")
        self.assertEqual(profile.bio, "Hello!")

    def test_profile_defaults(self):
        profile = UserProfile.objects.create(user=self.user)
        self.assertEqual(profile.bio, "")
        self.assertIsNone(profile.date_of_birth)


class CoupleModelTest(TestCase):
    def setUp(self):
        self.u1 = User.objects.create_user(username="bob", password="pass1234")
        self.u2 = User.objects.create_user(username="carol", password="pass1234")

    def test_create_couple(self):
        couple = Couple.objects.create(shared_vibe="Romantic")
        couple.partners.add(self.u1, self.u2)
        self.assertEqual(couple.partners.count(), 2)
        self.assertEqual(couple.shared_vibe, "Romantic")

    def test_couple_str(self):
        couple = Couple.objects.create()
        couple.partners.add(self.u1, self.u2)
        label = str(couple)
        self.assertIn("bob", label)
        self.assertIn("carol", label)

    def test_default_vibe(self):
        couple = Couple.objects.create()
        self.assertEqual(couple.shared_vibe, "Adventurous")


class AccountsViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="dave", password="pass1234")

    def test_profile_detail_unauthenticated(self):
        resp = self.client.get("/accounts/profile/")
        self.assertEqual(resp.status_code, 401)

    def test_profile_detail_authenticated(self):
        self.client.login(username="dave", password="pass1234")
        resp = self.client.get("/accounts/profile/")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["username"], "dave")

    def test_couple_list_unauthenticated(self):
        resp = self.client.get("/accounts/couples/")
        self.assertEqual(resp.status_code, 401)

    def test_couple_list_authenticated(self):
        self.client.login(username="dave", password="pass1234")
        resp = self.client.get("/accounts/couples/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("couples", resp.json())
