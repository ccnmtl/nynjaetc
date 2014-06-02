from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.conf import settings
from pagetree.models import Hierarchy, PageBlock
from nynjaetc.main.views import background, has_submitted_pretest
from .factories import (
    SectionPreferenceFactory, PreferenceFactory,
    UserFactory, QuizFactory, SubmissionFactory)


class BasicTest(TestCase):

    def setUp(self):
        self.c = Client()
        self.u = User.objects.create(username="testuser")
        self.u.set_password("test")
        self.u.save()
        self.c.login(username="testuser", password="test")

    def tearDown(self):
        self.u.delete()

    def test_root(self):
        response = self.c.get("/")
        self.assertEquals(response.status_code, 200)

    def test_edit(self):
        response = self.c.get("/edit/")
        self.assertEquals(response.status_code, 200)

    def test_reset(self):
        response = self.c.post(
            "/",
            dict(action="reset"),
        )
        self.assertEquals(response.status_code, 302)

    def test_submit(self):
        response = self.c.post(
            "/",
            dict(action=""),
        )
        self.assertEquals(response.status_code, 302)

    def test_smoketest(self):
        response = self.c.get("/smoketest/")
        self.assertEquals(response.status_code, 200)

    def test_resend_activation_email_form(self):
        response = self.c.get("/resend_activation_email/")
        self.assertEquals(response.status_code, 200)

    def test_resend_activation_email(self):
        # empty
        response = self.c.post("/resend_activation_email/", dict())
        self.assertEquals(response.status_code, 200)
        # nonexistant
        response = self.c.post("/resend_activation_email/",
                               dict(email='foo@bar.com'))
        self.assertEquals(response.status_code, 200)

    def test_latest_page(self):
        r = self.c.get("/latest/")
        self.assertEquals(r.status_code, 302)

    def test_about(self):
        r = self.c.get("/about/")
        self.assertEqual(r.status_code, 200)

    def test_record_section_as_answered_correctly(self):
        r = self.c.get("/record_section_as_answered_correctly/")
        self.assertEqual(r.status_code, 200)


class StaffViewTests(TestCase):
    def setUp(self):
        self.c = Client()
        self.u = User.objects.create(username="testuser",
                                     is_staff=True)
        self.u.set_password("test")
        self.u.save()
        self.c.login(username="testuser", password="test")

    def test_edit_page(self):
        r = self.c.get("/edit/")
        self.assertEquals(r.status_code, 200)


class AnonViewTests(TestCase):
    def setUp(self):
        self.c = Client()

    def test_latest_page(self):
        r = self.c.get("/latest/")
        self.assertEquals(r.status_code, 302)


class DummyRequest(object):
    path = "/foo/"


class BackgroundTest(TestCase):
    def test_nonexistant(self):
        r = background(DummyRequest(), "not in there")
        self.assertEquals(r.status_code, 302)


class HasSubmittedPretest(TestCase):
    def setUp(self):
        self.h = Hierarchy.objects.create(name="main")
        self.root = self.h.get_root()
        self.root.add_child_section_from_dict(
            {
                'label': 'Section 1',
                'slug': 'section-1',
                'pageblocks': [],
                'children': [],
            })
        self.section1 = self.root.get_children()[0]
        self.p = PreferenceFactory(slug=settings.PRETEST_PREF_SLUG)
        self.sp = SectionPreferenceFactory(section=self.section1,
                                           preference=self.p)
        self.u = UserFactory()

    def test_no_submissions(self):
        self.assertFalse(has_submitted_pretest(self.u, self.h))

    def test_with_submissions(self):
        q = QuizFactory()
        PageBlock.objects.create(
            section=self.section1,
            content_object=q)
        SubmissionFactory(quiz=q, user=self.u)
        self.assertTrue(has_submitted_pretest(self.u, self.h))

    def test_with_other_submissions(self):
        # make another section, that has submissions from this
        # user, but is not the pre-test section
        q = QuizFactory()
        self.root.add_child_section_from_dict(
            {
                'label': 'Section 2',
                'slug': 'section-2',
                'pageblocks': [],
                'children': [],
            }
        )
        section2 = self.root.get_children()[1]
        PageBlock.objects.create(
            section=section2,
            content_object=q)
        SubmissionFactory(quiz=q, user=self.u)
        self.assertFalse(has_submitted_pretest(self.u, self.h))
