from django.test import TestCase
from .factories import (UserFactory)
from nynjaetc.main.models import UserProfile


class UserProfileTest(TestCase):
    def test_unicode(self):
        u = UserFactory()
        up, _created = UserProfile.objects.get_or_create(user=u)
        self.assertTrue(str(up).startswith("Encrypted email and"))
