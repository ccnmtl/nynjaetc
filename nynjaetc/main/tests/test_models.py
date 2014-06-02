from django.test import TestCase
from django.test.utils import override_settings
from .factories import (
    UserFactory, SectionFactory, SectionTimestampFactory,
    SectionAlternateNavigationFactory, SectionQuizAnsweredCorrectlyFactory,
    PreferenceFactory, SectionPreferenceFactory,
)
from nynjaetc.main.models import (
    UserProfile, next_with_content, prev_with_content,
    my_quiz_submit,
)
from pagetree.models import Hierarchy


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


# first, we mock up a "Quiz" object
class MockQuiz(object):
    def original_submit(self, user, data):
        self.user = user
        self.data = data


class MyQuizSubmitTest(TestCase):
    def test_my_quiz_submit_basic(self):
        d = MockQuiz()
        u = UserFactory()
        my_quiz_submit(d, u, dict())
        self.assertEqual(d.user, u)
        self.assertEqual(d.data, dict())

    @override_settings(HRSA_ID_FIELD='question17')
    def test_my_quiz_submit_with_hrsa_id(self):
        d = MockQuiz()
        u = UserFactory()
        my_quiz_submit(d, u, dict(question17="foo"))
        # it needs to scrub it from the data dictionary that it passes along
        self.assertEqual(d.data, dict(question17="*****"))
        # then it sets it on the user profile instead
        the_profile, created = UserProfile.objects.get_or_create(user=u)
        self.assertEqual(created, False)
        self.assertEqual(the_profile.hrsa_id, "foo")

    @override_settings(HRSA_ID_FIELD='something_else_altogether')
    def test_my_quiz_submit_with_different_hrsa_id(self):
        d = MockQuiz()
        u = UserFactory()
        my_quiz_submit(d, u, dict(something_else_altogether="foo"))
        # it needs to scrub it from the data dictionary that it passes along
        self.assertEqual(d.data, dict(something_else_altogether="*****"))
        # then it sets it on the user profile instead
        the_profile, created = UserProfile.objects.get_or_create(user=u)
        self.assertEqual(created, False)
        self.assertEqual(the_profile.hrsa_id, "foo")


class SectionQuizAnsweredCorrectlyTest(TestCase):
    def test_unicode(self):
        h = Hierarchy.objects.create(name="main")
        root = h.get_root()
        sq = SectionQuizAnsweredCorrectlyFactory(section=root)
        self.assertEqual(str(sq), root.get_path())


class PreferenceTest(TestCase):
    def test_unicode(self):
        p = PreferenceFactory()
        self.assertTrue(str(p).startswith("pref"))

    def test_sections(self):
        p = PreferenceFactory()
        self.assertEqual(p.sections(), [])


class SectionPreferenceTest(TestCase):
    def test_unicode(self):
        h = Hierarchy.objects.create(name="main")
        root = h.get_root()
        sp = SectionPreferenceFactory(section=root)
        self.assertTrue(" has " in str(sp))
