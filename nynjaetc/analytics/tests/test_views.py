from datetime import datetime
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from pagetree.models import Hierarchy
from nynjaetc.analytics.views import (
    checked_enduring_materials_box,
    timestamps_for, responses_for, generate_row_info, generate_row,
    sum_of_gaps_longer_than_x_minutes, time_spent_estimate,
    ProfileHeaderMaker,
)


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

    def test_analytics_table_testing(self):
        with self.settings(ENDURING_MATERIALS_SECTION_ID=self.section1.id):
            response = self.c.get("/analytics/testing/")
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
        with self.settings(ENDURING_MATERIALS_SECTION_ID=self.section1.id):
            self.assertFalse(
                checked_enduring_materials_box(self.u))

    def test_timestamps_for(self):
        self.assertEquals(timestamps_for(self.u), ({}, {}))

    def test_responses_for(self):
        self.assertEquals(responses_for(self.u), {})

    def test_generate_row_info(self):
        with self.settings(ENDURING_MATERIALS_SECTION_ID=self.section1.id):
            r = generate_row_info(
                self.u, [self.section1], [])
            self.assertEquals(r['the_user'], self.u)
            self.assertEquals(r['the_profile'].user, self.u)
            self.assertEquals(r['user_questions'], [])
            self.assertEquals(r['user_sections'], [None])
            self.assertEquals(r['read_intro'], False)

    def test_generate_row(self):
        with self.settings(ENDURING_MATERIALS_SECTION_ID=self.section1.id):
            self.u.last_login = datetime.now()
            r = generate_row(
                self.u, [self.section1], [], False)
            self.assertEquals(len(r), 7)

            r = generate_row(
                self.u, [self.section1], [], True)
        self.assertEquals(len(r), 11)

    def test_sum_of_gaps_longer_than_x(self):
        timestamps = [datetime.now(), datetime.now()]
        self.assertEqual(sum_of_gaps_longer_than_x_minutes(1, timestamps), 0)

    def test_sum_of_gaps_longer_than_x_empty(self):
        self.assertEqual(sum_of_gaps_longer_than_x_minutes(1, []), 0)

    def test_time_spent_estimate_empty(self):
        self.assertEqual(time_spent_estimate([]), 0)

    def test_time_spent_estimate(self):
        timestamps = [datetime.now(), datetime.now()]
        self.assertEqual(time_spent_estimate(timestamps), "0.0")

    def test_profile_header_maker(self):
        phm = ProfileHeaderMaker(None)
        self.assertEqual(phm.header(), [None, None])
