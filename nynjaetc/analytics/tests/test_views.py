from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from pagetree.models import Hierarchy


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
