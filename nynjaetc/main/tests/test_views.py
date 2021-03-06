from django.core import mail
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.conf import settings
from pagetree.models import Hierarchy, PageBlock
from nynjaetc.main.views import background, has_submitted_pretest, Pretest
from .factories import (
    SectionPreferenceFactory, PreferenceFactory,
    UserFactory, QuizFactory, SubmissionFactory,
    SectionTimestampFactory,
)


class BasicTest(TestCase):

    def setUp(self):
        self.c = Client()
        self.u = User.objects.create(username="testuser")
        self.u.is_staff = True
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

    def test_pretest(self):
        p = Pretest(self.section1)
        self.assertFalse(p.user_has_submitted('', self.u))


class LoggedInAndHasSectionTest(TestCase):
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
        self.c = Client()
        self.u = User.objects.create(username="testuser")
        self.u.set_password("test")
        self.u.save()
        self.c.login(username="testuser", password="test")

    def test_latest_page_visited(self):
        SectionTimestampFactory(user=self.u, section=self.section1)
        r = self.c.get("/latest/section-1/")
        self.assertEqual(r.status_code, 302)

    def record_answered_correctly_post_null(self):
        r = self.c.post("/record_section_as_answered_correctly/", dict())
        self.assertEqual(r.content, '')

    def record_answered_correctly_post(self):
        r = self.c.post("/record_section_as_answered_correctly/",
                        dict(
                            section_id=self.section1.id,
                        ),
                        HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(r.content, 'ok')


class AltNavTest(TestCase):
    def setUp(self):
        self.c = Client()
        self.u = User.objects.create(username="testuser")
        self.u.set_password("test")
        self.u.save()
        self.c.login(username="testuser", password="test")

    def test_create_altnav(self):
        r = self.c.get("/manage/altnav/add/")
        self.assertTrue(r.status_code, 200)

    def test_create_secprof(self):
        r = self.c.get("/manage/secprof/add/")
        self.assertTrue(r.status_code, 200)


class RegistrationTest(TestCase):
    def setUp(self):
        self.c = Client()

    def test_get_register(self):
        r = self.c.get("/accounts/register/")
        self.assertEqual(r.status_code, 200)

    def test_post_register(self):
        r = self.c.post(
            "/accounts/register/",
            dict(
                username='foo',
                email='test@example.com',
                password1='bar',
                password2='bar',
            )
        )
        self.assertEqual(r.status_code, 302)
        self.assertEqual(mail.outbox[0].to, [u'test@example.com'])

    def test_change_password_form(self):
        u = User.objects.create(username="testuser")
        u.set_password("test")
        u.save()
        self.c.login(username="testuser", password="test")
        r = self.c.get("/password/change/")
        self.assertEqual(r.status_code, 200)

    def test_reset_password_form(self):
        u = User.objects.create(username="testuser")
        u.set_password("test")
        u.save()
        r = self.c.get("/password/reset/")
        self.assertEqual(r.status_code, 200)

    def test_reset_password_form_post_user_not_found(self):
        r = self.c.post("/password/reset/", {'email': 'foo@foo.com'},
                        follow=True)
        self.assertEqual(r.status_code, 200)
        self.assertTrue('email' in r.context['form'].errors)
        self.assertEquals(
            r.context['form'].errors['email'][0],
            'No user found matching the email address foo@foo.com')

    def test_reset_password_form_post_unusable_password(self):
        user = User(username='testuser', password='test', email='foo@foo.com')
        user.set_unusable_password()
        user.save()

        r = self.c.post("/password/reset/", {'email': 'foo@foo.com'},
                        follow=True)
        self.assertEqual(r.status_code, 200)
        self.assertTrue('email' in r.context['form'].errors)
        self.assertEquals(r.context['form'].errors['email'][0],
                          'This user\'s password cannot be changed')

    def test_reset_password_form_post(self):
        u = User.objects.create(username="testuser", email='foo@foo.com')
        u.set_password("test")
        u.save()
        r = self.c.post("/password/reset/", {'email': 'foo@foo.com'},
                        follow=True)
        self.assertEqual(r.status_code, 200)
        self.assertEquals(r.context['title'], 'Password reset sent')
        self.assertFalse('form' in r.context)
