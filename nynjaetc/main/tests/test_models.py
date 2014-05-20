from django.test import TestCase
from .factories import (UserFactory)
from nynjaetc.main.models import UserProfile, next_with_content


class UserProfileTest(TestCase):
    def test_unicode(self):
        u = UserFactory()
        up, _created = UserProfile.objects.get_or_create(user=u)
        self.assertTrue(str(up).startswith("Encrypted email and"))


class DummySection(object):
    def get_previous(self):
        return None

    def get_next(self):
        return None


class HelpersTest(TestCase):
    def test_next_with_content_no_next(self):
        d = DummySection()
        self.assertEqual(next_with_content(d), None)
