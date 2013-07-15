from datetime import datetime
from django.contrib.auth.models import User, AnonymousUser
from django.test import TestCase
from django.utils.timezone import utc
from nynjaetc.main.models import SectionTimestamp
from nynjaetc.main.views_helpers import whether_already_visited
from nynjaetc.main.views_helpers import already_visited_pages
from pagetree.models import Hierarchy


class WAVTest(TestCase):
    def setUp(self):
        self.u = User.objects.create(username="test1")
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

    def test_whether_already_visited_none(self):
        SectionTimestamp.objects.all().delete()
        self.assertFalse(whether_already_visited(self.section1, self.u))

    def test_whether_already_visited_some(self):
        SectionTimestamp.objects.create(
            section=self.section1,
            user=self.u,
            timestamp=datetime.utcnow().replace(tzinfo=utc), )
        self.assertTrue(whether_already_visited(self.section1, self.u))


class AVPTest(TestCase):
    def setUp(self):
        self.u = User.objects.create(username="test1")
        self.anon_u = AnonymousUser()
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

    def test_already_visited_pages_none(self):
        self.assertEquals(
            already_visited_pages(self.section1, self.u),
            [])

    def test_already_visited_pages_anon(self):
        """ calling with anon user returns the section """
        self.assertEquals(
            already_visited_pages(self.section1, self.anon_u),
            self.section1)
