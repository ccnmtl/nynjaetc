from django.test import TestCase
from .factories import (
    UserFactory, SectionFactory, SectionTimestampFactory,
    SectionAlternateNavigationFactory,
)
from nynjaetc.main.models import (
    UserProfile, next_with_content, prev_with_content)


class UserProfileTest(TestCase):
    def test_unicode(self):
        u = UserFactory()
        up, _created = UserProfile.objects.get_or_create(user=u)
        self.assertTrue(str(up).startswith("Encrypted email and"))


class DummySection(object):
    def __init__(self, n=None, p=None, lohc=True):
        self.next = n
        self.prev = p
        self.lohc = lohc

    def get_previous(self):
        return self.prev

    def get_next(self):
        return self.next

    def is_leaf_or_has_content(self):
        return self.lohc


class HelpersTest(TestCase):
    def test_next_with_content_no_next(self):
        d = DummySection()
        self.assertEqual(next_with_content(d), None)

    def test_next_with_content(self):
        n = DummySection()
        d = DummySection(n=n)
        self.assertEqual(next_with_content(d), n)
        d.lohc = False
        d2 = DummySection(n=d)
        self.assertEqual(next_with_content(d2), n)

    def test_prev_with_content_no_prev(self):
        d = DummySection()
        self.assertEqual(prev_with_content(d), None)

    def test_prev_with_content(self):
        p = DummySection()
        d = DummySection(p=p)
        self.assertEqual(prev_with_content(d), p)
        d.lohc = False
        d2 = DummySection(p=d)
        self.assertEqual(prev_with_content(d2), p)


class SectionTimestampTest(TestCase):
    def test_unicode(self):
        s = SectionFactory()
        swt = SectionTimestampFactory(section=s)
        self.assertEqual(str(swt), "")


class SectionAlternateNavigationTest(TestCase):
    def test_unicode(self):
        s = SectionFactory()
        san = SectionAlternateNavigationFactory(section=s)
        self.assertEqual(str(san), "Alternate nav for ")
