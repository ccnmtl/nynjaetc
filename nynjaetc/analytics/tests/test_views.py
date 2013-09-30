from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from pagetree.models import Hierarchy
from nynjaetc.analytics.views import checked_enduring_materials_box
from nynjaetc.analytics.views import timestamps_for
from nynjaetc.analytics.views import responses_for
from nynjaetc.analytics.views import generate_row_info
from nynjaetc.analytics.views import generate_row


class SimpleViewsTest(TestCase):
    def setUp(self):
        self.u = User.objects.create(username="foo", is_staff=True)
        self.u.set_password("bar")
        self.u.save()
        self.c = Client()
        self.c.login(username="foo", password="bar")
        self.h = Hierarchy.objects.create(name="main", base_url="")
        self.root = self.h.get_root()
        self.root.add_child_section_from_dict(
            {
                'label': 'Section 1',
                'slug': 'section-1',
                'pageblocks': [],
                'children': [],
            })
        r = self.root.get_children()
        self.section1 = r[0]

    def tearDown(self):
        self.u.delete()
        self.root.delete()
        self.h.delete()

    def test_analytics_csv(self):
        response = self.c.get("/analytics/csv/")
        self.assertEquals(response.status_code, 200)

    def test_analytics_table(self):
        response = self.c.get("/analytics/")
        self.assertEquals(response.status_code, 200)


class HelpersTest(TestCase):
    def setUp(self):
        self.u = User.objects.create(username="foo", is_staff=True)
        self.h = Hierarchy.objects.create(name="main", base_url="")
        self.root = self.h.get_root()
        self.root.add_child_section_from_dict(
            {
                'label': 'Section 1',
                'slug': 'section-1',
                'pageblocks': [],
                'children': [],
            })
        r = self.root.get_children()
        self.section1 = r[0]

    def tearDown(self):
        self.u.delete()
        self.root.delete()
        self.h.delete()

    def test_checked_enduring_materials_box(self):
        self.assertFalse(
            checked_enduring_materials_box(
                self.u,
                self.section1.id))

    def test_timestamps_for(self):
        self.assertEquals(timestamps_for(self.u), ({}, {}))

    def test_responses_for(self):
        self.assertEquals(responses_for(self.u), {})

    def test_generate_row_info(self):
        r = generate_row_info(
            self.u, [self.section1], [],
            cemb_pk=self.section1.id)
        self.assertEquals(r['the_user'], self.u)
        self.assertEquals(r['the_profile'].user, self.u)
        self.assertEquals(r['user_questions'], [])
        self.assertEquals(r['user_sections'], [None])
        self.assertEquals(r['read_intro'], False)

    def test_generate_row(self):
        r = generate_row(
            self.u, [self.section1], [], False,
            cemb_pk=self.section1.id)
        self.assertEquals(len(r), 7)

        r = generate_row(
            self.u, [self.section1], [], True,
            cemb_pk=self.section1.id)
        self.assertEquals(len(r), 11)
